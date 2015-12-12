import pickle, datetime, os

class Status(object):

	def __init__(self, status, datetime):
		self._status   = status
		self._datetime = datetime
		self._filename = None

	def dump(self, folder=None):
		if self._filename:
			filename = self._filename
		else:
			filename = os.path.join(folder, "{0}.status".format(self.id) )
		with open(filename,'wb') as outfile: pickle.dump(self, outfile)

	@staticmethod
	def load(filename):
		with open(filename,'rb') as infile: obj = pickle.load(infile)
		obj._filename = filename
		return obj


	@property
	def id(self): return self._status.id
	
	@property
	def __unicode__(self): return str(self._status)

	@property
	def __str__(self): return str(self._status)
	

	@property
	def name(self): return self._status.name
	