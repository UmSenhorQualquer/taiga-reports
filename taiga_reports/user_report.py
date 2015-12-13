from taiga_reports.stats import Stats


class UserReport(Stats):

	def __init__(self, user_id, snapshot):
		self._user_id = user_id
		self._datetime = snapshot._datetime
		self.__filter(snapshot)


	def __filter(self, snapshot):
		self._stories  = {}
		self._status   = {}
		self._projects = {}

		for story in snapshot._stories.values():
			if self._user_id == story.assigned_to:
				self._stories[story.id] = story

		for proj in snapshot._projects.values():
			self._projects[proj.id] = proj

		for status in snapshot._status.values():
			self._status[status.id] = status

