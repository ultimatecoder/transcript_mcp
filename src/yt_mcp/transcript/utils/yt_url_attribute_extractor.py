from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urlparse, parse_qs
import pygtrie
from pygtrie import PrefixSet


class _YtURLAttributeExtractor(ABC):
    """Use this to drive an attribute from a Youtube URL"""

    @abstractmethod
    def extract_video_id(self, url: str) -> Optional[str]:
        """Derive the 11 character video ID from a Youtube URL"""
        pass

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Confirms if deriving an attribute from a Youtube URL is possible using this class or not"""
        pass


class _YtStandardUrlAttributeExtractor(_YtURLAttributeExtractor):
    """Use this to derive an attribute from a standard Youtube URL.
    For example: https://www.youtube.com/watch?v=abcXyz"""
    _YT_SUPPORTED_URLS: List[str] = [
        "https://youtube.com/watch",
        "http://youtube.com/watch",
        "https://www.youtube.com/watch",
        "http://www.youtube.com/watch",
    ]
    _VIDEO_QUERY_PARAM = "v"
    _PATH_PARAM_WATCH = "/watch"

    def __init__(self):
        self._supported_urls_trie_set: PrefixSet = pygtrie.PrefixSet(factory=pygtrie.CharTrie)
        self._add_supported_urls()

    def _add_supported_urls(self):
        for url in self._YT_SUPPORTED_URLS:
            self._supported_urls_trie_set.add(url)

    def extract_video_id(self, url: str) -> Optional[str]:
        parsed_query_params = parse_qs(urlparse(url).query)
        if ((self._VIDEO_QUERY_PARAM in parsed_query_params) and
                (len(parsed_query_params[self._VIDEO_QUERY_PARAM]) == 1)):
            return parsed_query_params[self._VIDEO_QUERY_PARAM][0]
        raise (ValueError(
            "Given URL {url} is invalid because does not contain required query param {param}.".format(
                url=url, param=self._VIDEO_QUERY_PARAM)))

    def can_handle(self, url: str) -> bool:
        parsed_url = urlparse(url)
        return ((url in self._supported_urls_trie_set) and
                (parsed_url.path == self._PATH_PARAM_WATCH))


class _YtShortUrlAttributeExtractor(_YtURLAttributeExtractor):
    """Use this to derive an attribute from a short Youtube URL.
    For example: https://youtu.be/abcXyz"""

    _YT_SUPPORTED_URLS: List[str] = [
        "https://youtu.be/",
        "http://youtu.be/",
    ]
    _PATH_SEPARATOR: str = "/"

    def __init__(self):
        self._supported_urls_trie_set: PrefixSet = pygtrie.PrefixSet(factory=pygtrie.CharTrie)
        self._add_supported_urls()

    def _add_supported_urls(self):
        for url in self._YT_SUPPORTED_URLS:
            self._supported_urls_trie_set.add(url)

    def extract_video_id(self, url: str) -> Optional[str]:
        parsed_url = urlparse(url)
        path_split = parsed_url.path.split(self._PATH_SEPARATOR)

        if (len(path_split) == 2) and (path_split[-1] != ""):
            return path_split[-1]
        else:
            raise ValueError("Given URL {url} does not contain expected path params.".format(url=url))

    def can_handle(self, url: str) -> bool:
        return url in self._supported_urls_trie_set


class YtURLAttributeExtractorCoordinator:

    # TODO: Add support for "m.youtube.com"
    _YOUTUBE_URL_ATTRIBUTE_DERIVER_REGISTRY: List[_YtURLAttributeExtractor] = [
        _YtStandardUrlAttributeExtractor(),
        _YtShortUrlAttributeExtractor()
    ]

    def extract_video_id(self, url: str) -> str:
        """Extract the 11 character video ID from a Youtube URL."""
        for url_attribute_deriver in self._YOUTUBE_URL_ATTRIBUTE_DERIVER_REGISTRY:
            if url_attribute_deriver.can_handle(url):
                return url_attribute_deriver.extract_video_id(url)
        raise ValueError("Given URL {url} is invalid.".format(url=url))