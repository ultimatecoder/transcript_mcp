# SPDX-License-Identifier: MIT

from typing import List

from transcript_mcp.transcript.entities import Transcript
from transcript_mcp.transcript.transcript_provider._transcript_provider import TranscriptProvider
from transcript_mcp.transcript.errors import NotSupportedError


class TranscriptProviderManager:
    """This manager class is responsible for iterating on received providers and assign request to a provider which
    can fetch transcript for received request url.

    If no provider can fetch transcript, then it raises an error to indicate that it is not supported."""

    def __init__(self, transcript_provider_registry: List[TranscriptProvider]) -> None:
        if (transcript_provider_registry is None) or (len(transcript_provider_registry) == 0):
            raise ValueError("Transcript provider registry can not be null or empty or none")
        self._transcript_provider_registry = transcript_provider_registry

    def get_transcript(self, url: str) -> Transcript:
        if (url is None) or (url == ""):
            raise ValueError("Transcript provider registry can not be null or empty or none")
        for _transcript_provider in self._transcript_provider_registry:
            if _transcript_provider.can_provide(url=url):
                return _transcript_provider.provide(url=url)
        raise NotSupportedError(identifier=url)