import datetime, pickle, os
from taiga import TaigaAPI
from settings import USER, PASS, TEAM, OUTPUT_FOLDER
from taiga_reports.snapshot import Snapshot

api = TaigaAPI(); api.auth( username=USER, password=PASS)

Snapshot(OUTPUT_FOLDER,api,TEAM)