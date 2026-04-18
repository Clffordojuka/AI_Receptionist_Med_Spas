class AppException(Exception):
    """Base application exception."""


class NotFoundError(AppException):
    """Raised when a requested resource is not found."""


class ValidationError(AppException):
    """Raised when business validation fails."""


class IntegrationError(AppException):
    """Raised when external service integration fails."""