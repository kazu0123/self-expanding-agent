from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from database import get_session
from models import LlmFunctionFile


router = APIRouter(prefix="/llm-function-file")


@router.post("/")
def create_llm_function_file(llm_function_file: LlmFunctionFile, session: Session=Depends(get_session)):
  session.add(llm_function_file)
  session.commit()
  session.refresh(llm_function_file)
  return llm_function_file

@router.get("/")
def read_llm_function_file(session: Session=Depends(get_session)):
  llm_functions_file = session.exec(select(LlmFunctionFile)).all()
  return llm_functions_file
