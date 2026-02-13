from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CoordinateSystem(Enum):
    SwissCoordinateSystem = "LV95"
    WorldGeodeticSystem = "WGS84"


@dataclass
class Coordinates:
    coordinates_system: CoordinateSystem
    longitude: float
    latitude: float


@dataclass
class Address:
    street_name: str
    house_number: str
    coordinates: Optional[Coordinates]
