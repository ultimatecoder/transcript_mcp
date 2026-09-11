# SPDX-License-Identifier: MIT

from unittest.mock import Mock

import pytest
from requests import HTTPError
from youtube_transcript_api import (YouTubeRequestFailed, VideoUnavailable, InvalidVideoId, AgeRestricted,
                                    YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled)

from tests.helper.yt_url_type import YtURLType
from transcript_mcp.transcript.entities import Language, Transcript
from transcript_mcp.transcript.errors import ServiceUnavailable, VideoNotFound, AuthRequired, TranscriptNotFound
from transcript_mcp.transcript.transcript_provider._mappers import LanguageMapper
from transcript_mcp.transcript.transcript_provider._yt_transcript_provider import YtTranscriptApiBasedProvider
from tests.helper.yt_data_helper import YtDataHelper, YouTubeTranscriptApiDataHelper, YtTranscriptDataHelper
from transcript_mcp.transcript.utils._yt_url_attribute_extractor import YtURLAttributeExtractorCoordinator


class TestYtTranscriptAPIBasedFetcher:
    _SAMPLE_SNIPPET_RECORD_SIZE: int = 5

    @pytest.fixture
    def mock_youtube_transcript_api(self):
        return Mock(spec=YouTubeTranscriptApi)

    @pytest.fixture
    def mock_yt_attribute_extractor_coordinator(self):
        return Mock(spec=YtURLAttributeExtractorCoordinator)

    @pytest.fixture
    def yt_transcript_provider(self, mock_youtube_transcript_api: YouTubeTranscriptApi,
                               mock_yt_attribute_extractor_coordinator: YtURLAttributeExtractorCoordinator) \
            -> YtTranscriptApiBasedProvider:
        return YtTranscriptApiBasedProvider(mock_youtube_transcript_api, mock_yt_attribute_extractor_coordinator)

    def test_valid_video_url_provide_response(
            self, yt_transcript_provider: YtTranscriptApiBasedProvider,
            mock_youtube_transcript_api: YouTubeTranscriptApi,
            mock_yt_attribute_extractor_coordinator: YtURLAttributeExtractorCoordinator) -> None:
        url = YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.STANDARD)
        mock_yt_attribute_extractor_coordinator.extract_video_id.return_value = YtDataHelper.VIDEO_ID
        mock_youtube_transcript_api.fetch.return_value = (
            YouTubeTranscriptApiDataHelper.construct_fetched_transcript(
                YtDataHelper.VIDEO_ID, Language.ENGLISH, self._SAMPLE_SNIPPET_RECORD_SIZE))

        response: Transcript = yt_transcript_provider.provide(url)

        assert response == YtTranscriptDataHelper.construct_transcript(
            video_id=YtDataHelper.VIDEO_ID, language=Language.ENGLISH,
            record_size=self._SAMPLE_SNIPPET_RECORD_SIZE)
        mock_youtube_transcript_api.fetch.assert_called_once_with(
            video_id=YtDataHelper.VIDEO_ID, languages=[LanguageMapper.to_yt_language_code(Language.ENGLISH)],)
        mock_yt_attribute_extractor_coordinator.extract_video_id.assert_called_once_with(url=url)

    def test_valid_video_url_provide_with_language_response(
            self, yt_transcript_provider: YtTranscriptApiBasedProvider,
            mock_youtube_transcript_api: YouTubeTranscriptApi,
            mock_yt_attribute_extractor_coordinator: YtURLAttributeExtractorCoordinator) -> None:
        url = YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.STANDARD)
        mock_youtube_transcript_api.fetch.return_value = (
            YouTubeTranscriptApiDataHelper.construct_fetched_transcript(
                YtDataHelper.VIDEO_ID, Language.ENGLISH, self._SAMPLE_SNIPPET_RECORD_SIZE))
        mock_yt_attribute_extractor_coordinator.extract_video_id.return_value = YtDataHelper.VIDEO_ID


        response: Transcript = yt_transcript_provider.provide(url=url, language=Language.ENGLISH)

        mock_youtube_transcript_api.fetch.assert_called_once_with(
            video_id=YtDataHelper.VIDEO_ID, languages=[LanguageMapper.to_yt_language_code(Language.ENGLISH)],)
        mock_yt_attribute_extractor_coordinator.extract_video_id(url=url)
        assert response == YtTranscriptDataHelper.construct_transcript(
            video_id=YtDataHelper.VIDEO_ID, language=Language.ENGLISH,
            record_size=self._SAMPLE_SNIPPET_RECORD_SIZE)

    @pytest.mark.parametrize("downstream_exception, translated_exception_type, is_retriable", [
        (YouTubeRequestFailed(video_id=YtDataHelper.VIDEO_ID, http_error=HTTPError()), ServiceUnavailable, True),
        (VideoUnavailable(video_id=YtDataHelper.VIDEO_ID), VideoNotFound, False),
        (InvalidVideoId(video_id=YtDataHelper.VIDEO_ID), VideoNotFound, False),
        (AgeRestricted(video_id=YtDataHelper.VIDEO_ID), AuthRequired, False),
        (NoTranscriptFound(video_id=YtDataHelper.VIDEO_ID, requested_language_codes=[Language.ENGLISH.value],
                           transcript_data="sample transcript data"), TranscriptNotFound, False),
        (TranscriptsDisabled(video_id=YtDataHelper.VIDEO_ID), TranscriptNotFound, False),
    ])
    def test_valid_video_url_but_exception_from_downstream_provide_throws_translated_error(
            self, yt_transcript_provider: YtTranscriptApiBasedProvider,
            mock_youtube_transcript_api: YouTubeTranscriptApi,
            mock_yt_attribute_extractor_coordinator: YtURLAttributeExtractorCoordinator,
            downstream_exception: Exception, translated_exception_type: type[Exception], is_retriable: bool) -> None:
        url = YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.STANDARD)
        mock_yt_attribute_extractor_coordinator.extract_video_id.return_value = YtDataHelper.VIDEO_ID
        mock_youtube_transcript_api.fetch.side_effect = downstream_exception

        with pytest.raises(translated_exception_type) as translated_exception_info:
            yt_transcript_provider.provide(url)

        translated_exception_obj = translated_exception_info.value
        assert translated_exception_obj.is_retriable == is_retriable
        mock_youtube_transcript_api.fetch.assert_called_once_with(
            video_id=YtDataHelper.VIDEO_ID, languages=[LanguageMapper.to_yt_language_code(Language.ENGLISH)],)
        mock_yt_attribute_extractor_coordinator.extract_video_id(url=url)

    @pytest.mark.parametrize("url", YtDataHelper.VALID_YT_URLS)
    def test_valid_yt_url_can_provide_positive_response(self, yt_transcript_provider: YtTranscriptApiBasedProvider,
                                                        mock_youtube_transcript_api: YouTubeTranscriptApi,
                                                        url: str) -> None:
        response = yt_transcript_provider.can_provide(url=url)
        assert response == True
        mock_youtube_transcript_api.fetch.assert_not_called()

    @pytest.mark.parametrize("url", [
        "https://vimeo.com/347119375",
        "https://www.dailymotion.com/video/xb1kkj2"
    ])
    def test_invalid_yt_url_can_provide_negative_response(self, yt_transcript_provider: YtTranscriptApiBasedProvider,
                                                        mock_youtube_transcript_api: YouTubeTranscriptApi,
                                                        url: str) -> None:
        response = yt_transcript_provider.can_provide(url=url)
        assert response == False
        mock_youtube_transcript_api.fetch.assert_not_called()
