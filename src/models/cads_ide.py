from tortoise import Model,fields
from src.types import IDERequest
from src.utils import SnowFlake
class CadsIDE(Model):
  id = fields.BigIntField(pk=True, generated=False)
  cads = fields.ForeignKeyField('models.CodeActivityDayStatistics', related_name='ides')
  name = fields.CharField(max_length=255)
  duration = fields.BigIntField()

  @classmethod
  async def new(cls, cads:'CodeActivityDayStatistics', ide: IDERequest,duration:int=0):
    '''
    创建一个新的 CadsIDE 对象
    '''
    from src.models import CodeActivityDayStatistics
    obj = CadsIDE()
    obj.id = SnowFlake().gen_id()
    obj.cads = cads
    obj.name = ide.name
    obj.duration = duration
    return obj