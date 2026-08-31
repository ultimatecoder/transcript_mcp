from typing import Dict, List

from youtube_transcript_api import FetchedTranscript, FetchedTranscriptSnippet

from transcript_mcp.transcript.entities import Language, TranscriptMetadata, TranscriptLineItem, Transcript
from transcript_mcp.transcript.errors import DataError


# TODO: Write unit test for each mapper
class LanguageMapper:
    """Use this mapper to map entity to Language entity"""

    _YT_ENGLISH_LANGUAGE_CODE: str= "en"

    _YT_LANGUAGE_CODE_TO_LANGUAGE_MAPPING: Dict[str, Language]= {
        _YT_ENGLISH_LANGUAGE_CODE: Language.ENGLISH,
    }

    _LANGUAGE_MAPPING_TO_YT_LANGUAGE_MAPPING: Dict[Language, str] = {
        Language.ENGLISH: _YT_ENGLISH_LANGUAGE_CODE,
    }

    @staticmethod
    def from_yt_language_code(yt_language_code: str) -> Language:
        if (yt_language_code is None) or (yt_language_code == ""):
            raise ValueError("Youtube Transcript Api language code can not be null or empty")

        if yt_language_code not in LanguageMapper._YT_LANGUAGE_CODE_TO_LANGUAGE_MAPPING:
            raise DataError(f"No mapping found for YouTube transcript Api language_code: {yt_language_code}")
        return LanguageMapper._YT_LANGUAGE_CODE_TO_LANGUAGE_MAPPING.get(yt_language_code)

    @staticmethod
    def to_yt_language_code(language: Language) -> str:
        if language is None:
            raise ValueError("Language code can not be null")
        if language not in LanguageMapper._LANGUAGE_MAPPING_TO_YT_LANGUAGE_MAPPING:
            raise DataError(f"No mapping found for Language : {language}")
        return LanguageMapper._LANGUAGE_MAPPING_TO_YT_LANGUAGE_MAPPING.get(language)


class TranscriptMetadataMapper:
    """Use this mapper to map entity to Transcript Metadata entity"""

    @staticmethod
    def from_yt_fetched_transcript(fetched_transcript: FetchedTranscript) -> TranscriptMetadata:
        if fetched_transcript is None:
            raise ValueError("Empty response received from Youtube Transcript.")
        elif (fetched_transcript.video_id is None) or (fetched_transcript.video_id == ""):
            raise DataError(f"Missing required video id from Youtube Transcript. "
                            f"Received : {fetched_transcript}".format(fetched_transcript=fetched_transcript))

        language = LanguageMapper.from_yt_language_code(fetched_transcript.language_code)
        return TranscriptMetadata(
            video_id=fetched_transcript.video_id,
            language=language
        )


class TranscriptLineItemMapper:
    """Use this mapper to map entity to Transcript LineItem entity"""

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
        elif fetched_transcript_snippet.duration is None:
            error_message = (f"Emtpy duration received from Youtube Transcript. Duration can not be empty. "
                             f"Received : {fetched_transcript_snippet}")
        if error_message != f"":
            raise DataError(error_message.format(fetched_transcript_snippet=fetched_transcript_snippet))
        return TranscriptLineItem(
            text=fetched_transcript_snippet.text,
            start_time=fetched_transcript_snippet.start,
            duration=fetched_transcript_snippet.duration
        )


class TranscriptMapper:
    """Use this mapper to map entity to Transcript entity"""

    @staticmethod
    def from_yt_fetched_transcript(fetched_transcript: FetchedTranscript) -> Transcript:
        if fetched_transcript is None:
            raise DataError("Empty response received from Youtube Transcript.")

        metadata = TranscriptMetadataMapper.from_yt_fetched_transcript(fetched_transcript)
        transcripts_line_items: List[TranscriptLineItem] = []

        for snippet in fetched_transcript.snippets:
            transcript = TranscriptLineItemMapper.from_yt_fetched_transcript_snippet(snippet)
            transcripts_line_items.append(transcript)
        return Transcript(metadata=metadata, transcript_line_items=transcripts_line_items)