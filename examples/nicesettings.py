"""
One of pydantic's most useful applications is settings management.

If you create a model that inherits from BaseSettings, the model 
initialiser will attempt to determine the values of any fields not 
passed as keyword arguments by reading from the environment. 
(Default values will still be used if the matching environment 
variable is not set.)
"""

from typing import Set
import os
from pydantic import (
    BaseModel,
    BaseSettings,
    PyObject,
    RedisDsn,
    PostgresDsn,
    Field,
)


class SubModel(BaseModel):
    foo = 'bar'
    apple = 1



# set environment variables:
os.environ['my_prefix_auth_key'] = 'not working'
os.environ['my_prefix_my_api_key'] = 'not working'

os.environ['my_auth_key'] = 'works'
os.environ['my_api_key'] = 'works'

os.environ['my_prefix_domains'] = '["wor.com", "ks.com"]'


class Settings(BaseSettings):
    auth_key: str = "yyy"

    # custom environment variable names:
    api_key: str = Field("xxx", env='my_api_key')

    redis_dsn: RedisDsn = 'redis://user:pass@localhost:6379/1'
    pg_dsn: PostgresDsn = 'postgres://user:pass@localhost:5432/foobar'

    special_function: PyObject = 'math.cos'

    domains: Set[str] = set()

    more_settings: SubModel = SubModel()

    class Config:
        env_prefix = 'my_prefix_'  # defaults to no prefix, i.e. ""
        case_sensitive = True  # case-sensitivity can be turned on
        # custom environment variable names:
        fields = {
            'auth_key': {
                'env': 'my_auth_key',
            },
            'redis_dsn': {
                'env': ['service_redis_dsn', 'redis_url']
            }
        }


print(Settings().dict())

# to override:
# export my_prefix_more_settings='{"foo": "x", "apple": 1}'
# export my_prefix_special_function='foo.bar'

"""
Complex types like: list, set, dict, and sub-models are 
populated from the environment by treating the environment 
variable's value as a JSON-encoded string.

ie. more_settings
"""
