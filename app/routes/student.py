from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.shemas.student import Student, StudentResponse
from app.services.student import create_student

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/", tags=["create student"])
def create(request: Student, db: DbSession) -> StudentResponse:
    return create_student(db, request)
