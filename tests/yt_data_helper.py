from typing import List
from youtube_transcript_api import FetchedTranscript, FetchedTranscriptSnippet

from yt_mcp.transcript.entities import TranscriptLanguage, Transcript, TranscriptMetadata, TranscriptLineItem


class YtDataHelper:
    """Exposes various types of data"""

    VIDEO_ID: str = "tY2njfpWC8g"
    SNIPPET_DURATION: float = 1.5
    START_TIME: float = 0.0

    @staticmethod
    def get_sample_transcript_text(video_id: str) -> str:
        return f"Sample video snippet for {video_id} text".format(video_id=video_id)


class YouTubeTranscriptApiDataHelper:
    """Use this class to create data objects of YoutubeTranscriptApi library"""

    @staticmethod
    def construct_fetched_transcript(video_id: str, language: TranscriptLanguage, record_size: int) -> FetchedTranscript:
        return FetchedTranscript(
            video_id=video_id,
            language=language.value,
            language_code=language.value,
            is_generated=False,
            snippets=YouTubeTranscriptApiDataHelper.construct_fetched_transcript_snippets(
                video_id, record_size),
        )

    @staticmethod
    def construct_fetched_transcript_snippet(video_id: str, start: float, duration: float) -> FetchedTranscriptSnippet:
        return FetchedTranscriptSnippet(
            text=YtDataHelper.get_sample_transcript_text(video_id),
            start=start,
            duration=duration
        )

    @staticmethod
    def construct_fetched_transcript_snippets(video_id: str, number_of_records: int) -> List[FetchedTranscriptSnippet]:
        snippets: List[FetchedTranscriptSnippet] = []
        last_end_time: float = YtDataHelper.START_TIME
        duration: float = YtDataHelper.SNIPPET_DURATION

        for _ in range(number_of_records):
            snippet = YouTubeTranscriptApiDataHelper.construct_fetched_transcript_snippet(
                video_id, last_end_time, last_end_time + duration)
            snippets.append(snippet)
            last_end_time += duration
        return snippets


class YtTranscriptAPIBasedFetcherDataHelper:
    """Use this class to create data objects of YoutubeTranscriptApi library"""

    @staticmethod
    def construct_transcript(video_id: str, language: TranscriptLanguage, record_size: int) -> Transcript:
        metadata: TranscriptMetadata = TranscriptMetadata(
            video_id=video_id,
            language=language,
        )
        transcripts: List[TranscriptLineItem] = YtTranscriptAPIBasedFetcherDataHelper.construct_transcript_line_items(
            video_id, record_size)
        return Transcript(transcripts=transcripts, metadata=metadata)


    @staticmethod
    def construct_transcript_line_item(video_id: str, start_time: float) -> TranscriptLineItem:
        return TranscriptLineItem(
            text=YtDataHelper.get_sample_transcript_text(video_id),
            start_time=start_time)


    @staticmethod
    def construct_transcript_line_items(video_id: str, number_of_line_items: int) -> List[TranscriptLineItem]:
        transcripts = []
        last_start_time: float = YtDataHelper.START_TIME
        duration: float = YtDataHelper.SNIPPET_DURATION
        for _ in range(number_of_line_items):
            line_item: TranscriptLineItem = YtTranscriptAPIBasedFetcherDataHelper.construct_transcript_line_item(
                video_id, last_start_time)
            transcripts.append(line_item)
            last_start_time += duration
        return transcripts