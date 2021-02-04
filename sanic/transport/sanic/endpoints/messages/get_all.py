from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.response import ResponseMessageDto
from db.database import DBSession
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint


class AllMessageEndpoint(BaseEndpoint):

    async def method_get(self,
                         request: Request,
                         body: dict,
                         session: DBSession,
                         token: dict,
                         *args, **kwargs) -> BaseHTTPResponse:
        sender_id = token['uid']
        db_message = message_queries.get_all_messages(session, sender_id)

        response_model = ResponseMessageDto(db_message, many=True)
        body = {'messages': response_model.dump()}

        return await self.make_response_json(body=body, status=202)
