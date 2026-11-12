import re

from pydantic import BaseModel, Field, field_validator, ConfigDict


class Student(BaseModel):
    first_name: str = Field(min_length=2, max_length=50)
    second_name: str = Field(min_length=2, max_length=50)
    faculty: str = Field(min_length=2, max_length=15)
    course: str = Field(min_length=2, max_length=100)
    mark: int = Field(ge=0, le=100)

    @field_validator('first_name', 'second_name')
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not re.fullmatch(r'[А-ЯЁ][а-яё]+', value):
            raise ValueError("Имя и фамилия должны начинаться с заглавной буквы и содержать только кириллицу")

        return value

class StudentResponse(Student):
    id: int

    model_config = ConfigDict(from_attributes=True)
