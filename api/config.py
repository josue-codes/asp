import pydantic


class __AppConfig(pydantic.BaseSettings):
    # Access Token Settings
    secret_key: str
    secret_algorithm: str
    access_token_expire_minutes: int

    # MongoDB Settings
    mongo_db_scheme: str
    mongo_db_username: str
    mongo_db_password: str
    mongo_db_host: str
    mongo_db_name: str


APP_CONFIG = __AppConfig()


if __name__ == '__main__':  # pragma: no cover
    pass
