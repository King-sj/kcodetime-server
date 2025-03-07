from src.models import *
from src.types import *

async def get_user_create_time(user_id: int):
  user = await User.get(id=user_id)
  return user.created_at


async def get_projects_times(user_id: int, date_range: DateRangeRequest):
  cadses = await CodeActivityDayStatistics.filter(
    user_id=user_id,
    date__gte=date_range.date_from,
    date__lte=date_range.date_to
  ).order_by('date')
  res = []
  for cads in cadses:
    cads_projects = await CadsProject.filter(cads=cads)
    tmp = {
      'date': cads.date.strftime('%Y-%m-%d'),
      'projects': []
    }
    for cads_project in cads_projects:
      tmp['projects'].append({
        'project_name': cads_project.name,
        'duration': cads_project.duration
      })
    res.append(tmp.copy())
  return res