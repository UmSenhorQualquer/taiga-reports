import os, glob, datetime
from dateutil import parser
from taiga_reports.models.project import Project
from taiga_reports.models.user_story import UserStory
from taiga_reports.models.status import Status
from taiga_reports import tools
from matplotlib import pyplot as plt

class Stats(object):

	def __init__(self):
		self._datetime = None
		self._projects = []
		self._status   = []
		self._stories  = []

	

	def status_counts(self, no_closed=True, stories=None):
		status_counts = {}
		for story in self._stories.values():
			if no_closed==story.is_closed: continue
			points = story.total_points if story.total_points!=None else 0
			status  = self._status[story.status]
			if status.name not in status_counts.keys(): status_counts[status.name] = 0
			status_counts[status.name] += 1
		return status_counts


	def status_points(self, no_closed=True, stories=None):
		status_points = {}
		for story in self._stories.values():
			if no_closed==story.is_closed: continue
			points = story.total_points if story.total_points!=None else 0
			status  = self._status[story.status]
			if status.name not in status_points.keys(): status_points[status.name] = 0
			status_points[status.name] += points
		return status_points

	def tags_counts(self, no_closed=True, stories=None):
		tags_counts = {'None':0}
		for story in self._stories.values():
			if no_closed==story.is_closed: continue
			points = story.total_points if story.total_points!=None else 0
			if len(story.tags)>0:
				for tag in story.tags:
					if tag not in tags_counts.keys(): tags_counts[tag] = 0
					tags_counts[tag] += 1
			else:
				tags_counts['None'] += 1
		return tags_counts


	def tags_points(self, no_closed=True):
		tags_points = {'None':0}
		for story in self._stories.values():
			if no_closed==story.is_closed: continue
			points = story.total_points if story.total_points!=None else 0
			if len(story.tags)>0:
				for tag in story.tags:
					if tag not in tags_points.keys(): tags_points[tag] = 0
					tags_points[tag] += points
			else:
				tags_points['None'] += points
		return tags_points

	
	@property
	def status(self): return self._status.values()


	def workload_4_next_days(self, priorities, working_days=None, hours_per_day=8):
		"""
		Finds the workload for the next days, until the it is lower than the working hours per day
		The estimation of the workload of lower priority stories includes the points of the most priority stories.
		"""
		working_days = working_days if working_days else tools.default_working_days()
		tags_points_results = self.tags_points()

		times 		= [] #List of working days
		tags_points = {}
		tags 		= [tag for tag, priority in sorted(priorities,key=lambda x:x[1]) if tag in tags_points_results.keys()]
		tags.append('None')
		total_pts = {}
		points_sum = 0

		#Calculates the first day points for each tag
		for tag in tags:
			points_sum += tags_points_results[tag]
			total_pts[tag] = points_sum

		#Iterates each working day until the number of points remaining 
		#is lower than the number of working hours per day
		
		for date in working_days:
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

	def save_workload_4_next_days_graph(self, filename,
			priorities, working_days=None, hours_per_day=8, title=None):
		"""
		Generates a graph with the workload vs next working days
		"""
		times, tags_points = self.workload_4_next_days(priorities, working_days, hours_per_day)

		tags =  ['None']
		tags += [tag for tag, priority in sorted(priorities,key=lambda x:-x[1]) if tag in tags_points.keys()]
		
		values = []

		for tag in tags: values.append( (tag, times[:len(tags_points[tag])], tags_points[tag]) )
		
		if len(values)>0: 
			tools.generate_graph(values, title=title, fill=True )
		
			working_hours = [hours_per_day for time in times]
			plt.plot(times, working_hours, alpha=0.3, marker='o', color='black', label='Working hours')
			plt.legend(loc=1)
			plt.savefig(filename)