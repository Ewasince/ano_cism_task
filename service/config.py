import os

from pydantic import BaseModel

__all__ = ['config']


class Config(BaseModel):
    """
    Основной класс конфига, выполняющий проверку всех полей
    """

    # secrets

    # public config

    ## logs
    log_level_console: str
    log_level_file: str
    log_file: str
    keep_log_files: int

    ## app
    service_host: str
    service_port: str

    ## storage
    users_storage_username: str
    users_storage_password: str
    users_storage_host: str
    users_storage_port: int
    users_storage_database: str

    ## broker
    broker_username: str
    broker_password: str
    broker_host: str
    broker_port: int

    ### channel properties
    broker_channel_tasks: str
    broker_channel_completed: str

    # делаем конфиг неизменяемым
    class Config:
        frozen = True

    pass


# создание конфига
__config_dict = {}

for param in Config.model_fields:
    param: str
    __config_dict[param] = os.environ.get(param.upper())
    pass

config = Config(**__config_dict)
