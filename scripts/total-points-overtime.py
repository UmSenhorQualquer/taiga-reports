from settings import TAGS_PRIORITIES
from taiga_reports.time_stats import TimeStats


TAGS = [tag for tag, _ in sorted(TAGS_PRIORITIES, key=lambda x:-x[1])]

stats = TimeStats('../data')
stats.export_members_stats_graphs('../graphs')
stats.export_tags_counts_graphs('../graphs', TAGS)
stats.export_tags_points_graphs('../graphs', TAGS)
stats.export_status_counts_graphs('../graphs')
stats.export_status_points_graphs('../graphs')