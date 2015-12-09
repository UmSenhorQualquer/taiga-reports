# Taiga reports

The generates reports for taiga.io:
- Generats stats for developers individually or for a team:
	- Number of stories per tag.
	- Total points per tag.
	- Number of stories per story status.
	- Total points per story status.
- Workload for the next days for each user.
- Stories with no assigned users.
- Progression graphs by tags and stories status.

## Examples

### Workload for the next days

![Prediction example](graphs/workload_for_the_next_days.png?raw=true "Screen")

### Stats example

```bash
==========================================================
| Team stats                                             |
==========================================================
| Total points:		113.0                                |
| Total stories:	17                                   |
| Total projects:	3                                    |
|--------------------------------------------------------|
|                       Tags stats                       |
|--------------------------------------------------------|
| urgent              points: 20.0      | count: 1       |
| no-tags             points: 314.0     | count: 49      |
| important           points: 5.0       | count: 1       |
|--------------------------------------------------------|
|                     Stories status                     |
|--------------------------------------------------------|
| New                 points: 113.0     | count: 17      |
==========================================================

==========================================================
| Stats for: XXXX XXXXX XXXXXXX                          |
==========================================================
| Total points:		68.0                                 |
| Total stories:	14                                   |
| Total projects:	5                                    |
|--------------------------------------------------------|
|                       Tags stats                       |
|--------------------------------------------------------|
| no-tags             points: 204.0     | count: 42      |
|--------------------------------------------------------|
|                     Stories status                     |
|--------------------------------------------------------|
| New                 points: 68.0      | count: 14      |
|--------------------------------------------------------|
|               Available on for stories                 |
|--------------------------------------------------------|
| no-tags                  13-01-2016                    |
==========================================================

==========================================================
| Stats for: Ricardo Jorge Vieira Ribeiro                |
==========================================================
| Total points:		45.0                                 |
| Total stories:	3                                    |
| Total projects:	3                                    |
|--------------------------------------------------------|
|                       Tags stats                       |
|--------------------------------------------------------|
| urgent              points: 20.0      | count: 1       |
| no-tags             points: 110.0     | count: 7       |
| important           points: 5.0       | count: 1       |
|--------------------------------------------------------|
|                     Stories status                     |
|--------------------------------------------------------|
| New                 points: 45.0      | count: 3       |
|--------------------------------------------------------|
|               Available on for stories                 |
|--------------------------------------------------------|
| urgent                   11-12-2015                    |
| important                14-12-2015                    |
| no-tags                  31-12-2015                    |
==========================================================


================================================================================
| NOT ASSIGNED STORIES                                                         |
================================================================================
| Project                                | Story                               |
|------------------------------------------------------------------------------|
| Maintenance - study.earcs.pt           | Review the backups                  |
| PyControl                              | teste                               |
================================================================================
```


## How to use

- Download and install the library: python setup.py install.
- Configure the settings.py file:
	- Run the script 'scripts/list-my-members.py' to find your team members ID'.
	- Configure the 'scripts/settings.py' file with your taiga.io credentials and the ids of your team members.
- Run the 'scripts/team-stats.py' file to produce your first report.
- Run the 'scripts/user-next-days-workload.py' file to generate a user workload for the next days.
- Configure a crontab to run everyday the script 'scripts/save-team-stats.py'.
	- This script will generate the team history.
- Use the script 'scripts/total-points-overtime.py' to generate graphs for the work progression.