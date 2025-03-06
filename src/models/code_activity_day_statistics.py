from tortoise import Model, fields
from src.types import CodeActivityRequest
import datetime
from src.utils import SnowFlake
from typing import Tuple,List

class CodeActivityDayStatistics(Model):
  '''
  每日代码活动统计信息

  '''
  id = fields.BigIntField(pk=True, generated=False)
  user_id = fields.BigIntField()
  date = fields.DateField(auto_now_add=True)
  code_duration = fields.BigIntField()
  debug_duration = fields.BigIntField()
  terminal_duration = fields.BigIntField()

  @classmethod
  def new(cls, user_id: int,
          date: datetime.date) -> 'CodeActivityDayStatistics':
    '''
    创建一个新的 CodeActivityDayStatistics 对象
    '''
    obj = CodeActivityDayStatistics()
    obj.id = SnowFlake().gen_id()
    obj.user_id = user_id
    obj.date = date
    obj.code_duration = 0
    obj.debug_duration = 0
    obj.terminal_duration = 0
    return obj

  @classmethod
  async def get_updated_cads(
      cls, activity: CodeActivityRequest,
      cads: 'CodeActivityDayStatistics ') -> Tuple['CodeActivityDayStatistics', 'CadsProject', 'CadsIDE', 'CadsOS', List['CadsLanguage']]:
    '''
    获得更新后的 CodeActivityDayStatistics 对象，及其关联对象

    不会保存对象到数据库
    '''
    from src.models import CadsIDE, CadsLanguage, CadsOS, CadsProject

    cads.code_duration += sum(
        [language.duration for language in activity.languages])
    cads.debug_duration += activity.debug.duration
    cads.terminal_duration += activity.terminal.duration

    # 更新/创建关联对象
    total_duration = activity.end_time_stamp - activity.start_time_stamp
    # project
    project = await CadsProject.get_or_none(
        cads=cads.id,
        name=activity.project.name,
        branch=activity.project.branch,
    )
    if not project:
      project = await CadsProject().new(cads, activity.project)
    project.duration += total_duration
    # ide
    ide = await CadsIDE.get_or_none(
        cads=cads.id,
        name=activity.ide.name,
    )
    if not ide:
      ide = await CadsIDE().new(cads, activity.ide)
    ide.duration += total_duration

    # os
    os = await CadsOS.get_or_none(
        cads=cads.id,
        name=activity.os.name,
        version=activity.os.version,
    )
    if not os:
      os = await CadsOS().new(cads, activity.os)
    os.duration += total_duration
    # languages
    langs = []
    for lang in activity.languages:
      language = await CadsLanguage.get_or_none(
          cads=cads.id,
          name=lang.name,
      )
      if not language:
        language = await CadsLanguage().new(cads, lang)
      language.duration += lang.duration
      langs.append(language)

    return cads, project, ide, os, langs
