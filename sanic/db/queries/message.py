from typing import List

from api.request import RequestCreateMessageDto, RequestPatchMessageDto
from db.database import DBSession
from db.exceptions import DBUserNotExistExtension
from db.models import DBMessage
from transport.sanic.exceptions import SanicAccessDeniedException


def create_message(session: DBSession, message: RequestCreateMessageDto, sender_id: int) -> DBMessage:
    if session.get_user_login(message.recipient) is None:
        raise DBUserNotExistExtension

    new_message = DBMessage(
        sender_id=sender_id,
        recipient_id=session.get_user_id_by_login(message.recipient),
        message=message.message,
    )
    session.add_model(new_message)
    return new_message


def patch_message(session: DBSession, message: RequestPatchMessageDto, message_id: int, sender_id: int) -> DBMessage:
    db_message = session.get_message(message_id)
    for attr in message.fields:
        if hasattr(message, attr):
            setattr(db_message, attr, getattr(message, attr))

    return db_message


def check_message_author(session: DBSession, message_id: int, sender_id: int) -> bool:
    check_message = session.get_message(message_id)
    if check_message is None or sender_id is not check_message.sender_id:
        raise SanicAccessDeniedException(message='Access denied')
    else:
        return True


def delete_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message(message_id)
    db_message.is_delete = True
    return db_message


def get_message(session: DBSession, message_id: int) -> DBMessage:
    db_message = session.get_message(message_id)
    return db_message


def get_all_messages(session: DBSession, sender_id: int) -> List[DBMessage]:
    return session.get_all_messages(sender_id)

