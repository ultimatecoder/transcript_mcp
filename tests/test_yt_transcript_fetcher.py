from unittest.mock import Mock

import pytest
from requests import HTTPError
from youtube_transcript_api import (YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, AgeRestricted,
                                    YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled)

from transcript_mcp.transcript.entities import TranscriptLanguage, Transcript
from transcript_mcp.transcript.errors import ServiceUnavailable, VideoNotFound, AuthRequired, TranscriptNotFound
from transcript_mcp.transcript.transcript_fetcher.transcript_fetcher import YtTranscriptAPIBasedFetcher
from tests.yt_data_helper import YtDataHelper, YouTubeTranscriptApiDataHelper, YtTranscriptAPIBasedFetcherDataHelper


class TestYtTranscriptAPIBasedFetcher:
    _SAMPLE_SNIPPET_RECORD_SIZE: int = 5

    @pytest.fixture
    def mock_youtube_transcript_api(self):
        return Mock(spec=YouTubeTranscriptApi)

    @pytest.fixture
    def yt_transcript_fetcher(self, mock_youtube_transcript_api: YouTubeTranscriptApi) -> YtTranscriptAPIBasedFetcher:
        return YtTranscriptAPIBasedFetcher(mock_youtube_transcript_api)

    def test_valid_video_id_fetch_response(self, yt_transcript_fetcher: YtTranscriptAPIBasedFetcher,
                                           mock_youtube_transcript_api: YouTubeTranscriptApi) -> None:
        mock_youtube_transcript_api.fetch.return_value = (
            YouTubeTranscriptApiDataHelper.construct_fetched_transcript(
                YtDataHelper.VIDEO_ID, TranscriptLanguage.English, self._SAMPLE_SNIPPET_RECORD_SIZE))

        response: Transcript = yt_transcript_fetcher.fetch(YtDataHelper.VIDEO_ID)

        mock_youtube_transcript_api.fetch.assert_called_once_with(
            video_id=YtDataHelper.VIDEO_ID, languages=[TranscriptLanguage.English.to_yt_fetched_language_code()])
        assert response == YtTranscriptAPIBasedFetcherDataHelper.construct_transcript(
            video_id=YtDataHelper.VIDEO_ID, language=TranscriptLanguage.English,
            record_size=self._SAMPLE_SNIPPET_RECORD_SIZE)

    def test_valid_video_id_fetch_with_language_response(self, yt_transcript_fetcher: YtTranscriptAPIBasedFetcher,
                                                         mock_youtube_transcript_api: YouTubeTranscriptApi) -> None:
        mock_youtube_transcript_api.fetch.return_value = (
            YouTubeTranscriptApiDataHelper.construct_fetched_transcript(
                YtDataHelper.VIDEO_ID, TranscriptLanguage.English, self._SAMPLE_SNIPPET_RECORD_SIZE))

        response: Transcript = yt_transcript_fetcher.fetch(video_id=YtDataHelper.VIDEO_ID,
                                                           language=TranscriptLanguage.English)

        mock_youtube_transcript_api.fetch.assert_called_once_with(
            video_id=YtDataHelper.VIDEO_ID, languages=[TranscriptLanguage.English.to_yt_fetched_language_code()])
        assert response == YtTranscriptAPIBasedFetcherDataHelper.construct_transcript(
            video_id=YtDataHelper.VIDEO_ID, language=TranscriptLanguage.English,
            record_size=self._SAMPLE_SNIPPET_RECORD_SIZE)

    @pytest.mark.parametrize("downstream_exception, translated_exception_type, is_retriable", [
        (YouTubeRequestFailed(video_id=YtDataHelper.VIDEO_ID, http_error=HTTPError()), ServiceUnavailable, True),
        (VideoUnavailable(video_id=YtDataHelper.VIDEO_ID), VideoNotFound, False),
        (InvalidVideoId(video_id=YtDataHelper.VIDEO_ID), VideoNotFound, False),
        (AgeRestricted(video_id=YtDataHelper.VIDEO_ID), AuthRequired, False),
        (NoTranscriptFound(video_id=YtDataHelper.VIDEO_ID, requested_language_codes=[TranscriptLanguage.English.value],
                           transcript_data="sample transcript data"), TranscriptNotFound, False),
        (TranscriptsDisabled(video_id=YtDataHelper.VIDEO_ID), TranscriptNotFound, False),
    ])
    def test_valid_video_id_but_service_unavailable_fetch_throws_service_unavailable_error(
            self, yt_transcript_fetcher: YtTranscriptAPIBasedFetcher, mock_youtube_transcript_api: YouTubeTranscriptApi,
            downstream_exception: Exception, translated_exception_type: type[Exception], is_retriable: bool) -> None:
        mock_youtube_transcript_api.fetch.side_effect = downstream_exception

        with pytest.raises(translated_exception_type) as translated_exception_info:
            yt_transcript_fetcher.fetch(YtDataHelper.VIDEO_ID)

        translated_exception_obj = translated_exception_info.value
        assert translated_exception_obj.is_retriable == is_retriable
        mock_youtube_transcript_api.fetch.assert_called_once_with(
            video_id=YtDataHelper.VIDEO_ID, languages=[TranscriptLanguage.English.to_yt_fetched_language_code()])
