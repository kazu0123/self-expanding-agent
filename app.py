from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import create_db_and_tables
from routers import create_function_from_text, llm_function, llm_function_file

@asynccontextmanager
async def lifespan(app: FastAPI):
  create_db_and_tables()
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(create_function_from_text.router)
app.include_router(llm_function.router)
app.include_router(llm_function_file.router)
