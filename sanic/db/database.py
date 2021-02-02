from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import sessionmaker, Session

from db.exceptions import DBintegrityException, DBDataException
from db.models import BaseModel, DBEmployee, DBUser, DBMessage


class DBSession:
    _session: Session

    def __init__(self,session: Session):
        self._session = session

    def query(self, *args, **kwargs):
        return self._session.query(*args, **kwargs)

    def close_session(self):
        self.close_session()

    def add_model(self, model: BaseModel):
        try:
            self._session.add(model)
        except IntegrityError as e:
            raise DBintegrityException(e)
        except DataError as e:
            raise DBDataException(e)

    def get_employee_login(self, login:str) -> DBEmployee:
        return self._session.query(DBEmployee).filter(DBEmployee.login == login).first()

    def get_user_login(self, login:str) -> DBUser:
        return self._session.query(DBUser).filter(DBUser.login == login).first()

    def commit_session(self,need_close:bool= False):
        try:
            self._session.commit()
        except IntegrityError as e:
            raise DBintegrityException(e)
        except DataError as e:
            raise DBDataException(e)

        if need_close:
            self.close_session()

    def get_employee_by_id(self, employee_id:int):
        return self._session.query(DBEmployee).filter(DBEmployee.id == employee_id).first()

    def get_user_by_id(self, user_id:int):
        return self._session.query(DBUser).filter(DBUser.id == user_id).first()

    def get_user_id_by_login(self, login:str):
        return self._session.query(DBUser).filter(DBUser.login == login).first().id

    def get_message(self, message_id):
        return self._session.query(DBMessage).filter(DBMessage.id == message_id).first()


class DataBase:
    connection: Engine
    session_factory: sessionmaker
    _test_query = 'SELECT 1'

    def __init__(self, connection: Engine):
        self.connection = connection
        self.session_factory = sessionmaker(bind=self.connection)

    def check_connection(self):
        self.connection.execute(self._test_query).fetchone()

    def make_session(self) -> DBSession:
        session = self.session_factory()
        return DBSession(session)









