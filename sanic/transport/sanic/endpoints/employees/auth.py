from sanic.request import Request
from sanic.response import BaseHTTPResponse
from transport.sanic.exceptions import SanicEmployeeNotFound,SanicPasswordHashException

from transport.sanic.endpoints import BaseEndpoint
from api.request import RequestCreateUserDto
from db.queries import employee as employees_queries
from db.exceptions import DBEmployeeNotExistExtension
from helpers.password.hash import check_hash,ChekPasswordHashException
from helpers.auth import create_token

class AuthEmployeeEndpoint(BaseEndpoint):
    async def method_post(self, request: Request, body: dict,session, *args, **kwargs) -> BaseHTTPResponse:

        request_model = RequestCreateUserDto(body)

        try:
            db_employee = employees_queries.get_employee(session,login=request_model.login)
        except DBEmployeeNotExistExtension:
            raise SanicEmployeeNotFound('Employee not found')

        try:
            check_hash(request_model.password,db_employee.password)

        except ChekPasswordHashException:
            raise SanicPasswordHashException('Wrong password')

        payload = {
            'edi':db_employee.id,
        }
        response_body = {
            'authorization':create_token(payload)
        }
        return await self.make_response_json(
            body=response_body,
            status=200,

        )


