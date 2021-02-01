from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBEmployeeExistException, DBUserNotExistExtension
from db.models import DBMessage
from transport.sanic.exceptions import SanicUserNotFound


def create_message(session: DBSession, message: RequestCreateMessageDto) -> DBMessage:
    if session.get_user_login(message.recipient) is None:
        raise DBUserNotExistExtension

    new_message = DBMessage(
        sender_id=message.sender_id,
        recipient_id=session.get_user_id_by_login(message.recipient),
        message=message.message,
    )
    session.add_model(new_message)
    return new_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, message_id: int) -> DBMessage:
    db_message = session.get_sender_id(message_id)
    for attr in message.fields:
        if hasattr(message, attr):
            setattr(db_message, attr, getattr(message, attr))

    return db_message




