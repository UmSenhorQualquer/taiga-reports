from taiga_reports.user_stats import UserStats

class TeamStats(object):

	def __init__(self, api, team_users, 
		story_is_closed='false', 
		stories_status=[], tags_priorities=[]):
		"""
		Calculate team stats
		"""
		self.api = api
		self.team_users_ids = team_users
		self.users_stats = []

		for user_id in team_users:
			user_stats = UserStats(api, user_id, 
				story_is_closed=story_is_closed,
				stories_status=stories_status,
				tags_priorities=tags_priorities)
			self.users_stats.append(user_stats)



	def not_assigned_stories(self):
		"""
		Returns the not assigned stories
		"""
		projects = self.api.projects.list(member=self.team_users_ids)

		not_assigned = []
		for project in projects:

			for t in self.api.user_stories.list(
				project=project.id, is_closed=None):
				if not t.assigned_to:
					not_assigned.append( (project, t) )
		return not_assigned
		

	def print_not_assigned_stories(self):
		not_assigned = self.not_assigned_stories()

		print('='*80)
		print('| NOT ASSIGNED STORIES'.ljust(79)+'|')
		print('='*80)
		print('| Project'.ljust(40) + ' | ' + 'Story'.ljust(35) + ' |' )
		print('|'+'-'*78+'|')
		for project, story in not_assigned:
			print('| ' +project.name.ljust(38) + ' | ' + story.subject.ljust(35) + ' |' )
		print('='*80)
		











	def __str__(self): return self.__unicode__()

	def __unicode__(self):
		out = ''

		total_points  		= 0
		total_stories 		= 0
		stories_projects 	= []
		tags_count 	= {}
		tags_points = {}
		stories_status_count  = {}
		stories_status_points = {}
		
		for user_stats in self.users_stats:
			total_points += user_stats.total_points
			total_stories += user_stats.total_stories
			stories_projects.append(user_stats.projects)

			for tagname in user_stats.tags_count.keys():
				if tagname not in tags_count.keys(): 
						tags_count[tagname]  = 0
						tags_points[tagname] = 0

				tags_count[tagname] += user_stats.tags_count[tagname]
				tags_points[tagname] += user_stats.tags_points[tagname]


			for tagname in user_stats.stories_status_count.keys():
				if tagname not in stories_status_count.keys(): 
						stories_status_count[tagname]  = 0
						stories_status_points[tagname] = 0

				stories_status_count[tagname]  += user_stats.stories_status_count[tagname]
				stories_status_points[tagname] += user_stats.stories_status_points[tagname]

		out = "==========================================================\n"
		out+= "| Team stats                                             |\n"
		out+= "==========================================================\n"
		out+= "| Total points:\t\t"	+str(total_points).ljust(37)   + "|\n"
		out+= "| Total stories:\t" 	+str(total_stories).ljust(37)  + "|\n"
		out+= "| Total projects:\t" +str(len(stories_projects)).ljust(37) + "|\n"
		
		if len(tags_count):
			out+= "|--------------------------------------------------------|\n"
			out+= "|                       Tags stats                       |\n"
			out+= "|--------------------------------------------------------|\n"
			for tagname in tags_count.keys():
				out += '| '
				out += tagname.ljust(20)
				out += "points: " + str(tags_points[tagname]).ljust(10)
				out += "| count: " + str(tags_count[tagname]).ljust(8)
				out += '|\n'
		if len(stories_status_count):
			out+= "|--------------------------------------------------------|\n"
			out+= "|                     Stories status                     |\n"
			out+= "|--------------------------------------------------------|\n"
			for tagname in stories_status_count.keys():
				out += '| '
				out += tagname.ljust(20)
				out += "points: " + str(stories_status_points[tagname]).ljust(10)
				out += "| count: " + str(stories_status_count[tagname]).ljust(8)
				out += '|\n'
		out+= "==========================================================\n"

		
		out += '\n'

		for user_stats in self.users_stats:
			out += str(user_stats)
			out += '\n'

		return out


	def dump_to_folder(self, folder):
		for user_stats in self.users_stats: user_stats.dump_to_folder(folder)

