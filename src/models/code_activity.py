from quart_cors import T
from tortoise import Model, fields
from src.types import CodeActivityRequest
from src.models import User
class CodeActivity(Model):
  '''
  代码活动详细记录

  id 须采用适用分布式的 id 生成算法
  '''
  id = fields.BigIntField(pk=True, generated=False)
  # 建立双向关联通道
  # example: user_a.code_activities.all()
  user = fields.ForeignKeyField('models.User', related_name='code_activities')
  cads = fields.ForeignKeyField('models.CodeActivityDayStatistics', related_name='code_activities')
  start_time_stamp = fields.BigIntField()
  end_time_stamp = fields.BigIntField()
  project_name = fields.CharField(max_length=255)
  project_branch = fields.CharField(max_length=255)
  debug_duration = fields.BigIntField()
  terminal_duration = fields.BigIntField()
  os_name = fields.CharField(max_length=255)
  os_version = fields.CharField(max_length=255)
  ide_name = fields.CharField(max_length=255)
  ide_version = fields.CharField(max_length=255)
  version = fields.CharField(max_length=255)


  @classmethod
  async def new(cls, user:User, cads:'CodeActivityDayStatistics', activity: CodeActivityRequest):
    '''
    创建一个新的 CodeActivity 对象, 及其关联对象

    userid: 用户 id

    cads_id: CodeActivityDayStatistics id

    activity: CodeActivityRequest 对象

    return: CodeActivity 对象, LanguageInfo 对象列表
    '''
    from src.models import LanguageInfo
    obj = await CodeActivity.get_or_none(id=activity.id)
    if obj:
      raise ValueError(f"CodeActivity {activity.id} already exists")

    obj = CodeActivity()
    obj.id = activity.id
    obj.user = user
    obj.cads = cads
    obj.start_time_stamp = activity.start_time_stamp
    obj.end_time_stamp = activity.end_time_stamp
    obj.project_name = activity.project.name
    obj.project_branch = activity.project.branch
    obj.debug_duration = activity.debug.duration
    obj.terminal_duration = activity.terminal.duration
    obj.os_name = activity.os.name
    obj.os_version = activity.os.version
    obj.ide_name = activity.ide.name
    obj.ide_version = activity.ide.version
    obj.version = activity.version
    # 创建语言信息
    languages = []
    for language in activity.languages:
      lang = await LanguageInfo().new(obj, language)
      languages.append(lang)
    return obj, languages