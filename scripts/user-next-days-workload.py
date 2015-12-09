import os
from taiga import TaigaAPI
from settings import USER, PASS, TEAM, TAGS_PRIORITIES
from datetime import date
from taiga_reports.user_stats import UserStats

api = TaigaAPI()
api.auth(username=USER, password=PASS)

user_stats = UserStats(api, TEAM[0], 
	stories_status=['New', 'Ready', 'In progress', 'Ready for test'],
	tags_priorities=TAGS_PRIORITIES)


print user_stats


filename = os.path.join('../graphs', 'workload_for_the_next_days.png')
user_stats.export_next_days_workload(
	filename, hours_per_day=8
)
