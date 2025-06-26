class NextcordException(Exception):
    """Base exception for nextcord."""
    pass

class HTTPException(NextcordException):
    """Raised when an HTTP request fails."""
    pass

class Forbidden(HTTPException):
    """Raised for status code 403."""
    pass

class NotFound(HTTPException):
    """Raised for status code 404."""
    pass

class LoginFailure(NextcordException):
    """Raised when bot token is invalid."""
    pass