import os
from taiga import TaigaAPI
from settings import USER, PASS, TEAM, TAGS_PRIORITIES
from datetime import date
from taiga_stats.team_stats import TeamStats

api = TaigaAPI()
api.auth(username=USER, password=PASS)

output_filename = 'stats-per-team-member.dat'
out_file_path = os.path.join('data', output_filename)

team_stats = TeamStats(api, TEAM, 
	stories_status=['New', 'Ready', 'In progress', 'Ready for test'],
	tags_priorities=TAGS_PRIORITIES)

#print team_stats
print team_stats.not_assigned_stories()

team_stats.dump_to_folder('../data')