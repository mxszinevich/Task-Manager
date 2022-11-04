from fastapi import Header


class TokenInputData:
    def __call__(self, authorization: str | None = Header(...)) -> str:
        return authorization
