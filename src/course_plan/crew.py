from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
import time

@CrewBase
class CoursePlan():
    """CoursePlan crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def course_designer(self) -> Agent:
        return Agent(
            config=self.agents_config['course_designer'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def subject_matter_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['subject_matter_expert'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def learning_path_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['learning_path_analyst'],  # type: ignore[index]
            verbose=True
        )
    
    @agent
    def tech_stack_advisor(self) -> Agent:
        return Agent(
            config=self.agents_config['tech_stack_advisor'],  # type: ignore[index]
            verbose=True
        )

    @agent
    def course_feedback_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['course_feedback_analyst'],  # type: ignore[index]
            verbose=True
        )


    @task
    def course_design_task(self) -> Task:
        return Task(
            config=self.tasks_config['course_design_task'],  # type: ignore[index]
            # output_file='course_design_report.md'  # Optional output file
        )
    
    @task
    def content_validation_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_validation_task'],  # type: ignore[index]
            output_file='content_validation_report.md'
        )
    
    @task
    def tech_stack_selection_task(self) -> Task:
        time.sleep(5)  # Add delay before task setup
        return Task(
            config=self.tasks_config['tech_stack_selection_task'],  # type: ignore[index]
            output_file='tech_stack_report.md'
        )

    # @task
    # def learning_path_task(self) -> Task:
    #     time.sleep(60)  # Add delay before task setup
    #     return Task(
    #         config=self.tasks_config['learning_path_task'],  # type: ignore[index]
    #         output_file='learning_path_report.md'
    #     )
  

    @task
    def feedback_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['feedback_analysis_task'],  # type: ignore[index]
            output_file='feedback_analysis_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CoursePlan crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical,  # Alternative process model
        )
