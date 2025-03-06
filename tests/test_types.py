from src.types import CodeActivityRequest
import json
import pytest
from pydantic import ValidationError

@pytest.mark.asyncio
async def test_code_activity_request():
  '''
  Test CodeActivityRequest
  '''
  json_data = '''
    {
      "id": "1",
      "start_time_stamp": 1678000000,
      "end_time_stamp": 1678003600,
      "languages": [
        {"name": "Python", "characters_added": 100, "characters_deleted": 10, "duration": 3600}
      ],
      "project": {"name": "MyProject", "branch": "main"},
      "debug": {"duration": 60},
      "terminal": {"duration": 120},
      "os": {"name": "Linux", "version": "Ubuntu 22.04"},
      "ide": {"name": "VSCode", "version": "1.80.0"},
      "version": "v1.2.3"
    }
  '''
  data = json.loads(json_data)
  activity = CodeActivityRequest(**data)
  assert activity.id == 1
  assert activity.start_time_stamp == 1678000000
  assert activity.end_time_stamp == 1678003600
  assert activity.languages[0].name == 'Python'
  assert activity.languages[0].characters_added == 100
  assert activity.languages[0].characters_deleted == 10
  assert activity.languages[0].duration == 3600
  assert activity.project.name == 'MyProject'
  assert activity.project.branch == 'main'
  assert activity.debug.duration == 60
  assert activity.terminal.duration == 120
  assert activity.os.name == 'Linux'
  assert activity.os.version == 'Ubuntu 22.04'
  assert activity.ide.name == 'VSCode'
  assert activity.ide.version == '1.80.0'
  assert activity.version == 'v1.2.3'

@pytest.mark.asyncio
async def test_code_activity_request_failed():
  '''
  Test CodeActivityRequest failed
  '''
  json_data = '''
    {
      "start_time_stamp": 1678000000,
      "end_time_stamp": 1678003600,
      "languages": [
        {"name": "Python", "characters_added": 100, "characters_deleted": 10, "duration": 3600}
      ],
      "project": {"name": "MyProject", "branch": "main"},
      "debug": {"duration": 60},
      "terminal": {"duration": 120},
      "os": {"name": "Linux", "version": "Ubuntu 22.04"},
      "ide": {"name": "VSCode", "version": "1.80.0"},
      "version": "v1.2.3"
    }
  '''
  data = json.loads(json_data)
  with pytest.raises(ValidationError):
    CodeActivityRequest(**data)