import csv
from pathlib import Path

from sqlalchemy import func, select
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


def get_student_by_faculty(db: Session, faculty: str) -> list[StudentResponse]:
    students = db.scalars(select(StudentModel).where(StudentModel.faculty == faculty)).all()

    return [StudentResponse.model_validate(student) for student in students]


def get_unique_courses(db: Session) -> list[str]:
    unique_courses = db.scalars(
        select(StudentModel.course).group_by(StudentModel.course).having(func.count() == 1)
    ).all()

    return list(unique_courses)


def get_lower_mark_students(db: Session, lower_mark: int) -> list[StudentResponse]:
    students = db.scalars(select(StudentModel).where(StudentModel.mark < lower_mark)).all()

    return [StudentResponse.model_validate(student) for student in students]


def get_average_mark_by_faculty(db: Session, faculty: str) -> float:
    average_mark = db.scalar(
        select(func.avg(StudentModel.mark))
        .where(StudentModel.faculty == faculty)
    )

    return round(float(average_mark), 2) if average_mark is not None else 0.0


def load_csv_data(db: Session, file_path: str | Path, delimiter: str = ",") -> int:
    columns = {
        column.name: attribute.key
        for attribute in StudentModel.__mapper__.column_attrs
        for column in attribute.columns
    }
    students = []

    with open(file_path, encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file, delimiter=delimiter)

        if reader.fieldnames is None:
            raise ValueError("CSV-файл не содержит заголовков")

        fields = [
            columns.get(name.strip(), name.strip())
            for name in reader.fieldnames
        ]

        if len(fields) != len(set(fields)):
            raise ValueError("CSV-файл содержит повторяющиеся заголовки")

        required = set(Student.model_fields)
        missing = required - set(fields)

        if missing:
            raise ValueError(f"В CSV отсутствуют столбцы: {', '.join(missing)}")

        reader.fieldnames = fields

        for row in reader:
            if None in row or any(
                    row[field] is None or not row[field].strip()
                    for field in required
            ):
                raise ValueError(f"Строка {reader.line_num}: неверное число значений")

            try:
                data = Student.model_validate({field: row[field].strip() for field in required})
            except ValueError as error:
                raise ValueError(f"Строка {reader.line_num}: {error}") from error

            students.append(StudentModel(**data.model_dump()))

    if students:
        try:
            db.add_all(students)
            db.commit()
        except Exception:
            db.rollback()
            raise

    return len(students)
