from sqlalchemy import String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Student(Base):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    second_name: Mapped[str] = mapped_column("Фамилия", String(256), nullable=False)
    first_name: Mapped[str] = mapped_column("Имя", String(256), nullable=False)
    faculty: Mapped[str] = mapped_column("Факультет", String(256), nullable=False)
    course: Mapped[str] = mapped_column("Курс", String(256), nullable=False)
    mark: Mapped[int] = mapped_column("Оценка", TINYINT(unsigned=True), nullable=False)

