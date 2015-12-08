from taiga import TaigaAPI
from settings import USER, PASS

api = TaigaAPI()
api.auth( username=USER, password=PASS)
me = api.me()

projects = api.projects.list(member=me.id)
for project in projects:
	print '- updating roles for:', project.name
	for role in project.list_roles():
		if role.name=='UX': 	role.name = 'Requirements gathering'
		if role.name=='Design': role.name = 'Meeting'
		if role.name=='Front': 	role.name = 'Development'
		if role.name=='Back': 	role.name = 'Maintenance'

		if role.name in ['Maintenance', 'Development', 'Meeting', 'Requirements gathering']: 
			role.update(project=project.id)