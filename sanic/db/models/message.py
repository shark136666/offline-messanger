from sqlalchemy import Column, INT, TEXT

from db.models import BaseModel


class DBMessage(BaseModel):

    __tablename__ = 'messages'

    sender_id = Column(INT, nullable=False,)
    recipient_id = Column(INT, nullable=False,)
    message = Column(TEXT)


