from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from api.response import ResponseMessageDto
from db.database import DBSession
from db.exceptions import DBDataException, DBIntegrityException, DBUserNotExistExtension
from db.queries import message as message_queries
from transport.sanic.endpoints import BaseEndpoint
from transport.sanic.exceptions import SanicDBException, SanicUserNotFound, SanicAccessDeniedException


class MessageEndpoint(BaseEndpoint):

    async def method_patch(self,
                           request: Request,
                           body: dict,
                           session:DBSession,
                           message_id,
                           token:dict,
                           *args, **kwargs) -> BaseHTTPResponse:

        sender_id = token['uid']

        try:
            message_queries.check_message_author(session,  message_id, sender_id)
        except SanicAccessDeniedException as e:
            raise SanicAccessDeniedException(str(e))

        request_model = RequestPatchMessageDto(body)
        db_message = message_queries.patch_message(session, request_model, message_id, sender_id)
        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))
        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_delete(
            self,
            request: Request,
            body: dict,
            session:DBSession,
            message_id,
            token:dict,
            *args, **kwargs) -> BaseHTTPResponse:

        sender_id = token['uid']
        try:
            message_queries.check_message_author(session, message_id, sender_id)
        except SanicAccessDeniedException as e:
            raise SanicAccessDeniedException(str(e))

        message_queries.delete_message(session, message_id=message_id)

        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))
        return await self.make_response_json(status=204)

    async def method_post(self, request: Request, body: dict, session,token:dict, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateMessageDto(body)
        sender_id = token['uid']

        try:
            db_message = message_queries.create_message(session, request_model, sender_id)
        except DBUserNotExistExtension as e:
            raise SanicUserNotFound('recipient not found')
        try:
            session.commit_session()
        except (DBDataException, DBIntegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseMessageDto(db_message)

        return await self.make_response_json(body=response_model.dump(), status=201)

    async def method_get(
            self,
            request: Request,
            body: dict,
            session:DBSession,
            message_id,
            token:dict,
            *args, **kwargs) -> BaseHTTPResponse:

        sender_id = token['uid']
        try:
            message_queries.check_message_author(session, message_id, sender_id)
        except SanicAccessDeniedException as e:
            raise SanicAccessDeniedException(str(e))

        db_message=message_queries.get_message(session, message_id=message_id)

        response_model = ResponseMessageDto(db_message)
        return await self.make_response_json(body=response_model.dump(), status=202)
