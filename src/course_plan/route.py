from fastapi import FastAPI, HTTPException,Request,Form
from pydantic import BaseModel
from datetime import datetime
import json
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from src.course_plan.crew import CoursePlan
from src.course_plan.course_suggestion import CourseCrew
from src.course_plan.db.util import getCurrentUser, addCourse,getAllCourses, add_course_modules
from src.course_plan.db.courseimporter import CourseImporter
from src.course_plan.db.CalendarStudyPlanner import CalendarStudyPlanner
from src.course_plan.model.user import User,Course
from typing import Optional
import traceback
import os

app = FastAPI()

templates = Jinja2Templates(directory="src/course_plan/templates")
app.mount("/static", StaticFiles(directory="src/course_plan/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the request body schema
class CourseRequest(BaseModel):
    subject: str
    course_title: str
    course_topic: str
    audience_type: str

class StudyPlanRequest(BaseModel):
    course_id: int
    start_date: str  # Format: "YYYY-MM-DD"
    skip_weekends: Optional[bool] = True




# @app.post("/run-course-plan/")
# async def run_course_plan(request: CourseRequest):
#     inputs = {
#         "subject": request.subject,
#         "course_title": request.course_title,
#         "course_topic": request.course_topic,
#         "audience_type": request.audience_type,
#         "current_year": str(datetime.now().year)
#     }

#     try:
#         result = CoursePlan().crew().kickoff(inputs=inputs)
#         return {"status": "success", "result": result}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile", response_class=HTMLResponse)
async def get_profile(request: Request):
    user = User(getCurrentUser())
    return templates.TemplateResponse("profile.html",
                                       {"request": request,
                                        "user_name": user.getUserName(),
                                        "user_email": user.getUserEmail(),
                                        "user_style": "Hands-on"})
@app.get("/my-courses", response_class=JSONResponse)
async def get_my_courses():
    """Fetches all courses created by the user. """
    course_db = getAllCourses()
    courses = [Course(x) for x in course_db]
    return courses



@app.post("/generate", response_class=HTMLResponse)
async def generate_plan(request: Request, course_topic: str = Form(...), audience_type: str = Form(...)):
    planner = CourseCrew()
    result = planner.kickoff({"course_topic": course_topic, "audience_type": audience_type})
    addCourse({
            "course_title": course_topic,
            "audience_type": audience_type,
            "created_time": datetime.now()
        })
    print("Result:", result)
    # weekly_modules = result.get("weekly_modules", [])
    # for week in weekly_modules:
    #     add_course_modules(week)

    return templates.TemplateResponse("index.html", {"request": request, "result": result})


#get the value from query parameters
@app.post("/course_generation")
async def course_generation(data:CourseRequest):

    """
    Endpoint to generate a course plan based on the provided title and audience type.
    """
    inputs = {
        "course_topic": data.course_title,
        "audience_type": data.audience_type,
        "current_year": str(datetime.now().year)
    }
    print(inputs)
    planner = CourseCrew()
    result = planner.kickoff(inputs)
    # Extract the actual JSON string
    raw_text = result.raw

    # Remove Markdown code block if present (```json\n ... ```)
    if raw_text.startswith("```json"):
        raw_text = raw_text.strip("`").lstrip("json\n").rstrip("`")

    try:
        print("Raw Text:", raw_text)
        parsed_result = json.loads(raw_text)  # Now it's a real dict
       
    except json.JSONDecodeError as e:
        print("Failed to parse JSON:", e)
        return JSONResponse(content={"error": "Invalid JSON from agent"}, status_code=500)
    
    final_result = jsonable_encoder(parsed_result)
    # Save the course data to the database
    course_importer = CourseImporter()
    try:
        course_importer.insert_course_data(final_result)
    except Exception as e:
        print("Failed to insert course data:", e)
        return JSONResponse(content={"error": "Failed to save course data"}, status_code=500)

    return JSONResponse(content=jsonable_encoder(parsed_result), status_code=200)

@app.post("/generate_study_plan")
def generate_study_plan(request: StudyPlanRequest):
    result = CalendarStudyPlanner().generate_plan(
        course_id=request.course_id,
        start_date_str=request.start_date,
        skip_weekends=request.skip_weekends
    )
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


# @app.post("/course_suggestion/")
# async def run_course_plan(request: CourseRequest):
#     inputs = {
#         "subject": request.subject,
#         "course_title": request.course_title,
#         "course_topic": request.course_topic,
#         "audience_type": request.audience_type,
#         "current_year": str(datetime.now().year)
#     }

#     try:
#         course_planner = CourseCrew()
#         result = course_planner.kickoff({
#                 "course_topic": "Generative AI for Beginners",
#                 "audience_type": "Working professionals with no ML background"
#         })
        
#         return {"status": "success", "result": result}
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))
