from abc import ABC, abstractmethod
from typing import Dict, Optional

from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript, YouTubeRequestFailed, VideoUnavailable, \
    InvalidVideoId, AgeRestricted, NoTranscriptFound, TranscriptsDisabled

from transcript_mcp.transcript.entities import TranscriptLanguage, Transcript
from transcript_mcp.transcript.errors import ServiceUnavailable, UnknownException, VideoNotFound, AuthRequired, \
    TranscriptNotFound, DataError


class TranscriptFetcher(ABC):
    """Use this class to fetch Youtube transcripts for a vide"""

    @abstractmethod
    def fetch(self, video_id: str, language: Optional[TranscriptLanguage] = TranscriptLanguage.English) -> Transcript:
        pass


class YtTranscriptAPIBasedFetcher(TranscriptFetcher):
    """This class implements transcript fetcher using
    Youtube Transcript API (https://github.com/jdepoix/youtube-transcript-api)"""

    _EXCEPTION_MAPPING: Dict[type[Exception], type[Exception]] = {
        YouTubeRequestFailed: ServiceUnavailable,
        VideoUnavailable: VideoNotFound,
        InvalidVideoId: VideoNotFound,
        AgeRestricted: AuthRequired,
        NoTranscriptFound: TranscriptNotFound,
        TranscriptsDisabled: TranscriptNotFound,
    }

    def __init__(self, youtube_transcript_api: YouTubeTranscriptApi):
        self.yt_transcript_api: YouTubeTranscriptApi = youtube_transcript_api

    def fetch(self, video_id: str, language: Optional[TranscriptLanguage] = TranscriptLanguage.English) -> Transcript:
        try:
            transcript_response: FetchedTranscript = self.yt_transcript_api.fetch(
                video_id=video_id, languages=[language.to_yt_fetched_language_code()])
            return Transcript.from_yt_fetched_transcript(transcript_response)
        except DataError as data_error:
            raise data_error
        except Exception as downstream_exception:
            raise self._EXCEPTION_MAPPING.get(type(downstream_exception), UnknownException)(video_id)