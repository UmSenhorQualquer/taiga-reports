from taiga import TaigaAPI
from settings import USER, PASS

api = TaigaAPI()
api.auth( username=USER, password=PASS)

me = api.me()

#Search for the members of all your projects
members = []
projects = api.projects.list(member=me.id)
for project in projects: 
	members += project.members

#Get the username of the members
for user_id in list(set(members)):
	user = api.users.get(user_id)
	print "({1}) {0}".format(user.username, user.id)