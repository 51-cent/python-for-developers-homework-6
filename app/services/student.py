from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.student import Student as StudentModel
from app.shemas.student import Student, StudentResponse


def create_student(db: Session, data: Student) -> StudentResponse:
    student = StudentModel(**data.model_dump())

    db.add(student)
    db.commit()
    db.refresh(student)

    return StudentResponse.model_validate(student)


def get_student_by_id(db: Session, student_id: int) -> StudentResponse | None:
    student = db.scalar(select(StudentModel).where(StudentModel.id == student_id))

    if student is None:
        return None

    return StudentResponse.model_validate(student)
