from sqlalchemy import Column, INT, TEXT, BOOLEAN, ForeignKey

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(INT, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    recipient_id = Column(INT, ForeignKey('users.id', ondelete='CASCADE'), nullable=False,)
    message = Column(TEXT)
    is_delete = Column(BOOLEAN(), nullable=False, default=False)


