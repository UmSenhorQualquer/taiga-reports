import os
from taiga_reports.overtime_report import OvertimeReport
from taiga_reports.user_report import UserReport
from settings import TAGS_PRIORITIES


folder = '~/xxx'

report = OvertimeReport(folder)


report.save_status_counts_graph('status.png', user_id=87239)
report.save_tags_points_graph('tags.png')

last_moment = report.last_moment
user_report = UserReport(86960, last_moment)
user_report.save_workload_4_next_days_graph('teste.png', TAGS_PRIORITIES)
