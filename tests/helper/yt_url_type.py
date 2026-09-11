# SPDX-License-Identifier: MIT

from enum import Enum


class YtURLType(Enum):
    """Types of Youtube URLs"""

    STANDARD = "standard"
    SHORT = "short"
    WITH_EXTRA_PARAMS = "with-extra-params"