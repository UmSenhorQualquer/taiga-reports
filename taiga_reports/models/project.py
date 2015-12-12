import pickle, datetime, os

class Project(object):

	def __init__(self, project, datetime):
		self._project    = project
		self._datetime = datetime
		self._filename = None

	def dump(self, folder=None):
		if self._filename:
			filename = self._filename
		else:
			filename = os.path.join(folder, "{0}.proj".format(self._project.id) )
		with open(filename,'wb') as outfile: pickle.dump(self, outfile)

	@staticmethod
	def load(filename):
		with open(filename,'rb') as infile: obj = pickle.load(infile)
		obj._filename = filename
		return obj

	@property
	def name(self): return self._project.name
	

	@property
	def id(self): return self._project.id
	
	@property
	def __unicode__(self): return str(self._project)

	@property
	def __str__(self): return str(self._project)
	