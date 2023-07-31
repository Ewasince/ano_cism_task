from sqlalchemy import URL

from service.config import config


def get_url_db(storage_driver: str):
    return URL.create(
        storage_driver,
        config.users_storage_username,
        config.users_storage_password,
        config.users_storage_host,
        config.users_storage_port,
        config.users_storage_database,
    )
    pass
