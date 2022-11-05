from fastapi import HTTPException
from starlette import status


class BaseApiException(HTTPException):
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = ""

    def __init__(self, **kwargs) -> None:
        self.detail = kwargs.pop("detail", None) or self.detail
        self.status_code = kwargs.pop("status_code", None) or self.status_code
        super().__init__(status_code=self.status_code, detail=self.detail, **kwargs)


class UnauthorizedException(BaseApiException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Не удалось подтвердить учетные данные"

    def __init__(self, **kwargs) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"}, **kwargs)


class ForbiddenException(BaseApiException):
    status_code = status.HTTP_403_FORBIDDEN


class NotFoundException(BaseApiException):
    status_code = status.HTTP_404_NOT_FOUND


class BadRequestException(BaseApiException):
    status_code = status.HTTP_400_BAD_REQUEST
