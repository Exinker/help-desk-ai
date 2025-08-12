from collections.abc import Mapping
from pydantic import Field, SecretStr, computed_field

from config.base_config import BaseConfig


class DBConfig(BaseConfig):

    host: str = Field('localhost', alias='DB_HOST')
    port: int = Field(5432, alias='DB_PORT')
    username: str = Field(alias='DB_USERNAME')
    password: SecretStr = Field(alias='DB_PASSWORD')
    database: str = Field('test', alias='DB_DATABASE')
    schema: str = Field('help_desk_ai', alias='DB_SCHEMA')

    @computed_field
    @property
    def url(self) -> str:
        return 'postgresql+psycopg://{username}:{password}@{host}:{port}/{database}'.format(
            username=self.username,
            password=self.password.get_secret_value(),
            host=self.host,
            port=self.port,
            database=self.database,
        )

    @property
    def naming_convention(self) -> Mapping[str, str]:

        return {
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s',
        }


DB_CONFIG = DBConfig()
