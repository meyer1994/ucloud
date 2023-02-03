from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    UCLOUD_REST_TYPE: str = 'sqlite'
    UCLOUD_REST_SQLITE_PATH: str = 'sqlite:////tmp/ucloud'
    UCLOUD_REST_MONGODB_PATH: str = 'mongodb://127.0.0.1'
    UCLOUD_REST_POSTGRESQL_PATH: str = 'postgresql://postgres@127.0.0.1/postgres'

    UCLOUD_FILES_TYPE: str = 'local'
    UCLOUD_FILES_LOCAL_PATH: str = '/tmp/ucloud_files'

    UCLOUD_QUEUE_TYPE: str = 'sqlite'
    UCLOUD_QUEUE_SQLITE_PATH: str = 'sqlite:////tmp/ucloud'
    UCLOUD_QUEUE_MONGODB_PATH: str = 'mongodb://127.0.0.1'
    UCLOUD_QUEUE_POSTGRESQL_PATH: str = 'postgresql://postgres@127.0.0.1/postgres'


config = Config()


def ConfigDep() -> Config:
    return config
