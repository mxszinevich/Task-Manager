from fastapi import Header


class TokenInputData:
    def __call__(self, authorization: str = Header(include_in_schema=False)) -> str:
        return authorization
