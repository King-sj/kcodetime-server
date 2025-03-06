from src.models import (CodeActivity, CodeActivityDayStatistics, User)
from src.types import CodeActivityRequest

from tortoise.transactions import in_transaction
import datetime
import logging

logger = logging.getLogger(__name__)


async def update_code_activity(user_id: int, activity: CodeActivityRequest):
  # got today's code_activity_day_statistics by user_id and date
  today_cads = await CodeActivityDayStatistics.filter(
      user_id=user_id, date=datetime.date.today()).first()

  today_cads = today_cads or CodeActivityDayStatistics().new(
      user_id, datetime.date.today())
  # update today's cads
  cads, project, ide, os, cad_langs = await CodeActivityDayStatistics.get_updated_cads(activity,today_cads)
  # create a new code_activity
  user = await User.get(id=user_id)
  new_ca,langs = await CodeActivity.new(user, today_cads, activity)

  # save to db
  async with in_transaction() as conn:
    await cads.save(using_db=conn)
    await project.save(using_db=conn)
    await ide.save(using_db=conn)
    await os.save(using_db=conn)
    await new_ca.save(using_db=conn)
    for lang in cad_langs:
      await lang.save(using_db=conn)
    for lang in langs:
      await lang.save(using_db=conn)
    logger.info(f"update code activity {activity.id} success")
  return new_ca


