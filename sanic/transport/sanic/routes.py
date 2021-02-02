from configs.config import ApplicationConfig
from context import Context
from transport.sanic import endpoints


def get_routes(config: ApplicationConfig, context: Context):
    return (

        endpoints.HealthEndpoint(config=config, context=context, uri='/', methods=['GET', 'POST', 'PATCH']),
        endpoints.AuthEmployeeEndpoint(config, context, uri='/employee/auth', methods=['POST']),
        endpoints.UserEndpoint(config, context, uri='/user', methods=['POST']),
        endpoints.AuthUserEndpoint(config, context, uri='/auth', methods=['POST']),
        endpoints.UserEndpoint(config, context, uri='/user/<uid:int>', methods=['GET', 'PATCH', 'DELETE'],
                               auth_required=True),
        endpoints.MessageEndpoint(config, context, uri='/msg', methods=['POST'], auth_required=True),
        endpoints.MessageEndpoint(config, context, uri='/msg/<message_id>', methods=['PATCH', 'DELETE','GET'],
                                  auth_required=True)

    )
