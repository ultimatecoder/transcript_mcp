from typing import List
from unittest.mock import Mock

import pytest
from tests.helper.yt_data_helper import YtDataHelper
from tests.helper.yt_url_type import YtURLType
from transcript_mcp.transcript.utils._yt_url_attribute_extractor import YtURLAttributeExtractorCoordinator, \
    YtURLAttributeExtractor, YtStandardUrlAttributeExtractor, YtShortUrlAttributeExtractor


class TestYoutubeURLExtractor:

    @pytest.fixture
    def yt_url_extractor(
            self, yt_url_extractor_registry: List[YtURLAttributeExtractor]) -> YtURLAttributeExtractorCoordinator:
        return YtURLAttributeExtractorCoordinator(yt_url_extractor_registry)

    @pytest.fixture
    def yt_url_extractor_registry(self, yt_url_extractor_1: YtURLAttributeExtractor,
                                  yt_url_extractor_2: YtURLAttributeExtractor) -> List[YtURLAttributeExtractor]:
        return [yt_url_extractor_1, yt_url_extractor_2]

    @pytest.fixture
    def yt_url_extractor_1(self) -> YtURLAttributeExtractor:
        return Mock(spec=YtURLAttributeExtractor)

    @pytest.fixture
    def yt_url_extractor_2(self) -> YtURLAttributeExtractor:
        return Mock(spec=YtURLAttributeExtractor)

    @pytest.mark.parametrize("url", YtDataHelper.VALID_YT_URLS)
    def test_valid_url_extract_video_id_returns_video_id(
            self, yt_url_extractor_1: YtURLAttributeExtractor, yt_url_extractor_2: YtURLAttributeExtractor,
            yt_url_extractor: YtURLAttributeExtractorCoordinator, url: str) -> None:
        yt_url_extractor_1.can_handle.return_value = True
        yt_url_extractor_1.extract_video_id.return_value = YtDataHelper.VIDEO_ID

        assert yt_url_extractor.extract_video_id(url) == YtDataHelper.VIDEO_ID
        yt_url_extractor_1.can_handle.assert_called_once_with(url=url)
        yt_url_extractor_1.extract_video_id.assert_called_once_with(url=url)
        yt_url_extractor_2.can_handle.assert_not_called()
        yt_url_extractor_2.extract_video_id.assert_not_called()

    @pytest.mark.parametrize("url", YtDataHelper.INVALID_YT_URLS)
    def test_invalid_url_extract_video_id_throws_error(
            self, yt_url_extractor_1: YtURLAttributeExtractor, yt_url_extractor_2: YtURLAttributeExtractor,
            yt_url_extractor: YtURLAttributeExtractorCoordinator, url: str) -> None:
        yt_url_extractor_1.can_handle.return_value = False
        yt_url_extractor_2.can_handle.return_value = False

        with pytest.raises(ValueError):
            yt_url_extractor.extract_video_id(url)

        yt_url_extractor_1.can_handle.assert_called_once_with(url=url)
        yt_url_extractor_1.extract_video_id.assert_not_called()
        yt_url_extractor_2.can_handle.assert_called_once_with(url=url)
        yt_url_extractor_2.extract_video_id.assert_not_called()


class TestYtStandardUrlAttributeExtractor:

    @pytest.fixture
    def yt_standard_url_extractor(self) -> YtStandardUrlAttributeExtractor:
        return YtStandardUrlAttributeExtractor()

    @pytest.mark.parametrize("url", [
        YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.STANDARD),
        YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.WITH_EXTRA_PARAMS),
    ])
    def test_valid_url_extract_video_id_returns_video_id(
            self, yt_standard_url_extractor: YtStandardUrlAttributeExtractor, url: str) -> None:
        assert yt_standard_url_extractor.extract_video_id(url) == YtDataHelper.VIDEO_ID

    @pytest.mark.parametrize("url", [
        YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.STANDARD),
        YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.WITH_EXTRA_PARAMS),
    ])
    def test_valid_url_can_handle_returns_positive(
            self, yt_standard_url_extractor: YtStandardUrlAttributeExtractor, url: str) -> None:
        assert yt_standard_url_extractor.can_handle(url) == True

    @pytest.mark.parametrize("url", [YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.SHORT)])
    def test_invalid_url_can_handle_returns_negative(
            self, yt_standard_url_extractor: YtStandardUrlAttributeExtractor, url: str) -> None:
        assert yt_standard_url_extractor.can_handle(url) == False


class TestYtShortUrlAttributeExtractor:

    @pytest.fixture
    def yt_short_url_extractor(self) -> YtShortUrlAttributeExtractor:
        return YtShortUrlAttributeExtractor()

    @pytest.mark.parametrize("url", [YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.SHORT)])
    def test_valid_url_extract_video_id_returns_video_id(
            self, yt_short_url_extractor: YtShortUrlAttributeExtractor, url: str) -> None:
        assert yt_short_url_extractor.extract_video_id(url) == YtDataHelper.VIDEO_ID

    @pytest.mark.parametrize("url", [YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.SHORT)])
    def test_valid_url_can_handle_returns_positive(
            self, yt_short_url_extractor: YtShortUrlAttributeExtractor, url: str) -> None:
        assert yt_short_url_extractor.can_handle(url) == True

    @pytest.mark.parametrize("url", YtDataHelper.INVALID_YT_URLS + [
            YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.STANDARD),
            YtDataHelper.YT_URL_FACTORY.create_url(YtURLType.WITH_EXTRA_PARAMS)
    ])
    def test_invalid_url_can_handle_returns_negative(
            self, yt_short_url_extractor: YtShortUrlAttributeExtractor, url: str) -> None:
        assert yt_short_url_extractor.can_handle(url) == False
