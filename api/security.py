from datetime import timedelta, datetime

from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

from api.config import APP_CONFIG
from api.models.user import User
from api.roles import Roles


crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


class TokenData(BaseModel):
    username: str
    expiration: datetime
    roles: list[Roles] | None = [Roles.client]


def password_verified(plain_password, hashed_password) -> bool:
    return crypt_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return crypt_context.hash(password)


def create_user(
        given_name: str,
        surname: str,
        email: EmailStr,
        password: str = Depends(hash_password),
        roles: list[Roles] | None = None
) -> User:
    if roles is None:
        roles = [Roles.client]
    if isinstance(roles, Roles):
        roles = [roles]
    roles = [role.value for role in roles]
    user = User(
        given_name=given_name,
        surname=surname,
        email=email,
        hashed_password=password,
        roles=roles
    )
    user.save()
    return user


def authenticate_user(username: str, password: str) -> User | None:
    user = User.objects(email=username).first()
    if user and password_verified(password, user.hashed_password):
        return user
    return None


def authenticate_user_with_form_data(
        form_data: OAuth2PasswordRequestForm = Depends()
) -> User:
    if user := authenticate_user(form_data.username, form_data.password):
        return user
    raise credentials_exception


def create_access_token(
        data: dict,
        expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(
        to_encode,
        APP_CONFIG.secret_key,
        algorithm=APP_CONFIG.secret_algorithm
    )
    return encoded_jwt


def authenticate_user_with_access_token(
        request: Request
) -> dict:
    access_token = _get_access_token_from_cookies(request)
    payload = _decode_access_token(access_token)
    user = _get_user(payload.get('sub'))
    return user.dict()


def _get_access_token_from_cookies(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise credentials_exception

    scheme, access_token = token.split()
    if scheme.lower() != 'bearer':
        raise credentials_exception

    return access_token


def _decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token=token,
            key=APP_CONFIG.secret_key,
            algorithms=[APP_CONFIG.secret_algorithm]
        )
    except JWTError:
        raise credentials_exception

    return payload


def _get_user(email: str | None):
    if email is None:
        raise credentials_exception

    user = User.objects(email=email).first()
    if user is None:
        raise credentials_exception

    return user


if __name__ == '__main__':  # pragma: no cover
    pass
