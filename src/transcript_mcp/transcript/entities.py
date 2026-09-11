# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from enum import Enum
from typing import List


class Language(Enum):
    ENGLISH = "en"


@dataclass(frozen=True)
class TranscriptLineItem:
    """Class representing a Youtube Transcript LineItem"""
    start_time: float
    text: str
    duration: float


@dataclass(frozen=True)
class TranscriptMetadata:
    video_id: str
    language: Language = Language.ENGLISH


@dataclass(frozen=True)
class Transcript:
    """Class representing a Youtube Transcript"""
    metadata: TranscriptMetadata
    transcript_line_items: List[TranscriptLineItem]