from marshmallow import fields, Schema

from api.base import RequestDto


class RequestCreateMessageDtoSchema(Schema):
    sender_id = fields.Str(required=False)
    recipient = fields.Str(required=True, allow_none=False)
    message = fields.Str(required=True, allow_none=False)


class RequestCreateMessageDto(RequestDto):
    __schema__ = RequestCreateMessageDtoSchema
