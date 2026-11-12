import csv
from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.file import prepare_csv_file
from app.services.student import (
    create_student,
    get_student_by_id,
    load_csv_data,
    get_student_by_faculty,
    get_lower_mark_students,
    get_unique_courses as get_unique_courses_service,
    get_average_mark_by_faculty as get_average_mark_service,
)
from app.shemas.student import Student, StudentResponse

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=StudentResponse, tags=["Добавление нового студента"])
def create(request: Student, db: DbSession) -> StudentResponse:
    return create_student(db, request)


@router.post("/upload-csv", tags=["Загрузка студентов из CSV"])
def upload_csv(
        db: DbSession,
        file: Annotated[UploadFile, File()],
        delimiter: Annotated[str, Query(min_length=1, max_length=1)] = ",",
) -> dict[str, int]:
    try:
        with prepare_csv_file(file, "students.csv") as file_path:
            count = load_csv_data(db, file_path, delimiter=delimiter)
    except (ValueError, csv.Error) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"imported": count}


@router.get("/by-faculty", response_model=list[StudentResponse], tags=["Получение списка студентов по факультету"])
def get_by_faculty(faculty: str, db: DbSession) -> list[StudentResponse]:
    return get_student_by_faculty(db, faculty)


@router.get("/unique-courses", response_model=list[str], tags=["Получение уникальных курсов"])
def get_unique_courses(db: DbSession) -> list[str]:
    return get_unique_courses_service(db)


@router.get("/lower-mark", response_model=list[StudentResponse], tags=["Получение студентов с оценкой ниже 30"])
def get_lower_mark(db: DbSession) -> list[StudentResponse]:
    return get_lower_mark_students(db, 30)


@router.get("/faculty-average-mark", response_model=float, tags=["Получение средней оценки по факультету"])
def get_average_mark(faculty: str, db: DbSession) -> float:
    return get_average_mark_service(db, faculty)


@router.get("/{student_id}", response_model=StudentResponse, tags=["Получение студента по id"])
def get(student_id: int, db: DbSession) -> StudentResponse:
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Студент не найден")

    return student
