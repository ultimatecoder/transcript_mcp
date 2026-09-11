# SPDX-License-Identifier: MIT

from typing import List
from youtube_transcript_api import FetchedTranscript, FetchedTranscriptSnippet

from tests.helper.yt_url_factory import YtURLFactory
from tests.helper.yt_url_type import YtURLType
from transcript_mcp.transcript.entities import Language, Transcript, TranscriptMetadata, TranscriptLineItem


class YtDataHelper:
    """Exposes various types of data"""

    VIDEO_ID: str = "tY2njfpWC8g"
    SNIPPET_DURATION: float = 1.5
    START_TIME: float = 0.0
    YT_URL_FACTORY = YtURLFactory(VIDEO_ID)

    VALID_YT_URLS = [
        YT_URL_FACTORY.create_url(YtURLType.STANDARD),
        YT_URL_FACTORY.create_url(YtURLType.SHORT),
        YT_URL_FACTORY.create_url(YtURLType.WITH_EXTRA_PARAMS),
    ]

    INVALID_YT_URLS = [
        "https://vimeo.com/tY2njfpWC8g",
        "",
        "not a url",
        "youtu.be/tY2njfpWC8g",
        "https://www.youtube.com/abc",
        "https://www.youtube.com/watch?x=abcXyz",
        "https://www.youtube.com/watch?v=",
        "https://www.youtube.com?v=abcXyz",
        "https://www.youtube.com?v=",
        "https://www.youtube.com/watchlater?v=tY2njfpWC8g",
        "https://www.youtube.com/watch/extra/path?v=tY2njfpWC8g",
    ]

    @staticmethod
    def get_sample_transcript_text(video_id: str) -> str:
        return f"Sample video snippet for {video_id} text".format(video_id=video_id)


class YouTubeTranscriptApiDataHelper:
    """Use this class to create data objects of YoutubeTranscriptApi library"""

    @staticmethod
    def construct_fetched_transcript(video_id: str, language: Language, record_size: int) -> FetchedTranscript:
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
                video_id, last_end_time, duration)
            snippets.append(snippet)
            last_end_time += duration
        return snippets


class YtTranscriptDataHelper:
    """Use this class to create data objects of YoutubeTranscriptApi library"""

    @staticmethod
    def construct_transcript(video_id: str, language: Language, record_size: int) -> Transcript:
        metadata: TranscriptMetadata = TranscriptMetadata(
            video_id=video_id,
            language=language,
        )
        transcript_line_items: List[TranscriptLineItem] = YtTranscriptDataHelper.construct_transcript_line_items(
            video_id, record_size)
        return Transcript(transcript_line_items=transcript_line_items, metadata=metadata)

    @staticmethod
    def construct_transcript_line_item(video_id: str, start_time: float, duration: float) -> TranscriptLineItem:
        return TranscriptLineItem(
            text=YtDataHelper.get_sample_transcript_text(video_id),
            start_time=start_time,
            duration=duration)

    @staticmethod
    def construct_transcript_line_items(video_id: str, number_of_line_items: int) -> List[TranscriptLineItem]:
        transcripts = []
        last_start_time: float = YtDataHelper.START_TIME
        duration: float = YtDataHelper.SNIPPET_DURATION
        for _ in range(number_of_line_items):
            line_item: TranscriptLineItem = YtTranscriptDataHelper.construct_transcript_line_item(
                video_id, last_start_time, duration)
            transcripts.append(line_item)
            last_start_time += duration
        return transcripts