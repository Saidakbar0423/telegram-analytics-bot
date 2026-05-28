class TelegramAnalyticsException(Exception):
    """Base exception for the application"""

    pass


class DatabaseException(TelegramAnalyticsException):
    """Database operation exception"""

    pass


class ParserException(TelegramAnalyticsException):
    """Parser operation exception"""

    pass


class TelegramApiException(TelegramAnalyticsException):
    """Telegram API exception"""

    pass


class AuthenticationException(TelegramAnalyticsException):
    """Authentication exception"""

    pass


class RateLimitException(TelegramAnalyticsException):
    """Rate limit exception"""

    pass


class ValidationException(TelegramAnalyticsException):
    """Validation exception"""

    pass


class NotFoundError(TelegramAnalyticsException):
    """Resource not found exception"""

    pass


class ConflictError(TelegramAnalyticsException):
    """Resource conflict exception"""

    pass