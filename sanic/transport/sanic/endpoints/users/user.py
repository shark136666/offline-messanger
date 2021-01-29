from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import  RequestPatchUserDto
from db.database import DBSession
from transport.sanic.endpoints import BaseEndpoint
from api.response import ResponseUserDto
from transport.sanic.exceptions import SanicPasswordHashException, SanicDBException, SanicEmployeeConflictException, \
    SanicUserNotFound, SanicAccessDeniedException

from db.queries import user as user_queries
from db.exceptions import DBDataException, DBintegrityException, DBEmployeeExistException, DBUserNotExistExtension
from helpers.password import generate_hash
from helpers.password import GeneratePasswordHashException


class UserEndpoint(BaseEndpoint):
    async def method_patch(
            self, request: Request, body: dict, session:DBSession, uid:int, *args, **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestPatchUserDto(body)

        if kwargs['token']['eid'] is not uid:
            raise SanicAccessDeniedException(message="Access denied")
        try:
            user = user_queries.patch_user(session, request_model, uid)
        except DBUserNotExistExtension:
            raise SanicUserNotFound('User not found')

        try:
            session.commit_session()
        except (DBDataException, DBintegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(user)
        return await self.make_response_json(status=200, body=response_model.dump())

    async def method_delete(
            self, request: Request, body: dict, session:DBSession, uid: int, *args, **kwargs) -> BaseHTTPResponse:
        try:
            user_queries.delete_user(session, user_id=uid)
        except DBUserNotExistExtension as e:
            raise SanicUserNotFound('User not found')
        try:
            session.commit_session()
        except (DBDataException, DBintegrityException) as e:
            raise SanicDBException(str(e))

        return await self.make_response_json(status=204)

    async def method_get(
            self, request: Request, body: dict, session: DBSession, uid: int, *args, **kwargs
    ) -> BaseHTTPResponse:
        request_model = RequestPatchUserDto(body)
        if kwargs['token']['eid'] is not uid:
            raise SanicAccessDeniedException(message="Access denied")
        try:
            user = user_queries.patch_user(session, request_model, uid)
        except DBUserNotExistExtension:
            raise SanicUserNotFound('User not found')

        response_model = ResponseUserDto(user)
        body = response_model.dump()
        body.pop('id')
        return await self.make_response_json(status=200, body=response_model.dump())
