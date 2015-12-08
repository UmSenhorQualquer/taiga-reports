from taiga import TaigaAPI
from settings import USER, PASS

api = TaigaAPI()
api.auth( username=USER, password=PASS)

me = api.me()

projects = api.projects.list(member=me.id)
for project in projects: print project.name