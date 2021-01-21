from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context):
    return (

        endpoints.HealthEndpoint(config=config, context=context, uri='/', methods=['GET', 'POST', 'PATCH']),
        endpoints.AuthEmployeeEndpoint(config, context, uri='/employee/auth', methods=['POST']),
        endpoints.CreateUserEndpoint(config, context, uri='/user', methods=['POST']),
        endpoints.AuthUserEndpoint(config, context, uri='/user/auth', methods=['POST']),
        endpoints.UserEndpoint(config, context, uri='/user/<uid:int>', methods=['PATCH', 'DELETE'], auth_required=True)

    )
