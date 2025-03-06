from src.services import update_code_activity
import pytest
from src.types import CodeActivityRequest
import pytest
import json

@pytest.mark.asyncio
async def test_update_code_activity():
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
  await update_code_activity(1, activity)