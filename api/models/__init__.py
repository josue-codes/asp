from mongoengine import connect

from api.config import APP_CONFIG


connect(
    db=APP_CONFIG.mongo_db_name,
    username=APP_CONFIG.mongo_db_username,
    password=APP_CONFIG.mongo_db_password,
    host=f'{APP_CONFIG.mongo_db_scheme}{APP_CONFIG.mongo_db_host}',
)


if __name__ == '__main__':  # pragma: no cover
    pass
