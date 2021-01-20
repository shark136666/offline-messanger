from marshmallow import Schema, fields

from api.base import ResponseDto


class ResponseUserDtoSchema(Schema):
    pass



class ResponseUserDto(ResponseDto,ResponseUserDtoSchema):
    __schema__ = ResponseUserDtoSchema
