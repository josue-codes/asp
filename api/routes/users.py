from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.security import authenticate_user_with_access_token, TokenData


router = APIRouter(prefix='/users')


@router.get('/')
def index(user: TokenData = Depends(authenticate_user_with_access_token)) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_302_FOUND,
        content={'message': f'Under construction: {user}'}
    )


if __name__ == '__main__':  # pragma: no cover
    pass
