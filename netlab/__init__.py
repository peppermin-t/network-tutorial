from __future__ import annotations

from pathlib import Path

__version__ = "0.1.0"

_SRC_PACKAGE = Path(__file__).resolve().parents[1] / "src" / "netlab"
if _SRC_PACKAGE.exists():
    __path__.append(str(_SRC_PACKAGE))
