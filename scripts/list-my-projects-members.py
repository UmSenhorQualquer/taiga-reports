from taiga import TaigaAPI
from settings import USER, PASS, TEAM

api = TaigaAPI()
api.auth( username=USER, password=PASS)

me = api.me()

#projects = api.projects.list(member=me.id)
projects = api.projects.list(member=TEAM)
for project in projects:
	print 'Project ', project.name, ', members ids', project.members