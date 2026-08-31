from abc import ABC, abstractmethod
from typing import List, Optional
from urllib.parse import urlparse, parse_qs
import pygtrie
from pygtrie import PrefixSet

from transcript_mcp.transcript.utils._yt_data_helper import YtDataHelper


class YtURLAttributeExtractor(ABC):
    """Use this to drive an attribute from a Youtube URL"""

    @abstractmethod
    def extract_video_id(self, url: str) -> Optional[str]:
        """Derive the 11 character video ID from a Youtube URL"""
        pass

    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Confirms if deriving an attribute from a Youtube URL is possible using this class or not"""
        pass


class YtStandardUrlAttributeExtractor(YtURLAttributeExtractor):
    """Use this to derive an attribute from a standard Youtube URL.
    For example: https://www.youtube.com/watch?v=abcXyz"""
    _VIDEO_QUERY_PARAM = "v"
    _PATH_PARAM_WATCH = "/watch"

    def __init__(self):
        self._supported_urls_trie_set: PrefixSet = pygtrie.PrefixSet(factory=pygtrie.CharTrie)
        self._add_supported_urls()

    def _add_supported_urls(self):
        for url in YtDataHelper.YT_LONG_URLS:
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


class YtShortUrlAttributeExtractor(YtURLAttributeExtractor):
    """Use this to derive an attribute from a short Youtube URL.
    For example: https://youtu.be/abcXyz"""

    _PATH_SEPARATOR: str = "/"

    def __init__(self):
        self._supported_urls_trie_set: PrefixSet = pygtrie.PrefixSet(factory=pygtrie.CharTrie)
        self._add_supported_urls()

    def _add_supported_urls(self):
        for url in YtDataHelper.YT_SHORT_URLS:
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

    def __init__(self, yt_url_attribute_deriver_registry) -> None:
        if (yt_url_attribute_deriver_registry is None) or (len(yt_url_attribute_deriver_registry) == 0):
            raise ValueError("yt_url_attribute_deriver_registry can not be null or empty")
        self._yt_url_attribute_deriver_registry = yt_url_attribute_deriver_registry

    def extract_video_id(self, url: str) -> str:
        """Extract the 11 character video ID from a Youtube URL."""
        for url_attribute_deriver in self._yt_url_attribute_deriver_registry:
            if url_attribute_deriver.can_handle(url=url):
                return url_attribute_deriver.extract_video_id(url=url)
        raise ValueError("Given URL {url} is invalid.".format(url=url))