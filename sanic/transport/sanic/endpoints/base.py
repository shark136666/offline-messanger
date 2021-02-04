from sanic.request import Request
from sanic.response import BaseHTTPResponse
from sanic.exceptions import SanicException

from db.database import DBSession
from db.exceptions import DBUserNotExistExtension
from transport.sanic.base import SanicEndpoint

from db.queries import user as user_queries
from transport.sanic.exceptions import SanicAccessDeniedException


class BaseEndpoint(SanicEndpoint):
    async def _method(self, request: Request, body: dict,  *args, **kwargs) -> BaseHTTPResponse:
        database = self.context.database
        session = database.make_session()
        if kwargs.get('token') is not None:
            token = kwargs['token']
            try:
                self.authorization(session, token)
            except SanicAccessDeniedException:
                return await self.make_response_json(status=403)

        try:
            return await super()._method(request, body, session, *args, **kwargs)

        except SanicException as e:
            return await self.make_response_json(status=e.status_code, message=str(e))

    @staticmethod
    def authorization(session: DBSession, token):
        try:
            user_queries.get_user(session, user_id=token['uid'])
        except DBUserNotExistExtension as e:
            raise SanicAccessDeniedException(message='Access denied')

