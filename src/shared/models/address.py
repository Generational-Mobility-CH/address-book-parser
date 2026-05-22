from dataclasses import dataclass
from typing import Optional


@dataclass
class Coordinates:
    latitude_wgs84: float
    longitude_wgs84: float
    easting_lv95: float
    northing_lv95: float


@dataclass
class Address:
    street_name: str
    house_number: str
    coordinates: Optional[Coordinates]
