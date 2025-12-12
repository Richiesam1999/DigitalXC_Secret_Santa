class SecretSantaException(Exception):
    """Base exception for Secret Santa application"""
    pass


class InvalidEmployeeDataException(SecretSantaException):
    """Raised when employee data is invalid"""
    pass


class InsufficientEmployeesException(SecretSantaException):
    """Raised when there are not enough employees"""
    pass


class AssignmentFailedException(SecretSantaException):
    """Raised when assignment generation fails"""
    pass


class DuplicateEmailException(SecretSantaException):
    """Raised when duplicate emails are found"""
    pass
