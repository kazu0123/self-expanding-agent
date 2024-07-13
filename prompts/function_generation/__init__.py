from pathlib import Path
from pydantic import Field, BaseModel

from openai.types.chat import ChatCompletionMessageParam
from openai.types.chat.completion_create_params import Function


name = "create_function"

system_prompt = Path("prompts/function_generation/system.md").read_text(encoding="utf-8")

messages: list[ChatCompletionMessageParam] = [
  { "role": "system", "content": system_prompt }
]


class FunctionFile(BaseModel):
  file_name: str = Field(description="ファイル名", examples=[
    "DateInfo.py",
    "dockerfile",
    "get_datetime.py",
    "main.py",
    "requirements.txt"
  ])
  text_content: str = Field(description="ファイルの中身", examples=[
    Path("prompts/function_generation/examples/get_datetime/DateInfo.py").read_text(encoding="utf-8"),
    Path("prompts/function_generation/examples/get_datetime/dockerfile").read_text(encoding="utf-8"),
    Path("prompts/function_generation/examples/get_datetime/get_datetime.py").read_text(encoding="utf-8"),
    Path("prompts/function_generation/examples/get_datetime/main.py").read_text(encoding="utf-8"),
    Path("prompts/function_generation/examples/get_datetime/requirements.txt").read_text(encoding="utf-8"),
  ])

class FunctionInfo(BaseModel):
  function_name: str = Field(description="呼び出される関数名", examples=["get_datetime"])
  description: str = Field(description="関数についての1-2文の短い説明", examples=[
    "現在時刻をISOフォーマットで取得できる関数です。タイムゾーンを指定できます。",
  ])
  json_schema: str = Field(description="引数をJsonSchemaで表現してください。JSONをテキスト形式で返却すること。", examples=[
    Path("prompts/function_generation/examples/get_datetime/schema.json").read_text(encoding="utf-8"),
  ])
  files: list[FunctionFile] = Field(description="配置するファイル")


functions: list[Function] = [
  Function(
    name=name,
    description="関数を作成し、追加します",
    parameters=FunctionInfo.model_json_schema(),
  )
]
