from pyproj import Transformer

_transformer = Transformer.from_crs("EPSG:4326", "EPSG:2056", always_xy=False)


def wgs84_to_lv95(latitude: float, longitude: float) -> tuple[float, float]:
    """Convert WGS84 (lat, lon) to LV95 (easting, northing)."""
    easting, northing = _transformer.transform(latitude, longitude)
    return easting, northing
