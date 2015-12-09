import os
from taiga import TaigaAPI
from settings import USER, PASS, TEAM, TAGS_PRIORITIES
from datetime import date
from taiga_reports.team_stats import TeamStats

api = TaigaAPI()
api.auth(username=USER, password=PASS)

team_stats = TeamStats(api, TEAM, 
	stories_status=['New', 'Ready', 'In progress', 'Ready for test'],
	tags_priorities=TAGS_PRIORITIES)

team_stats.dump_to_folder( os.path.join('..','data') )