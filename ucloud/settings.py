from pathlib import Path
from tempfile import NamedTemporaryFile

from pydantic import BaseSettings, AnyUrl


class Config(BaseSettings):
    UCLOUD_REST_TYPE: str = 'mongodb'
    UCLOUD_REST_SQLITE_PATH: str = 'sqlite:///' + NamedTemporaryFile().name
    UCLOUD_REST_MONGODB_PATH: str = 'mongodb://127.0.0.1'
    UCLOUD_REST_POSTGRESQL_PATH: str = 'postgresql://postgres@127.0.0.1/postgres'


config = Config()


def ConfigDep() -> Config:
    return config
