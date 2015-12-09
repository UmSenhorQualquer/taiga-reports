from taiga_reports.time_stats import TimeStats


stats = TimeStats('../data')
stats.export_members_stats_graphs('../graphs')
stats.export_tags_counts_graphs('../graphs')
stats.export_tags_points_graphs('../graphs')
stats.export_status_counts_graphs('../graphs')
stats.export_status_points_graphs('../graphs')