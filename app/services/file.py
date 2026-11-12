from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterator

from fastapi import UploadFile

MAX_FILE_SIZE = 5 * 1024 * 1024

@contextmanager
def prepare_csv_file(file: UploadFile, filename: str) -> Iterator[Path]:
    try:
        if file.size is not None and file.size > MAX_FILE_SIZE:
            raise ValueError("Файл слишком большой")

        if not file.filename or Path(file.filename).suffix.lower() != ".csv":
            raise ValueError("Файл не соответствует формату .csv")

        total_size = 0

        with TemporaryDirectory() as directory:
            file_path = Path(directory) / filename
            with file_path.open("wb") as destination:
                while chunk := file.file.read(64 * 1024):
                    total_size += len(chunk)

                    if total_size > MAX_FILE_SIZE:
                        raise ValueError("Файл слишком большой")

                    destination.write(chunk)

            yield file_path
    finally:
        file.file.close()
