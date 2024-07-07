from typing import Optional

from sqlmodel import Field, SQLModel


class LlmFunction(SQLModel, table=True):
  function_id: Optional[int] = Field(default=None, primary_key=True)
  function_name: str = Field(index=True, max_length=255)
  description: str = Field(max_length=2047)


class LlmFunctionFile(SQLModel, table=True):
  file_id: Optional[int] = Field(default=None, primary_key=True)
  function_id: int = Field(foreign_key="llmfunction.function_id")
  file_name: str = Field(max_length=255)
  contents: str = Field(max_length=8191)
