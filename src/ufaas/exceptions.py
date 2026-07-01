"""Exception classes for UFaaS application."""

error_messages: dict[str, str] = {}


class UFaaSError(Exception):
    """UFaaSError is a base exception for all UFaaS exceptions."""

    status_code: int = 402
    error_code: str = "insufficient_funds"
    message_en: str = "Insufficient funds"
    message_fa: str | None = "موجودی کافی نیست"

    def __init__(
        self,
        status_code: int,
        error_code: str,
        detail: str | None = None,
        message: dict | None = None,
        **kwargs: object,
    ) -> None:
        """
        Initialize base HTTP exception.

        Args:
            status_code: HTTP status code.
            error_code: Error code string.
            detail: Optional error detail message.
            message: Optional dictionary of language-specific messages.
            **kwargs: Additional error data.

        """
        self.status_code = status_code
        self.error_code = error_code
        if message is None:
            if self.message_en and self.message_fa:
                self.message = {
                    "en": self.message_en,
                    "fa": self.message_fa,
                }
            else:
                self.message = {
                    "en": detail,
                }
        else:
            if isinstance(message, str):
                message = {"en": message}
            self.message = message
        self.detail = detail or str(self.message.get("en"))
        self.data = kwargs
        super().__init__(status_code, detail=detail)


class InsufficientFundsError(UFaaSError):
    """Exception raised for insufficient funds."""

    def __init__(self, detail: str | None = None) -> None:
        """
        Initialize InsufficientFundsError.

        Args:
            detail: Optional detail message
        """
        super().__init__(
            status_code=402, error_code="insufficient_funds", detail=detail
        )


class InvalidRequestError(UFaaSError):
    """Exception raised for invalid requests."""

    def __init__(self, detail: str | None = None) -> None:
        """
        Initialize InvalidRequestError.

        Args:
            detail: Optional detail message
        """
        super().__init__(
            status_code=400, error_code="invalid_request", detail=detail
        )


class UnauthorizedError(UFaaSError):
    """Exception raised for unauthorized access."""

    def __init__(self, detail: str | None = None) -> None:
        """
        Initialize UnauthorizedError.

        Args:
            detail: Optional detail message
        """
        super().__init__(
            status_code=401, error_code="unauthorized", detail=detail
        )


class ForbiddenError(UFaaSError):
    """Exception raised for forbidden access."""

    def __init__(self, detail: str | None = None) -> None:
        """
        Initialize ForbiddenError.

        Args:
            detail: Optional detail message
        """
        super().__init__(
            status_code=403, error_code="forbidden", detail=detail
        )


class NotFoundError(UFaaSError):
    """Exception raised for resources not found."""

    def __init__(self, detail: str | None = None) -> None:
        """
        Initialize NotFoundError.

        Args:
            detail: Optional detail message
        """
        super().__init__(
            status_code=404, error_code="not_found", detail=detail
        )
