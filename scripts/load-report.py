import os
from taiga_reports.report import Report
from taiga_reports.user_report import UserReport
from settings import TAGS_PRIORITIES, OUTPUT_FOLDER


report = Report(OUTPUT_FOLDER)

report.save_status_counts_graph('../docs/imgs/status_counts.png', user_id=86960)
report.save_status_points_graph('../docs/imgs/status_points.png', user_id=86960)
report.save_tags_counts_graph('../docs/imgs/tags_counts.png', user_id=86960)
report.save_tags_points_graph('../docs/imgs/tags_points.png', user_id=86960)


user_report = UserReport(86960, report.last_snapshot)

print user_report.status_counts()
print user_report.status_points()
print user_report.tags_counts()
print user_report.tags_points()

user_report.workload_4_next_days(TAGS_PRIORITIES)
user_report.save_workload_4_next_days_graph('../docs/imgs/workload.png', TAGS_PRIORITIES)

