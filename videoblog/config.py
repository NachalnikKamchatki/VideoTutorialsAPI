from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin


class Config:
    DEBUG = True
    SECRET_KEY = "12345"
    APISPEC_SPEC = APISpec(
        title='videoblog',
        version='v1',
        openapi_version='2.0',
        plugins=[MarshmallowPlugin()]
    )
    APISPEC_SWAGGER_URL = '/swagger/'
