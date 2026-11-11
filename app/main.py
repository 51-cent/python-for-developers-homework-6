from fastapi import FastAPI

from app.routes.student import router as student_router

app = FastAPI(title="Домашнее задание 6. Работа с базами данных: FastAPI, SQLAlchemy, Alembic")

app.include_router(student_router, prefix="/student")
