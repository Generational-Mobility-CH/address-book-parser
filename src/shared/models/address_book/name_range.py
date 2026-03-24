from dataclasses import dataclass


@dataclass
class NameRange:
    start: str = ""
    end: str = ""

    def __len__(self) -> int:
        return sum(bool(x) for x in (self.start, self.end))

    def __repr__(self):
        return f"[start={self.start}, end={self.end}]"
