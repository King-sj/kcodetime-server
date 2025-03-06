from sys import version
from tortoise import Model,fields
from src.types import OSRequest
from src.utils import SnowFlake

class CadsOS(Model):
  id = fields.BigIntField(pk=True, generated=False)
  cads = fields.ForeignKeyField('models.CodeActivityDayStatistics', related_name='os')
  name = fields.CharField(max_length=255)
  duration = fields.BigIntField()
  version = fields.CharField(max_length=255,null=True)

  @classmethod
  async def new(cls, cads:'CodeActivityDayStatistics', os: OSRequest,duration:int=0):
    '''
    创建一个新的 CadsOS 对象
    '''
    from src.models import CodeActivityDayStatistics
    obj = CadsOS()
    obj.id = SnowFlake().gen_id()
    obj.cads = cads
    obj.name = os.name
    obj.duration = duration
    obj.version = os.version
    return obj