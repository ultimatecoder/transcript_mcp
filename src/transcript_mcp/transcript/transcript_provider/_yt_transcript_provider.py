# SPDX-License-Identifier: MIT

from typing import Dict, Optional

import pygtrie
from pygtrie import PrefixSet

from transcript_mcp.transcript.entities import Language, Transcript
from transcript_mcp.transcript.transcript_provider._mappers import TranscriptMapper, LanguageMapper
from transcript_mcp.transcript.transcript_provider._transcript_provider import TranscriptProvider
from transcript_mcp.transcript.errors import ServiceUnavailable, UnknownException, VideoNotFound, AuthRequired, \
    TranscriptNotFound, DataError
from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript, YouTubeRequestFailed, VideoUnavailable, \
    InvalidVideoId, AgeRestricted, NoTranscriptFound, TranscriptsDisabled

from transcript_mcp.transcript.utils._yt_data_helper import YtDataHelper
from transcript_mcp.transcript.utils._yt_url_attribute_extractor import YtURLAttributeExtractorCoordinator


class YtTranscriptApiBasedProvider(TranscriptProvider):
    """This class implements transcript fetcher using
    Youtube Transcript API (https://github.com/jdepoix/youtube-transcript-api)"""

    _EXCEPTION_MAPPING: Dict[type[Exception], type[Exception]] = {
        YouTubeRequestFailed: ServiceUnavailable,
        VideoUnavailable: VideoNotFound,
        InvalidVideoId: VideoNotFound,
        AgeRestricted: AuthRequired,
        NoTranscriptFound: TranscriptNotFound,
        TranscriptsDisabled: TranscriptNotFound,
    }

    def __init__(self, youtube_transcript_api: YouTubeTranscriptApi,
                 yt_url_attribute_extractor_coordinator: YtURLAttributeExtractorCoordinator):
        self._yt_transcript_api: YouTubeTranscriptApi = youtube_transcript_api
        self._yt_url_attribute_extractor_coordinator = yt_url_attribute_extractor_coordinator
        self._supported_urls_trie_set: PrefixSet = pygtrie.PrefixSet(factory=pygtrie.CharTrie)
        self._add_supported_urls()

    def _add_supported_urls(self):
        for url in YtDataHelper.YT_SHORT_URLS + YtDataHelper.YT_LONG_URLS:
            self._supported_urls_trie_set.add(url)

    def provide(self, url: str, language: Optional[Language] = Language.ENGLISH)\
            -> Transcript:
        video_id:str = self._yt_url_attribute_extractor_coordinator.extract_video_id(url=url)
        try:
            transcript_response: FetchedTranscript = self._yt_transcript_api.fetch(
                video_id=video_id, languages=[LanguageMapper.to_yt_language_code(language=language)],)
            return TranscriptMapper.from_yt_fetched_transcript(transcript_response)
        except DataError as data_error:
            raise data_error
        except Exception as downstream_exception:
            raise self._EXCEPTION_MAPPING.get(type(downstream_exception), UnknownException)(url)

    def can_provide(self, url: str) -> bool:
        return url in self._supported_urls_trie_set