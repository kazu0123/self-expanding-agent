from os import getenv, open
from pathlib import Path

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from openai import OpenAI
from sqlmodel import select, Session

from database import get_session
from prompts import function_generation
from models import LlmFunction, LlmFunctionFile


load_dotenv()

router = APIRouter(prefix="/create-function-from-text")
client = OpenAI(api_key=getenv("OPENAI_API_KEY"))


@router.post("/")
def create_function_from_text(prompt: str, session: Session=Depends(get_session)):
  chat_completion = client.chat.completions.create(
    messages=[
      *function_generation.messages,
      { "role": "user", "content": prompt}
    ],
    model="gpt-4o",
    functions=function_generation.functions
  )
  function_call = chat_completion.choices[0].message.function_call
  if function_call is None:
    return Response(status_code=503)
  if function_call.name == function_generation.name:
    function_info = function_generation.FunctionInfo.model_validate_json(function_call.arguments)
    llm_function = LlmFunction(function_name=function_info.function_name, description=function_info.description)

    session.add(llm_function)
    session.commit()
    session.refresh(llm_function)

    for function_file in function_info.files:
      session.add(LlmFunctionFile(
        function_id=llm_function.function_id,
        file_name=function_file.file_name,
        contents=function_file.text_content
      ))

    session.commit()

    return llm_function
