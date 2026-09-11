# SPDX-License-Identifier: MIT

from abc import ABC, abstractmethod
from typing import Optional

from transcript_mcp.transcript.entities import Language, Transcript


class TranscriptProvider(ABC):
    """Use this class to fetch transcript of any video."""

    @abstractmethod
    def provide(self, url: str, language: Optional[Language] = Language.ENGLISH) -> (
            Transcript):
        """Call this method to get a transcript of a video."""
        pass

    @abstractmethod
    def can_provide(self, url: str) -> bool:
        """Call this method to confirm if given provider can provide a transcript against a video or not."""
        pass