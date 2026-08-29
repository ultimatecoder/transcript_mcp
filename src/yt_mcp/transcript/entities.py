from dataclasses import dataclass
from enum import Enum
from typing import List

from youtube_transcript_api import FetchedTranscriptSnippet, FetchedTranscript

from yt_mcp.transcript.errors import DataError


class TranscriptLanguage(Enum):
    English = "en"

    @staticmethod
    def from_yt_fetched_language_code(language_code: str) -> TranscriptLanguage:
        if language_code == "en":
            return TranscriptLanguage.English
        raise DataError(f"Invalid language_code: {language_code}")

    def to_yt_fetched_language_code(self) -> str:
        return self.value


@dataclass(frozen=True)
class TranscriptLineItem:
    """Class representing a Youtube Transcript LineItem"""
    start_time: float
    text: str

    @staticmethod
    def from_yt_fetched_transcript_snippet(fetched_transcript_snippet: FetchedTranscriptSnippet) -> TranscriptLineItem:
        error_message = f""
        if fetched_transcript_snippet is None:
            error_message = f"Empty response received from Youtube Transcript. Received: {fetched_transcript_snippet}"
        elif (fetched_transcript_snippet.text is None) or (fetched_transcript_snippet.text == ""):
            error_message = (f"Empty text received from Youtube Transcript. Text can not be empty. "
                             f"Received: {fetched_transcript_snippet}")
        elif fetched_transcript_snippet.start is None:
            error_message = (f"Empty start time received from Youtube Transcript. Start time can not be empty. "
                             f"Received: {fetched_transcript_snippet}")
        if error_message != f"":
            raise DataError(error_message.format(fetched_transcript_snippet=fetched_transcript_snippet))
        return TranscriptLineItem(
            text=fetched_transcript_snippet.text,
            start_time=fetched_transcript_snippet.start
        )


@dataclass(frozen=True)
class TranscriptMetadata:
    video_id: str
    language: TranscriptLanguage = TranscriptLanguage.English

    @staticmethod
    def from_yt_fetched_transcript(fetched_transcript: FetchedTranscript) -> TranscriptMetadata:
        if fetched_transcript is None:
            raise DataError("Empty response received from Youtube Transcript.")
        elif (fetched_transcript.video_id is None) or (fetched_transcript.video_id == ""):
            raise DataError(f"Missing required video id from Youtube Transcript. "
                            f"Received : {fetched_transcript}".format(fetched_transcript=fetched_transcript))

        language = TranscriptLanguage.from_yt_fetched_language_code(fetched_transcript.language_code)
        return TranscriptMetadata(
            video_id=fetched_transcript.video_id,
            language=language
        )


@dataclass(frozen=True)
class Transcript:
    """Class representing a Youtube Transcript"""
    metadata: TranscriptMetadata
    transcripts: List[TranscriptLineItem]

    @staticmethod
    def from_yt_fetched_transcript(fetched_transcript: FetchedTranscript) -> Transcript:
        if fetched_transcript is None:
            raise DataError("Empty response received from Youtube Transcript.")

        metadata = TranscriptMetadata.from_yt_fetched_transcript(fetched_transcript)
        transcripts: List[TranscriptLineItem] = []

        for snippet in fetched_transcript.snippets:
            transcript = TranscriptLineItem.from_yt_fetched_transcript_snippet(snippet)
            transcripts.append(transcript)
        return Transcript(metadata=metadata, transcripts=transcripts)