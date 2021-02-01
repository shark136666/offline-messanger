from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.exceptions import DBDataException, DBintegrityException, DBUserNotExistExtension
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserNotFound, SanicAccessDeniedException


class MessageEndpoint(BaseEndpoint):
    async def method_patch(self, request: Request, body: dict, session, message_id, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestPatchMessageDto(body)

        try:
            db_message = message_queries.patch_message(session, request_model, message_id)
        except DBUserNotExistExtension as e:
            raise SanicUserNotFound('recipient not found')

        # if kwargs['token']['eid'] is not uid:
        #     raise SanicAccessDeniedException(message="Access denied")
        try:
            session.commit_session()
        except (DBDataException, DBintegrityException) as e:
            raise SanicDBException(str(e))
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)