import re

from modules.shared.models.address import Address, Coordinates
from modules.text_parser.src.constants.coordinates_basel import COORDINATES_MAP_BASEL
from modules.text_parser.src.coordinate_converter import wgs84_to_lv95
from modules.text_parser.src.constants.street_name_keywords import (
    KEYWORDS_STREET_NAME,
)
from modules.shared.constants.tags import TAG_NONE_FOUND


def is_address(text: str) -> bool:
    return any(char.isdigit() for char in text) or any(
        keyword.lower() in text for keyword in KEYWORDS_STREET_NAME
    )


def extract_address(content: str) -> Address:
    house_number = TAG_NONE_FOUND
    street_name = TAG_NONE_FOUND

    house_number_match = re.search(r"([a-zA-Z]*\d+[a-zA-Z]*)", content)

    if house_number_match:
        house_number = house_number_match.group(1).strip()
        street_name = content.replace(house_number, "").strip()

    return Address(street_name=street_name, house_number=house_number, coordinates=None)


def add_coordinates(address: Address) -> Address:
    if (
        address.street_name in COORDINATES_MAP_BASEL
        and address.house_number in COORDINATES_MAP_BASEL[address.street_name]
    ):
        lat = COORDINATES_MAP_BASEL[address.street_name][address.house_number][0]
        lon = COORDINATES_MAP_BASEL[address.street_name][address.house_number][1]
        easting, northing = wgs84_to_lv95(lat, lon)
        address.coordinates = Coordinates(
            latitude_wgs84=lat,
            longitude_wgs84=lon,
            easting_lv95=easting,
            northing_lv95=northing,
        )

    return address
