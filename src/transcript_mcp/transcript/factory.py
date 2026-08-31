from typing import List

from youtube_transcript_api import YouTubeTranscriptApi

from transcript_mcp.transcript.transcript_provider._transcript_provider_manager import TranscriptProviderManager
from transcript_mcp.transcript.transcript_provider._transcript_provider import TranscriptProvider
from transcript_mcp.transcript.transcript_provider._yt_transcript_provider import YtTranscriptApiBasedProvider
from transcript_mcp.transcript.utils._yt_url_attribute_extractor import YtURLAttributeExtractorCoordinator, \
    YtURLAttributeExtractor, YtStandardUrlAttributeExtractor, YtShortUrlAttributeExtractor


class Factory:

    @staticmethod
    def create_transcript_provider_manager() -> TranscriptProviderManager:
        registry = Factory._create_transcript_provider_registry()
        return TranscriptProviderManager(registry)

    @staticmethod
    def _create_transcript_provider_registry() -> List[TranscriptProvider]:
        registry: List[TranscriptProvider] = [
            Factory._create_yt_transcript_api_based_provider()
        ]

        return registry

    @staticmethod
    def _create_yt_transcript_api_based_provider() -> YtTranscriptApiBasedProvider:
        youtube_transcript_api = Factory._create_youtube_transcript_api()
        yt_url_attribute_extractor_coordinator = Factory._create_yt_url_attribute_extractor_coordinator()

        return YtTranscriptApiBasedProvider(
            youtube_transcript_api=youtube_transcript_api,
            yt_url_attribute_extractor_coordinator=yt_url_attribute_extractor_coordinator)

    @staticmethod
    def _create_youtube_transcript_api() -> YouTubeTranscriptApi:
        return YouTubeTranscriptApi()

    @staticmethod
    def _create_yt_url_attribute_extractor_coordinator() -> YtURLAttributeExtractorCoordinator:
        yt_url_attribute_deriver_registry = Factory._create_yt_url_attribute_extractor_registry()
        return YtURLAttributeExtractorCoordinator(yt_url_attribute_deriver_registry=yt_url_attribute_deriver_registry)

    @staticmethod
    def _create_yt_url_attribute_extractor_registry() -> List[YtURLAttributeExtractor]:
        registry: List[YtURLAttributeExtractor] = [
            Factory._create_yt_standard_url_attribute_extractor(),
            Factory._create_yt_short_url_attribute_extractor()
        ]
        return registry

    @staticmethod
    def _create_yt_standard_url_attribute_extractor() -> YtStandardUrlAttributeExtractor:
        return YtStandardUrlAttributeExtractor()

    @staticmethod
    def _create_yt_short_url_attribute_extractor() -> YtShortUrlAttributeExtractor:
        return YtShortUrlAttributeExtractor()