from sanic.request import Request
from sanic.response import BaseHTTPResponse

from api.request import RequestPatchUserDto, RequestCreatemeaasgeDto
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
            self, request: Request, body: dict, session:DBSession, uid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        if token.get('uid') is not uid:
            return await self.make_response_json(status=403)
        request_model = RequestPatchUserDto(body)
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
            self, request: Request, body: dict, session:DBSession, uid: int, token:dict, *args, **kwargs) -> BaseHTTPResponse:
        if token.get('uid') is not uid:
            return await self.make_response_json(status=403)
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
            self, request: Request, body: dict, session: DBSession, uid: int, token: dict, *args, **kwargs
    ) -> BaseHTTPResponse:
        if token.get('uid') is not uid:
            return await self.make_response_json(status=403)
        request_model = RequestPatchUserDto(body)

        try:
            user = user_queries.patch_user(session, request_model, uid)
        except DBUserNotExistExtension:
            raise SanicUserNotFound('User not found')

        response_model = ResponseUserDto(user)
        body = response_model.dump()
        body.pop('id')
        return await self.make_response_json(status=200, body=response_model.dump())
    async def method_post(self, request: Request, body: dict,session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreatemeaasgeDto(body)

        try:
            hashed_password = generate_hash(request_model.password)
        except GeneratePasswordHashException as e:
            raise SanicPasswordHashException(str(e))

        try:
            db_user = user_queries.create_user(session, request_model, hashed_password)
        except DBEmployeeExistException as e:
            raise SanicEmployeeConflictException('Login is busy')
        try:
            session.commit_session()
        except (DBDataException, DBintegrityException) as e:
            raise SanicDBException(str(e))

        response_model = ResponseUserDto(db_user)

        return await self.make_response_json(body=response_model.dump(), status=201)