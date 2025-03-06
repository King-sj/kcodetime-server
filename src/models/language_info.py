import code
from tortoise import Model, fields
from src.types import LanguageRequest
from src.models import CodeActivity
from src.utils import SnowFlake

class LanguageInfo(Model):
  id = fields.BigIntField(pk=True, generated=False)
  code_activity = fields.ForeignKeyField('models.CodeActivity',
                                         related_name='language_infos')
  name = fields.CharField(max_length=255)
  characters_added = fields.BigIntField()
  characters_deleted = fields.BigIntField()
  duration = fields.BigIntField()

  @classmethod
  async def new(cls, activity:CodeActivity, language: LanguageRequest):
    '''
    创建一个新的 LanguageInfo 对象
    '''
    from src.models import CodeActivity
    obj = LanguageInfo()
    obj.id = SnowFlake().gen_id()
    obj.code_activity = activity
    obj.name = language.name
    obj.characters_added = language.characters_added
    obj.characters_deleted = language.characters_deleted
    obj.duration = language.duration
    return obj
