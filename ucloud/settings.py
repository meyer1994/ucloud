from pathlib import Path
from tempfile import mkstemp, mkdtemp

from pydantic import BaseSettings, AnyUrl


class Config(BaseSettings):
    UCLOUD_REST_TYPE: str = 'mongodb'
    UCLOUD_REST_SQLITE_PATH: str = 'sqlite:///' + mkstemp()[1]
    UCLOUD_REST_MONGODB_PATH: str = 'mongodb://127.0.0.1'
    UCLOUD_REST_POSTGRESQL_PATH: str = 'postgresql://postgres@127.0.0.1/postgres'

    UCLOUD_FILES_TYPE: str = 'local'
    UCLOUD_FILES_LOCAL_PATH: str = mkdtemp()

    UCLOUD_QUEUE_TYPE: str = 'sqlite'
    UCLOUD_QUEUE_SQLITE_PATH: str = 'sqlite:///' + mkstemp()[1]


config = Config()


def ConfigDep() -> Config:
    return config
