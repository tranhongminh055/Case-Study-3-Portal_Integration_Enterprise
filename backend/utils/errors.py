from fastapi import HTTPException

class AppError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail={
            "status": status_code,
            "error": HTTPException(status_code=status_code).detail if status_code >= 500 else "Error",
            "message": detail,
        })

class ConflictError(AppError):
    def __init__(self, detail: str):
        super().__init__(409, detail)

class NotFoundError(AppError):
    def __init__(self, detail: str):
        super().__init__(404, detail)

class BadRequestError(AppError):
    def __init__(self, detail: str):
        super().__init__(400, detail)

class InternalError(AppError):
    def __init__(self, detail: str):
        super().__init__(500, detail)
