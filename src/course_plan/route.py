from fastapi import FastAPI, HTTPException,Request,Form
from pydantic import BaseModel
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from src.course_plan.crew import CoursePlan
from src.course_plan.course_suggestion import CourseCrew
from src.course_plan.db.util import getCurrentUser, addCourse,getAllCourses, addCourseModules
from src.course_plan.model.user import User,Course
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
    weekly_modules = result.get("weekly_modules", [])
    for week in weekly_modules:
        addCourseModules(week)

    return templates.TemplateResponse("index.html", {"request": request, "result": result})


@app.post("/course_suggestion/")
async def run_course_plan(request: CourseRequest):
    inputs = {
        "subject": request.subject,
        "course_title": request.course_title,
        "course_topic": request.course_topic,
        "audience_type": request.audience_type,
        "current_year": str(datetime.now().year)
    }

    try:
        course_planner = CourseCrew()
        result = course_planner.kickoff({
                "course_topic": "Generative AI for Beginners",
                "audience_type": "Working professionals with no ML background"
        })
        
        return {"status": "success", "result": result}
    except Exception as e:
        print(e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
