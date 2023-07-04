from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from api.config import APP_CONFIG
from api.security import (
    authenticate_user_with_form_data,
    create_access_token,
)
from api.models.user import User


router = APIRouter(prefix='/auth')


@router.post('/token', response_model=None)
def login_for_access_token(
        user: User = Depends(authenticate_user_with_form_data)
) -> JSONResponse:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    access_token_expires = timedelta(minutes=APP_CONFIG.access_token_expire_minutes)
    access_token = create_access_token(
        data={'sub': user.email, 'roles': user.roles},
        expires_delta=access_token_expires,
    )
    response = JSONResponse(content={'message': 'Authentication successful.'})
    response.set_cookie(
        "access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        samesite='strict',
        max_age=18000,
        expires=18000
    )
    return response


if __name__ == '__main__':  # pragma: no cover
    pass
