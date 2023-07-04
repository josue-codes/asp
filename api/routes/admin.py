from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status, Depends

from api.security import authenticate_user_with_access_token


router = APIRouter(prefix='/admin')


@router.get('/')
def index(
        user: dict = Depends(authenticate_user_with_access_token)
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_302_FOUND,
        content={'message': f'Under construction: {user}'}
    )


if __name__ == '__main__':  # pragma: no cover
    pass
