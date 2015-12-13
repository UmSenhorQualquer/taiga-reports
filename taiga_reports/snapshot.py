import os, glob, datetime
from dateutil import parser
from taiga_reports.models.project import Project
from taiga_reports.models.user_story import UserStory
from taiga_reports.models.status import Status
from taiga_reports import tools
from matplotlib import pyplot as plt
from taiga_reports.stats import Stats

class Snapshot(Stats):

	def __init__(self, folder, api=None, team=None):
		if api==None or team==None:
			directory_name = os.path.basename(folder)
			self._datetime = parser.parse(directory_name)
			self.__load_data(folder)
		else:
			Snapshot.take_snapshot(api, folder, team)

	@staticmethod
	def take_snapshot(api, folder, team_members):
		#Create a folder
		current_time = datetime.datetime.now()
		time_string = str(datetime.datetime.now())
		output_folder = os.path.join(folder, time_string)
		os.mkdir(output_folder)

		projects = api.projects.list(member=team_members)

		for proj in projects:
			project = Project(proj, current_time)
			project.dump(output_folder)

			for st in api.user_stories.list(project=project.id):
				story = UserStory(st, current_time)
				story.dump(output_folder)

			for st in api.user_story_statuses.list(project=project.id):
				status = Status(st, current_time)
				status.dump(output_folder)
						
	def __load_data(self, folder):
		self._stories = {}
		self._status = {}
		self._projects = {}

		for filename in glob.glob(os.path.join(folder, '*.story')):
			story = UserStory.load(filename)
			self._stories[story.id] = story

		for filename in glob.glob(os.path.join(folder, '*.proj')):
			proj = Project.load(filename)
			self._projects[proj.id] = proj

		for filename in glob.glob(os.path.join(folder, '*.status')):
			status = Status.load(filename)
			self._status[status.id] = status


	def not_assigned_stories(self):
		return [ (self._projects[story.project], story) for story in self._stories.values() if not story.assigned_to]
