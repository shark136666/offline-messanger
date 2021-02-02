from sanic.request import Request
from sanic.response import BaseHTTPResponse
from transport.sanic.exceptions import SanicUserNotFound, SanicPasswordHashException

from transport.sanic.endpoints import BaseEndpoint
from db.queries import user as user_queries
from db.exceptions import DBUserNotExistExtension
from helpers.password.hash import check_hash,ChekPasswordHashException
from helpers.auth import create_token
from api.request import RequestAuthUserDto


class AuthUserEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict,session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestAuthUserDto(body)

        try:
            db_user = user_queries.get_user(session, login=request_model.login)
        except DBUserNotExistExtension:
            raise SanicUserNotFound('User not found')

        try:
            check_hash(request_model.password, db_user.password)

        except ChekPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'uid': db_user.id,
        }
        response_body = {
            'Authorization': create_token(payload)
        }
        return await self.make_response_json(
            body=response_body,
            status=200,

        )


