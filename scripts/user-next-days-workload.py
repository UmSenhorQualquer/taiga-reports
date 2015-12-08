import os
from taiga import TaigaAPI
from settings import USER, PASS, TEAM, TAGS_PRIORITIES, USER_WORKING_DAYS
from datetime import date
from taiga_stats.user_stats import UserStats

api = TaigaAPI()
api.auth(username=USER, password=PASS)

user_stats = UserStats(api, 85475, 
	stories_status=['New', 'Ready', 'In progress', 'Ready for test'],
	tags=[tag for tag, _ in TAGS_PRIORITIES])


print user_stats

#user_stats.predict_work(PRIORITY_TAGS, USER_WORKING_DAYS[85475])


filename = os.path.join('graphs', 'workload_for_the_next_days.png')
user_stats.export_next_days_workload(
	filename, hours_per_day=8
)
