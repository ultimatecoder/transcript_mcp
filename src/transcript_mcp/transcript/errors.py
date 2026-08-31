class _BaseError(Exception):
    """Defines exception that can be retriable after some interval"""

    def __init__(self, identifier: str, error_message: str):
        super().__init__(error_message)
        self.video_id = identifier
        self.error_message = error_message


class RetriableError(_BaseError):
    """Defines exception that can be retriable after some interval"""

    def __init__(self, identifier: str, message: str):
        super().__init__(identifier, message)
        self.is_retriable = True


class NonRetriableError(_BaseError):
    """Defines exceptions are permanent errors and should get the same result even after retry without fixing"""
    def __init__(self, identifier: str, message: str):
        super().__init__(identifier, message)
        self.is_retriable = False


class ServiceUnavailable(RetriableError):
    def __init__(self, identifier: str):
        message = (f"Respective video downloading service is unavailable. Please try after some time. "
                   f"Identifier: {identifier}")
        super().__init__(identifier, message.format(video_id=identifier))


class AuthRequired(NonRetriableError):
    def __init__(self, identifier: str):
        message = (f"To access this video an authentication is required. This video can be an age restricted video or "
                   f"due to any other reasons you are expected to authenticate yourself. Identifier: {identifier}")
        super().__init__(identifier, message.format(video_id=identifier))


class VideoNotFound(NonRetriableError):
    def __init__(self, identifier: str):
        message = f"Request video with id: {identifier} not found."
        super().__init__(identifier, message.format(video_id=identifier))


class TranscriptNotFound(NonRetriableError):
    def __init__(self, identifier: str):
        message = (f"No transcript found for requested video with id {identifier}. Either no transcript is available or "
                   f"transcript with requested language is unavailable")
        super().__init__(identifier, message.format(video_id=identifier))


class UnknownException(NonRetriableError):
    def __init__(self, identifier: str):
        message = f"Unknown exception occurred while accessing video id: {identifier}"
        super().__init__(identifier, message.format(video_id=identifier))


class DataError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidLink(NonRetriableError):
    def __init__(self, identifier: str):
        message = f"Invalid link provided : {identifier}"
        super().__init__(identifier, message.format(identifier=identifier))


class NotSupportedError(NonRetriableError):
    def __init__(self, identifier: str):
        message = f"Transcript feature from received video link is not supported {identifier}"
        super().__init__(identifier, message.format(identifier=identifier))