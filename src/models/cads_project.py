from tortoise import Model,fields
from src.types import ProjectRequest
from src.utils import SnowFlake

class CadsProject(Model):
  id = fields.BigIntField(pk=True, generated=False)
  cads = fields.ForeignKeyField('models.CodeActivityDayStatistics', related_name='projects')
  name = fields.CharField(max_length=255)
  duration = fields.BigIntField()
  branch = fields.CharField(max_length=255,null=True)

  @classmethod
  async def new(cls, cads:'CodeActivityDayStatistics', project: ProjectRequest,duration:int=0):
    '''
    创建一个新的 CadsProject 对象
    '''
    from src.models import CodeActivityDayStatistics
    obj = CadsProject()
    obj.id = SnowFlake().gen_id()
    obj.cads = cads
    obj.name = project.name
    obj.duration = duration
    obj.branch = project.branch
    return obj