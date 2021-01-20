
class PasswordHashException(Exception):
    status_code = 500


class GeneratePasswordHashException(PasswordHashException):
    pass


class ChekPasswordHashException(PasswordHashException):
    pass