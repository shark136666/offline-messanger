from api.request import RequestCreatemeaasgeDto
from db.database import DBSession
from db.exceptions import DBEmployeeExistException, DBUserNotExistExtension
from db.models import DBEmployee


def create_employee(session: DBSession, employee: RequestCreatemeaasgeDto, hashed_password: bytes) -> DBEmployee:
    new_employee = DBEmployee(
        login=employee.login,
        password=hashed_password,
        message=employee.message,
        last_name=employee.last_name,
        department=employee.department,
        position=employee.position,
    )
    if session.get_employee_login(new_employee.login) is not None:
        raise DBEmployeeExistException
    session.add_model(new_employee)
    return new_employee


def get_employee(sesion: DBSession, login: str = str, employee_id: int = None) -> DBEmployee:
    db_employee = None

    if login is not None:
        db_employee = sesion.get_employee_login(login)
    elif employee_id is not None:
        db_employee = sesion.get_employee_by_id(employee_id)

    if db_employee is None:
        raise DBEmployeeExistException

    return db_employee
