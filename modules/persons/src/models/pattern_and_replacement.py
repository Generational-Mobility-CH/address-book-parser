from dataclasses import dataclass
from re import Pattern


@dataclass
class PatternAndReplacement:
    pattern: Pattern[str]
    replacement: str
