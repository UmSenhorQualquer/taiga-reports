import pickle, os, glob
from taiga_stats import tools

class TimeStats(object):

	def __init__(self, folder):
		filespath = os.path.join(folder, '*.dat')
		users_stats = []
		for filename in glob.glob(filespath):
			with open(filename,'rb') as infile:
				user_stats = pickle.load(infile)
				users_stats.append(user_stats)
		self._users_stats = sorted(users_stats, key=lambda x: x.stats_datetime)


	def __calculate_points_data(self):
		times  = {}
		points = {}
		for user_stats in self._users_stats:
			key = user_stats.username
			if key not in points.keys(): times[key], points[key] = [], []
			points[key].append( user_stats.total_points )
			times[key].append( user_stats.stats_datetime )
		return times, points

	def __calculate_projects_data(self):
		times 	 = {}
		projects = {}
		for user_stats in self._users_stats:
			key = user_stats.username
			if key not in projects.keys(): times[key], projects[key] = [], []				
			projects[key].append( user_stats.projects_count )
			times[key].append( user_stats.stats_datetime )
		return times, projects

	def __calculate_stories_data(self):
		times 	= {}
		stories = {}
		for user_stats in self._users_stats:
			key = user_stats.username
			if key not in stories.keys(): times[key], stories[key] = [], []
			stories[key].append( user_stats.total_stories )
			times[key].append( user_stats.stats_datetime )
		return times, stories

	
	def __calculate_tags_counts(self):
		times  = {}
		counts = {}
		for user_stats in self._users_stats:
			username = user_stats.username
			if username not in counts.keys(): 
				counts[username] = {}
				times[username]  = {}
			for tag, count in user_stats.tags_count.items():
				if username not in counts[username].keys(): 
					times[username][tag]  = []
					counts[username][tag] = []

				times[username][tag].append( user_stats.stats_datetime )
				counts[username][tag].append( user_stats.tags_count[tag] )
		return times, counts

	def __calculate_tags_points(self):
		times  = {}
		points = {}
		for user_stats in self._users_stats:
			username = user_stats.username
			if username not in points.keys(): 
				points[username] = {}
				times[username]  = {}
			for tag, count in user_stats.tags_count.items():
				if username not in points[username].keys(): 
					times[username][tag]  = []
					points[username][tag] = []

				times[username][tag].append( user_stats.stats_datetime )
				points[username][tag].append( user_stats.tags_points[tag] )
		return times, points

	def calc_points_overtime_stats(self):
		times, points = self.__calculate_points_data()
		return [(key, times[key], points[key]) for key in times.keys()]

	def calc_stories_overtime_stats(self):
		times, stories = self.__calculate_stories_data()
		return [(key, times[key], stories[key]) for key in times.keys()]

	def calc_projects_overtime_stats(self):
		times, projects = self.__calculate_projects_data()
		return [(key, times[key], projects[key]) for key in times.keys()]
		

	def export_members_stats_graphs(self, folder):
		filename = os.path.join(folder, 'total_points_over_time.png')
		tools.export_graph(filename, self.calc_points_overtime_stats(), title='Points over time')

		filename = os.path.join(folder, 'total_stories_over_time.png')
		tools.export_graph(filename, self.calc_stories_overtime_stats(), title='Stories over time')

		filename = os.path.join(folder, 'total_projects_over_time.png')
		tools.export_graph(filename, self.calc_projects_overtime_stats(), title='Projects over time')


	def export_tags_counts_graphs(self, folder):
		times, tags = self.__calculate_tags_counts()

		for username in times.keys():
			values = []
			for tag in tags[username].keys():
				val = tag, times[username][tag], tags[username][tag]
				values.append( val )
			
			if len(values)>0:
				name = username.lower().replace(' ', '')
				filename = os.path.join(folder, 'tag_count_{0}.png'.format(name) )
				tools.export_graph( filename, values, title='Tags counts for {0}'.format(username) )

	def export_tags_points_graphs(self, folder):
		times, tags = self.__calculate_tags_points()

		for username in times.keys():
			values = []
			for tag in tags[username].keys():
				val = tag, times[username][tag], tags[username][tag]
				values.append( val )
			
			if len(values)>0:
				name = username.lower().replace(' ', '')
				filename = os.path.join(folder, 'tag_points_{0}.png'.format(name) )
				tools.export_graph( filename, values, title='Tags points for {0}'.format(username) )














	def __calculate_status_counts(self):
		times  = {}
		counts = {}
		for user_stats in self._users_stats:
			username = user_stats.username
			if username not in counts.keys(): 
				counts[username] = {}
				times[username]  = {}
			for tag, count in user_stats.stories_status_count.items():
				if username not in counts[username].keys(): 
					times[username][tag]  = []
					counts[username][tag] = []

				times[username][tag].append( user_stats.stats_datetime )
				counts[username][tag].append( user_stats.stories_status_count[tag] )
		return times, counts

	def export_status_counts_graphs(self, folder):
		times, counts = self.__calculate_status_counts()

		for username in times.keys():
			values = []
			for tag in counts[username].keys():
				val = tag, times[username][tag], counts[username][tag]
				values.append( val )
			
			if len(values)>0:
				name = username.lower().replace(' ', '')
				filename = os.path.join(folder, 'status_count_{0}.png'.format(name) )
				tools.export_graph( filename, values, title='Status counts for {0}'.format(username) )

	
	def __calculate_status_points(self):
		times  = {}
		points = {}
		for user_stats in self._users_stats:
			username = user_stats.username
			if username not in points.keys(): 
				points[username] = {}
				times[username]  = {}
			for tag, count in user_stats.stories_status_points.items():
				if username not in points[username].keys(): 
					times[username][tag]  = []
					points[username][tag] = []

				times[username][tag].append( user_stats.stats_datetime )
				points[username][tag].append( user_stats.stories_status_points[tag] )
		return times, points


	def export_status_points_graphs(self, folder):
		times, points = self.__calculate_status_points()

		for username in times.keys():
			values = []
			for tag in points[username].keys():
				val = tag, times[username][tag], points[username][tag]
				values.append( val )
			
			if len(values)>0:
				name = username.lower().replace(' ', '')
				filename = os.path.join(folder, 'status_points_{0}.png'.format(name) )
				tools.export_graph( filename, values, title='Status points for {0}'.format(username) )
