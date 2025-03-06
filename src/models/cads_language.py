from tortoise import Model, fields
from src.types import LanguageRequest
from src.utils import SnowFlake

class CadsLanguage(Model):
  id = fields.BigIntField(pk=True, generated=False)
  cads = fields.ForeignKeyField('models.CodeActivityDayStatistics', related_name='languages')
  name = fields.CharField(max_length=255)
  duration = fields.BigIntField()
  characters_added = fields.BigIntField()
  characters_deleted = fields.BigIntField()

  @classmethod
  async def new(cls, cads:'CodeActivityDayStatistics', language: LanguageRequest):
    '''
    创建一个新的 CadsLanguage 对象
    '''
    obj = CadsLanguage()
    obj.id = SnowFlake().gen_id()
    obj.cads = cads
    obj.name = language.name
    obj.duration = language.duration
    obj.characters_added = language.characters_added
    obj.characters_deleted = language.characters_deleted
    return obj
