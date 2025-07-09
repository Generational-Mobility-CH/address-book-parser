from typing import Optional, Iterator, List


# TODO: add __str__ and __repr__
class PersonDataParts:
    def __init__(self, first: str, second: str, third: Optional[str] = None):
        self.first = first
        self.second = second
        self.third = third

    def __len__(self) -> int:
        return sum(bool(x) for x in (self.first, self.second, self.third))

    def __str__(self) -> str:
        return f"first={self.first},  second={self.second}, third={self.third}"

    def __repr__(self):
        return f"first={self.first},  second={self.second}, third={self.third}"

    @classmethod
    def from_list(cls, parts: List[str]) -> "PersonDataParts":
        if len(parts) == 2:
            return cls(first=parts[0], second=parts[1])
        elif len(parts) == 3:
            return cls(first=parts[0], second=parts[1], third=parts[2])
        else:
            raise ValueError(f"Expected 2 or 3 parts, got {len(parts)}")

    def __iter__(self) -> Iterator[Optional[str]]:
        yield self.first
        yield self.second

        if self.third is not None:
            yield self.third
