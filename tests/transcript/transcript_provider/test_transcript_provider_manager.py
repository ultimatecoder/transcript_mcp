from typing import List
from unittest.mock import Mock

import pytest

from tests.helper.yt_data_helper import YtTranscriptDataHelper
from transcript_mcp.transcript.entities import Transcript, Language
from transcript_mcp.transcript.transcript_provider._transcript_provider import TranscriptProvider
from transcript_mcp.transcript.transcript_provider._transcript_provider_manager import TranscriptProviderManager
from transcript_mcp.transcript.utils._yt_data_helper import YtDataHelper
from tests.helper.yt_data_helper import YtDataHelper as TestYtDataHelper


class TestTranscriptManager:

    @pytest.fixture
    def transcript_provider_manager(self, transcript_provider_registry) -> TranscriptProviderManager:
        return TranscriptProviderManager(transcript_provider_registry)

    @pytest.fixture
    def transcript_provider_registry(
            self, transcript_provider_1: TranscriptProvider, transcript_provider_2: TranscriptProvider) -> List[
        TranscriptProvider]:
        return [
            transcript_provider_1,
            transcript_provider_2
        ]

    @pytest.fixture
    def transcript_provider_1(self) -> TranscriptProvider:
        return Mock(spec=TranscriptProvider)

    @pytest.fixture
    def transcript_provider_2(self) -> TranscriptProvider:
        return Mock(spec=TranscriptProvider)

    @pytest.mark.parametrize("url", YtDataHelper.YT_SHORT_URLS + YtDataHelper.YT_LONG_URLS)
    def test_valid_yt_video_link_get_transcript_provides_transcript(
            self, transcript_provider_manager: TranscriptProviderManager, transcript_provider_1: TranscriptProvider,
            transcript_provider_2: TranscriptProvider, url: str) -> None:
        record_size = 5
        transcript_provider_1.can_provide.return_value = True
        transcript_provider_1.provide.return_value = YtTranscriptDataHelper.construct_transcript(
            TestYtDataHelper.VIDEO_ID, Language.ENGLISH, record_size)

        response: Transcript = transcript_provider_manager.get_transcript(url)
        assert response == YtTranscriptDataHelper.construct_transcript(
            TestYtDataHelper.VIDEO_ID, Language.ENGLISH, record_size)
        transcript_provider_1.can_provide.assert_called_once_with(url=url)
        transcript_provider_1.provide.assert_called_once_with(url=url)
        transcript_provider_2.can_provide.assert_not_called()
        transcript_provider_2.provide.assert_not_called()

    def test_invalid_link_get_transcript_raises_invalid_link_error(
            self, transcript_provider_manager: TranscriptProviderManager) -> None:
        pass

    def test_video_link_from_unsupported_source_get_transcript_provides_transcript(
            self, transcript_provider_manager: TranscriptProviderManager) -> None:
        pass