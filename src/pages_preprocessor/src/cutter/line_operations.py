import numpy as np


def get_lineslope(x1: int, y1: int, x2: int, y2: int) -> float:
    if x2 - x1 == 0:
        slope = float("inf")
    else:
        slope = (y2 - y1) / (x2 - x1)
    return slope


def find_missing_coord(
    line_to_complete: tuple, target_end_of_line: int, linetype: str
) -> int:
    x1, y1, x2, y2 = line_to_complete
    slope = get_lineslope(x1, y1, x2, y2)

    if linetype in ("left", "right", "vertical"):
        if slope == float("inf"):
            searched_coord = x1
        else:
            y2 = target_end_of_line
            searched_coord = int(x1 + (y2 - y1) / slope)

    if linetype in ("top", "bottom", "horizontal"):
        if slope == float("inf"):
            searched_coord = y1
        else:
            x2 = target_end_of_line
            searched_coord = int(y1 + slope * (x2 - x1))
    return searched_coord


def extend_line_to_border(
    line: tuple, img_width: int, img_height: int, bordertype: str
) -> tuple:
    if bordertype in ("top", "bottom", "horizontal"):
        y1 = find_missing_coord(line, 0, bordertype)
        y2 = find_missing_coord(line, img_width, bordertype)
        border = (0, y1, img_width, y2)
    if bordertype in ("left", "right", "vertical"):
        x1 = find_missing_coord(line, 0, bordertype)
        x2 = find_missing_coord(line, img_height, bordertype)
        border = (x1, 0, x2, img_height)
    border = tuple(max(0, coord) for coord in border)
    return border


def line_intersection(line1: tuple, line2: tuple) -> list:
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    px = int(
        round(
            ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4))
            / denominator,
            0,
        )
    )
    py = int(
        round(
            ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4))
            / denominator,
            0,
        )
    )

    return [px, py]


def connect_lowest_highest_points(points_on_line: np.ndarray) -> tuple:
    highest_point = np.argmax(points_on_line[:, 1])
    lowest_point = np.argmin(points_on_line[:, 1])
    highest_point_x, highest_point_y = points_on_line[highest_point]
    lowest_point_x, lowest_point_y = points_on_line[lowest_point]

    line_lowest_highest = (
        lowest_point_x,
        lowest_point_y,
        highest_point_x,
        highest_point_y,
    )
    return line_lowest_highest
