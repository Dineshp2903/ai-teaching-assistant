from crewai import Agent, Task, Crew, Process

class CourseCrew:
    def __init__(self):
        self.agent = self.create_agent()
        self.task = self.create_task()
        self.crew = self.create_crew()

    def create_agent(self) -> Agent:
        return Agent(
            role="Course Designer",
            goal="Design a comprehensive and engaging curriculum tailored to the learner’s goals",
            backstory=(
                "You're an experienced curriculum architect who understands pedagogy and instructional design. "
                "You're skilled in organizing content into structured modules, ensuring each topic builds logically "
                "on the previous one to optimize learning outcomes."
            ),
            verbose=True
        )

    def create_task(self) -> Task:
        return Task(
            description=(
                "Design a structured, engaging week-by-week course syllabus for {course_topic}, "
                "targeting {audience_type}. The syllabus should include modules for each week with subtopics, "
                "learning objectives, recommended activities, tools, and estimated time. output should be a detailed and JSON-serializable format."
            ),
            expected_output=(
                "A weekly course outline for {course_topic} with:\n"
                "- Week Number\n"
                "- Module Title\n"
                "- Key subtopics\n"
                "- Learning objectives\n"
                "- Estimated duration (hours)\n"
                "- Tools/platforms needed\n"
                "- Assignments or hands-on practice\n"
                "- Prerequisites (if any)"
            ),
            agent=self.agent
        )

    def create_crew(self) -> Crew:
        return Crew(
            agents=[self.agent],
            tasks=[self.task],
            process=Process.sequential,
            verbose=True
        )

    def kickoff(self, inputs: dict):
        return self.crew.kickoff(inputs)