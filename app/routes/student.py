from typing import Annotated

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.shemas.student import Student, StudentResponse
from app.services.student import create_student, get_student_by_id

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=StudentResponse, tags=["Добавление нового студента"])
def create(request: Student, db: DbSession) -> StudentResponse:
    return create_student(db, request)


@router.get("/{student_id}", response_model=StudentResponse, tags=["Получение студента по id"])
def get(student_id: int, db: DbSession) -> StudentResponse:
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    return student
