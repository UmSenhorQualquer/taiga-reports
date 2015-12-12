import time, pickle, os
from datetime import datetime
from taiga_reports import tools
from matplotlib import pyplot as plt

class UserStats(object):
	"""
	Stores the stats of an user
	"""

	def __init__(self, api, user_id, story_is_closed='false', 
		stories_status=[], tags_priorities=[], working_days=None):
		self.user_id = user_id					#User id
		self.user 	 = api.users.get(user_id)	#Taiga API user model
		self.api 	 = api 						#Taiga API object
		self.working_days    = working_days if working_days else tools.default_working_days()
		self.tags_priorities = tags_priorities
		
		
		self.calculate_stats(story_is_closed, stories_status)

	def calculate_stats(self, 
			story_is_closed='false', 
			stories_status=[],
			filter_by_status=None):
		"""
		Retrieve the user data and calculate some stats
		"""
		self.total_points  		= 0				 #Total points the user has allocated to him
		self.total_stories 		= 0				 #Total number of stories the user has allocated to him
		self.stories_projects 	= []			 #List of the stories projects
		self.stats_datetime		= datetime.now() #Date when the information was retrieve
		
		self.tags_count	 = {'':0} #Tags stats
		self.tags_points = {'':0} #Tags stats

		self.stories_status_count  = {} #Status stats
		self.stories_status_points = {} #Status stats

		
		for t in self.api.user_stories.list(assigned_to=self.user_id, is_closed=story_is_closed): 
			
			#Filter stories by the status
			if filter_by_status:
				status = self.api.user_story_statuses.get(t.status)
				#Do not stats if not included in the allowed status list
				if status.name not in filter_by_status: continue


			points = t.total_points if t.total_points!=None else 0 #In case the points are not defined use 0

			#Count the stories, sum the points, and store the stories' projects.
			self.total_points  += points
			self.total_stories += 1
			self.stories_projects.append( t.project )

			#If we want some stats for stories status
			if len(stories_status)>0:
				status = self.api.user_story_statuses.get(t.status)

				if status.name in stories_status: 
					if status.name not in self.stories_status_points.keys(): 
						self.stories_status_points[status.name] = 0
						self.stories_status_count[status.name]  = 0
					self.stories_status_points[status.name] += points
					self.stories_status_count[status.name]  += 1

			#If we want some stats for stories tags
			if len(t.tags):
				storie_tags = map(lambda x:x.lower(), t.tags)
				for tag in storie_tags:
					if tag.lower() in storie_tags:
						if tag.lower() not in self.tags_points:
							self.tags_points[tag] = 0
							self.tags_count[tag]  = 0
						self.tags_points[tag] += points
						self.tags_count[tag]  += 1
			else:
				self.tags_points[''] += points
				self.tags_count['']  += 1

	
	@property
	def username(self): 
		return (self.user.full_name if self.user.full_name!='' else self.user.username)

	@property
	def projects(self): 
		"""
		A list of projects to which the user is member of.
		"""
		return list(set(self.stories_projects))

	@property
	def projects_count(self): 
		"""
		The number of projects to which the user is member of.
		"""
		return len(self.projects)

	def dump_to_folder(self, folder):
		"""
		Save the object to a folder
		"""
		if not os.path.exists(folder): os.makedirs(folder)

		timename = time.strftime("%Y%m%d-%H%M%S")
		filename = os.path.join(folder, "{0}-{1}.dat".format(self.user.id,timename) )
		with open(filename,'wb') as outfile: pickle.dump(self, outfile)


	def next_days_workload(self, hours_per_day=8):
		"""
		Finds the workload for the next days, until the it is lower than the working hours per day
		The estimation of the workload of lower priority stories includes the points of the most priority stories.
		"""
		times 		= [] #List of working days
		tags_points = {} 
		tags 		= [tag for tag, priority in sorted(self.tags_priorities,key=lambda x:x[1]) if tag in self.tags_points.keys()]
		tags.append('')
		total_pts = {}
		points_sum = 0

		#Calculates the first day points for each tag
		for tag in tags:
			points_sum += self.tags_points[tag]
			total_pts[tag] = points_sum

		#Iterates each working day until the number of points remaining 
		#is lower than the number of working hours per day
		
		for date in self.working_days:
			times.append(date)

			for tag in tags:
				if tag not in total_pts.keys(): continue

				if tag not in tags_points.keys():  
					tags_points[tag] = [  ]
					remaining_hours = total_pts[tag]
				else:
					remaining_hours = tags_points[tag][-1]-hours_per_day
				if remaining_hours<0: remaining_hours = 0

				tags_points[tag].append( remaining_hours )
				if tags_points[tag][-1]<hours_per_day:
					tags.remove(tag)
					break

			if len(tags)==0: break

		return times, tags_points


	def export_next_days_workload(self, filename, 
		hours_per_day=8, title='Workload for the next days'):
		"""
		Generates a graph with the workload vs next working days
		"""
		
		times, tags_points = self.next_days_workload(hours_per_day)

		tags =  ['']
		tags += [tag for tag, priority in sorted(self.tags_priorities,key=lambda x:-x[1]) if tag in self.tags_points.keys()]
		
		values = []

		for tag in tags: values.append( (tag, times[:len(tags_points[tag])], tags_points[tag]) )
		
		if len(values)>0: 
			tools.generate_graph(values, title=title, fill=True )
		
			working_hours = [hours_per_day for time in times]
			plt.plot(times, working_hours, alpha=0.3, marker='o', color='black', label='Working hours')
			plt.legend(loc=9, bbox_to_anchor=(0.5,0))
			plt.savefig(filename)




	def __unicode__(self): 

		out = "==========================================================\n"
		out+= "| Stats for: " + self.username.ljust(44) + '|\n'
		out+= "==========================================================\n"
		out+= "| Total points:\t\t"	+str(self.total_points).ljust(37)   + "|\n"
		out+= "| Total stories:\t" 	+str(self.total_stories).ljust(37)  + "|\n"
		out+= "| Total projects:\t" +str(self.projects_count).ljust(37) + "|\n"

		if len(self.tags_count):
			out+= "|--------------------------------------------------------|\n"
			out+= "|                       Tags stats                       |\n"
			out+= "|--------------------------------------------------------|\n"
			for tagname in self.tags_count.keys():
				out += '| '
				out += tagname.ljust(20)
				out += "points: " + str(self.tags_points[tagname]).ljust(10)
				out += "| count: " + str(self.tags_count[tagname]).ljust(8)
				out += '|\n'
		if len(self.stories_status_count):
			out+= "|--------------------------------------------------------|\n"
			out+= "|                     Stories status                     |\n"
			out+= "|--------------------------------------------------------|\n"
			for tagname in self.stories_status_count.keys():
				out += '| '
				out += tagname.ljust(20)
				out += "points: " + str(self.stories_status_points[tagname]).ljust(10)
				out += "| count: " + str(self.stories_status_count[tagname]).ljust(8)
				out += '|\n'

		times, tags_points = self.next_days_workload(8)
		if len(times)>0:
			out+= "|--------------------------------------------------------|\n"
			out+= "|               Available on for stories                 |\n"
			out+= "|--------------------------------------------------------|\n"
			tags = [tag for tag, priority in sorted(self.tags_priorities,key=lambda x:x[1]) if tag in tags_points.keys()]
			tags.append('')
		
			for tagname in tags:
				out += '| '
				name = 'None' if len(tagname)==0 else tagname
				out += name.ljust(25)
				available_date = times[len(tags_points[tagname])-1]
				out += available_date.strftime("%d-%m-%Y").ljust(30)
				out += '|\n'

		out+= "==========================================================\n"

		return out

	def __str__(self): return self.__unicode__()