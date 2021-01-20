from marshmallow import fields, Schema, pre_load, post_load
import datetime
from api.base import ResponseDto


class ResponseEmployeeDtoSchema(Schema):
    id = fields.Int(required=True)
    login = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    update_at = fields.DateTime(required=True)
    first_name = fields.Str(required=True)
    position= fields.Str(required=True,allow_none=True)
    department = fields.Str(required=True,allow_none=True)

    @pre_load
    @post_load
    def deserialize_datetime(self, data:dict, *args, **kwargs) -> dict:

        if 'created_at' in data:

            data['created_at'] = self.datetime_to_iso(data['created_at'])

        if 'update_at' in data:

            data['update_at'] = self.datetime_to_iso(data['update_at'])


        return data

    @staticmethod
    def datetime_to_iso(data):
        if isinstance(data,datetime.datetime):
            return data.isoformat()

        return data


class ResponseEmployeeDto(ResponseDto):
    __schema__ = ResponseEmployeeDtoSchema
