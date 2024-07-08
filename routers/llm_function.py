from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from database import get_session
from models import LlmFunction


router = APIRouter(prefix="/llm-function")


@router.post("/")
def create_llm_function(llm_function: LlmFunction, session: Session=Depends(get_session)):
  session.add(llm_function)
  session.commit()
  session.refresh(llm_function)
  return llm_function

@router.get("/")
def read_llm_function(session=Depends(get_session)):
  llm_functions = session.exec(select(LlmFunction)).all()
  return llm_functions