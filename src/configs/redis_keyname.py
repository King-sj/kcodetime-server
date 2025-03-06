import os
class Config():
  '''
  redis keyname config
  '''
  def __init__(self):
    # 去重 code_activity:request_id
    self.CODE_ACTIVITY_REQUEST = os.getenv('CODE_ACTIVITY_REQUEST', 'code_activity:request_id:')