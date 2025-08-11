from pydantic import Field

from config.base_config import BaseConfig


class TracerConfig(BaseConfig):

    endpoint: str = Field('http://localhost:6006/v1/traces', alias='TRACER_ENDPOINT')
    project_name: str = Field('test', alias='TRACER_PROJECT_NAME')


TRACER_CONFIG = TracerConfig()
