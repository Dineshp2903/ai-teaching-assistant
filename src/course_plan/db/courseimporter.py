import psycopg2
import json
from src.course_plan.db.connection import get_db_config
import traceback

class CourseImporter:
    def __init__(self):
        self.db_config = get_db_config()

    def insert_course_data(self, course_json: dict):
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    # Extract title and description from JSON or use defaults
                    course_title = course_json.get("course_title", "Untitled Course")
                    course_description = course_json.get("courseDescription", "No description provided.")

                    # Insert course
                    cursor.execute("""
                        INSERT INTO courses (course_title, course_description)
                        VALUES (%s, %s)
                        RETURNING course_id
                    """, (course_title, course_description))
                    course_id = cursor.fetchone()[0]
                    print(f"✅ Inserted course_id: {course_id}")

                    # Loop through modules
                    for module in course_json["weekly_modules"]:
                        cursor.execute("""
                            INSERT INTO modules (course_id, week, module_title, estimated_duration_hours)
                            VALUES (%s, %s, %s, %s)
                            RETURNING module_id
                        """, (
                            course_id,
                            module["week"],
                            module["module_title"],
                            module["estimated_duration_hours"]
                        ))
                        module_id = cursor.fetchone()[0]

                        # Insert subtopics
                        for sub in module.get("subtopics", []):
                            cursor.execute("""
                                INSERT INTO subtopics (module_id, subtopic)
                                VALUES (%s, %s)
                            """, (module_id, sub))

                        # Insert learning objectives
                        for obj in module.get("learning_objectives", []):
                            cursor.execute("""
                                INSERT INTO learning_objectives (module_id, objective)
                                VALUES (%s, %s)
                            """, (module_id, obj))

                        # Insert tools
                        for tool in module.get("tools_required", []):
                            cursor.execute("""
                                INSERT INTO tools_required (module_id, tool_name)
                                VALUES (%s, %s)
                            """, (module_id, tool))

                        # Insert assignments
                        for assignment in module.get("assignments", []):
                            cursor.execute("""
                                INSERT INTO assignments (module_id, assignment)
                                VALUES (%s, %s)
                            """, (module_id, assignment))

                        # Insert prerequisites
                        for prereq in module.get("prerequisites", []):
                            cursor.execute("""
                                INSERT INTO prerequisites (module_id, prerequisite)
                                VALUES (%s, %s)
                            """, (module_id, prereq))

                    conn.commit()
                    print("✅ All course data inserted successfully!")

        except Exception as e:
            print("❌ Error inserting data:", e)
            traceback.print_exc()
            raise e  # Re-raise the exception for further handling if needed
