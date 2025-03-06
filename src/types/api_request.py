from pydantic import BaseModel, field_validator, model_validator
from typing import List


class LanguageRequest(BaseModel):
  name: str
  characters_added: int
  characters_deleted: int
  duration: int


class ProjectRequest(BaseModel):
  name: str
  branch: str


class DebugRequest(BaseModel):
  duration: int


class TerminalRequest(BaseModel):
  duration: int


class OSRequest(BaseModel):
  name: str
  version: str


class IDERequest(BaseModel):
  name: str
  version: str


class CodeActivityRequest(BaseModel):
  '''
  Code activity request data

  Attributes:
    id (int): Code activity id
    start_time_stamp (int): Start time stamp
  '''
  id: int
  start_time_stamp: int
  end_time_stamp: int
  languages: List[LanguageRequest]
  project: ProjectRequest
  debug: DebugRequest
  terminal: TerminalRequest
  os: OSRequest
  ide: IDERequest
  version: str

  @model_validator(mode='after')
  def validate_time_order(self):
    if self.start_time_stamp >= self.end_time_stamp:
        raise ValueError("start_time_stamp must before end_time_stamp")
    return self
