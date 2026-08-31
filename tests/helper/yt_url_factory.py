from typing import Dict

from tests.helper.yt_url_type import YtURLType


class YtURLFactory:
    """Use this class to generate different types of Youtube URLs."""

    _YT_URL_REGISTRY: Dict[YtURLType, str] = {
        YtURLType.STANDARD: "https://www.youtube.com/watch?v={video_id}",
        YtURLType.SHORT: "https://youtu.be/{video_id}",
        YtURLType.WITH_EXTRA_PARAMS: "https://www.youtube.com/watch?v={video_id}&t=42s&list=PLxyz",
    }

    def __init__(self, video_id: str) -> None:
        self._video_id = video_id

    def create_url(self, url_type: YtURLType) -> str:
        if url_type not in YtURLFactory._YT_URL_REGISTRY:
            raise ValueError(f"Invalid URL type {url_type}")
        return YtURLFactory._YT_URL_REGISTRY[url_type].format(video_id=self._video_id)