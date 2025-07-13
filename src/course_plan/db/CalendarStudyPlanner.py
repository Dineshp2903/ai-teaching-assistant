import psycopg2
from datetime import datetime, timedelta
from src.course_plan.db.connection import get_db_config
from typing import Dict

class CalendarStudyPlanner:
    def __init__(self):
        self.db_config = get_db_config()

    def generate_plan(self, course_id: int, start_date_str: str, skip_weekends: bool = True):
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cur:
                    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

                    # Fetch all modules for the course
                    cur.execute("""
                        SELECT module_id, week, estimated_duration_hours
                        FROM modules
                        WHERE course_id = %s
                        ORDER BY week
                    """, (course_id,))
                    modules = cur.fetchall()

                    for module_id, week, duration in modules:
                        week_start_date = start_date + timedelta(weeks=(week - 1))
                        current_date = week_start_date

                        # Get subtopics for the module
                        cur.execute("""
                            SELECT subtopic FROM subtopics
                            WHERE module_id = %s
                        """, (module_id,))
                        subtopics = cur.fetchall()

                        if not subtopics:
                            continue

                        time_per_topic = round(duration / len(subtopics), 2)

                        for sub in subtopics:
                            # Skip weekends
                            while skip_weekends and current_date.weekday() >= 5:
                                current_date += timedelta(days=1)

                            # Insert into calendar_study_plan
                            cur.execute("""
                                INSERT INTO calendar_study_plan (
                                    course_id, module_id, subtopic,
                                    scheduled_date, estimated_time_hours
                                )
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                course_id,
                                module_id,
                                sub[0],
                                current_date,
                                time_per_topic
                            ))

                            current_date += timedelta(days=1)

                conn.commit()
                return {"message": "Study plan created successfully!"}

        except Exception as e:
            return {"error": str(e)}
