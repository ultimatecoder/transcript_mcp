import pytest

from tests.yt_url_factory import YtURLFactory, YtURLType
from tests.yt_data_helper import YtDataHelper
from transcript_mcp.transcript.utils.yt_url_attribute_extractor import YtURLAttributeExtractorCoordinator

# NOTE: Forced to create class-level static because @pytest.mark.parameterize() do not accept instance variable
_URL_FACTORY = YtURLFactory(YtDataHelper.VIDEO_ID)


class TestYoutubeURLExtractor:

    @pytest.fixture(scope="class")
    @classmethod
    def yt_url_extractor(cls) -> YtURLAttributeExtractorCoordinator:
        return YtURLAttributeExtractorCoordinator()

    @pytest.mark.parametrize("url", [
        _URL_FACTORY.create_url(YtURLType.STANDARD),
        _URL_FACTORY.create_url(YtURLType.SHORT),
        _URL_FACTORY.create_url(YtURLType.WITH_EXTRA_PARAMS),
    ])
    def test_valid_url_extract_video_id_returns_video_id(self, yt_url_extractor: YtURLAttributeExtractorCoordinator,
                                                         url: str) -> None:
        assert yt_url_extractor.extract_video_id(url) == YtDataHelper.VIDEO_ID

    @pytest.mark.parametrize("url", [
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
    ])
    def test_invalid_url_extract_video_id_throws_error(self, yt_url_extractor: YtURLAttributeExtractorCoordinator,
                                                       url: str) -> None:
        with pytest.raises(ValueError):
            yt_url_extractor.extract_video_id(url)