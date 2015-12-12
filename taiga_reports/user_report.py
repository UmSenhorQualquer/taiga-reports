from taiga_reports.single_moment_report import SingleMomentReport


class UserReport(SingleMomentReport):

	def __init__(self, user_id, single_moment_report):
		self._user_id = user_id
		self._datetime = single_moment_report._datetime

		self.__filter(single_moment_report)




	def __filter(self, single_moment_report):
		self._stories = {}
		self._status = {}
		self._projects = {}

		for story in single_moment_report._stories.values():
			if self._user_id == story.assigned_to:
				self._stories[story.id] = story

		for proj in single_moment_report._projects.values():
			self._projects[proj.id] = proj

		for status in single_moment_report._status.values():
			self._status[status.id] = status

