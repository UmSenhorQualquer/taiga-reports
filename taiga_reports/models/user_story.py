import pickle, datetime, os

class UserStory(object):

	def __init__(self, user_story, datetime):
		self._story    = user_story
		self._datetime = datetime
		self._filename = None

	def dump(self, folder=None):
		if self._filename:
			filename = self._filename
		else:
			filename = os.path.join(folder, "{0}.story".format(self._story.id) )
		with open(filename,'wb') as outfile: pickle.dump(self, outfile)

	@staticmethod
	def load(filename):
		with open(filename,'rb') as infile: obj = pickle.load(infile)
		obj._filename = filename
		return obj


	@property
	def id(self): return self._story.id
	
	@property
	def status(self): return self._story.status

	@property
	def tags(self): return self._story.tags

	@property
	def assigned_to(self): return self._story.assigned_to


	@property
	def total_points(self): return self._story.total_points
	
	@property
	def is_closed(self): return self._story.is_closed

	@property
	def project(self): return self._story.project

	@property
	def subject(self): return self._story.subject	


	@property
	def __unicode__(self): return str(self._story)

	@property
	def __str__(self): return str(self._story)
	