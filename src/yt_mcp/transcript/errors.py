class _BaseError(Exception):
    """Defines exception that can be retriable after some interval"""

    def __init__(self, video_id: str, error_message: str):
        super().__init__(error_message)
        self.video_id = video_id
        self.error_message = error_message


class RetriableError(_BaseError):
    """Defines exception that can be retriable after some interval"""

    def __init__(self, video_id: str, message: str):
        super().__init__(video_id, message)
        self.is_retriable = True


class NonRetriableError(_BaseError):
    """Defines exceptions are permanent errors and should get the same result even after retry without fixing"""
    def __init__(self, video_id: str, message: str):
        super().__init__(video_id, message)
        self.is_retriable = False


class ServiceUnavailable(RetriableError):
    def __init__(self, video_id: str):
        message = (f"Respective video downloading service is unavailable. Please try after some time. "
                   f"Video id: {video_id}")
        super().__init__(video_id, message.format(video_id=video_id))


class AuthRequired(NonRetriableError):
    def __init__(self, video_id: str):
        message = (f"To access this video an authentication is required. This video can be an age restricted video or "
                   f"due to any other reasons you are expected to authenticate yourself. Video id: {video_id}")
        super().__init__(video_id, message.format(video_id=video_id))


class VideoNotFound(NonRetriableError):
    def __init__(self, video_id: str):
        message = f"Request video with id: {video_id} not found."
        super().__init__(video_id, message.format(video_id=video_id))


class TranscriptNotFound(NonRetriableError):
    def __init__(self, video_id: str):
        message = (f"No transcript found for requested video with id {video_id}. Either no transcript is available or "
                   f"transcript with requested language is unavailable")
        super().__init__(video_id, message.format(video_id=video_id))


class UnknownException(NonRetriableError):
    def __init__(self, video_id: str):
        message = f"Unknown exception occurred while accessing video id: {video_id}"
        super().__init__(video_id, message.format(video_id=video_id))


class DataError(Exception):
    def __init__(self, message: str):
        super().__init__(message)