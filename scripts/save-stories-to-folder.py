import datetime, pickle, os
from taiga import TaigaAPI
from settings import USER, PASS, TEAM
from taiga_reports.moment import Moment

folder = '~/xxx'

api = TaigaAPI(); 
api.auth( username=USER, password=PASS)

SingleMomentReport.take_snapshot(api, folder, TEAM)
				
		