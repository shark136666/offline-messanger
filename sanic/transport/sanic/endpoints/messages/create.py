from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto
from api.response import ResponseMessageDto
from db.exceptions import DBDataException, DBintegrityException, DBUserNotExistExtension
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserNotFound


class CreateMessageEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict, session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)
        sender_id = kwargs['token']['eid']
        request_model.sender_id = sender_id
        try:
            db_message = message_queries.create_message(session, request_model,)
        except DBUserNotExistExtension as e:
            raise SanicUserNotFound('recipient not found')
        try:
            session.commit_session()
        except (DBDataException, DBintegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)