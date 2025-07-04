class User:
    def __init__(self,user :tuple):
        self.id = user[0]
        self.name = user[1]
        self.email = user[2]
        self.style = user[3] if len(user) > 3 else "Hands-on"
    
    def getUserName(self):
        return self.name
    
    def getUserEmail(self):
        return self.email
    def getUserStyle(self):
        return self.style
    
class Course:
    def __init__(self, course:dict):
        self.course_id = course["course_id"]
        self.course_title = course["course_title"]
        self.audience_type = course["audience_type"]
        self.created_time = course["created_time"]

    
    def getCourseId(self):
        return self.course_id
    
    def getCourseTitle(self):
        return self.course_title
    
    def getAudienceType(self):
        return self.audience_type
    
    def getCreatedTime(self):
        return self.created_time
    

from typing import List, Union
from datetime import datetime

class CourseModule:
    def __init__(self, module: dict):
        self.module_id = module.get("module_id")
        self.course_id = module.get("course_id")
        self.course_title = module.get("course_title")
        self.week = module.get("week")
        self.module_title = module.get("module_title")
        self.duration = module.get("duration")
        self.subtopics = module.get("subtopics", [])
        self.learning_objectives = module.get("learning_objectives", [])
        self.tools = module.get("tools", [])
        self.assignments = module.get("assignments", [])
        self.prerequisites = module.get("prerequisites", [])

    # Getters
    def getModuleId(self) -> Union[int, None]:
        return self.module_id

    def getCourseId(self) -> int:
        return self.course_id

    def getCourseTitle(self) -> str:
        return self.course_title

    def getWeek(self) -> int:
        return self.week

    def getModuleTitle(self) -> str:
        return self.module_title

    def getDuration(self) -> int:
        return self.duration

    def getSubtopics(self) -> List[str]:
        return self.subtopics

    def getLearningObjectives(self) -> List[str]:
        return self.learning_objectives

    def getTools(self) -> List[str]:
        return self.tools

    def getAssignments(self) -> List[str]:
        return self.assignments

    def getPrerequisites(self) -> List[str]:
        return self.prerequisites