from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
@CrewBase
class Financialresearcher():
	"""Financialresearcher crew"""
	agents_config = 'config/agents.yaml'
	task_config="config/tasks.yaml"

	@agent
	def researcher(self) -> Agent:
		return Agent(config=self.agents_config['researcher_agent'],verbose=True,tools=[SerperDevTool()])
	@agent
	def analyst_agent(self) -> Agent:
		return Agent(config=self.agents_config['analyst_agent'],verbose=True,tools=[SerperDevTool()])
	@task

	def research_task(self) -> Task:
		return Task(config=self.tasks_config['research_task'])
	@task
	def report_task(self) -> Task:
		return Task(config=self.tasks_config['analysis_task'])
	
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)