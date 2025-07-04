from src.course_plan.db.connection import get_db_connection, close_db_connection
from datetime import datetime



def getCurrentUser():
    """
    Returns the current user from the request context.
    This function is used to retrieve the user information from the request context.
    """
    curson = get_db_connection()
    print("curson", curson)
    if curson is None:
        return None # Handle the case where the database connection could not be established 
    else:
        try:
            curson.execute("SELECT * FROM users WHERE id = %s", (2,))  # Example query to get user with ID 1
            user = curson.fetchone()
            return user
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None
        finally:
            close_db_connection(curson)

def addCourse(course_data):
    """
    Adds a new course to the database.
    :param course_data: Dictionary containing course details.
    :return: True if the course was added successfully, False otherwise.
    """
    print("Adding course with data:", course_data)
    curson = get_db_connection()
    if curson is None:
        return False  # Handle the case where the database connection could not be established
    try:
        curson.execute(
            "INSERT INTO courseplanner (course_title, audience_type, created_time) VALUES (%s, %s, %s) RETURNING course_id",
            (course_data['course_title'], course_data['audience_type'], datetime.now())
        )
        course_id = curson.fetchone()[0]
        print(f"Course added with ID: {course_id}")
        curson.connection.commit()  # Commit the transaction
         # Optionally, you can return the course_id or any other relevant information
         # return course_id
        return True
    except Exception as e:
        print(f"Error adding course: {e}")
        return False
    finally:
        close_db_connection(curson)

def getAllCourses():
    """
    Retrieves all courses from the database.
    :return: List of dictionaries containing course details.
    """
    curson = get_db_connection()
    if curson is None:
        return []  # Handle the case where the database connection could not be established
    try:
        curson.execute("SELECT * FROM courseplanner")
        courses = curson.fetchall()
        print(f"Fetched {len(courses)} courses from the database. {courses}")

        return [dict(zip(("course_id","course_title","audience_type","created_time"),course)) for course in courses]  # Convert tuples to dictionaries
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return []
    finally:
        close_db_connection(curson)
    