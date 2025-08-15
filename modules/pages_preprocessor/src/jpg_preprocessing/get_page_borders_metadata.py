import os

import cv2
import numpy as np

from modules.pages_preprocessor.src.jpg_preprocessing.border_line_detector import (
    get_lines_for_border,
)
from modules.pages_preprocessor.src.cutter.line_operations import extend_line_to_border


def angle_outside_bounds(angle: float, bordertype: str) -> bool:
    if bordertype in ("top", "bottom"):
        result = abs(angle) > 5
    else:
        result = not (80 >= angle <= 100)
    return result


def select_line_as_border(img: np.ndarray, lines: list, bordertype: str) -> tuple:
    img_width, img_height = img.shape[1], img.shape[0]

    if bordertype == "top":
        sorted_lines = sorted(lines, key=lambda line: min(line[1], line[3]))
    elif bordertype == "bottom":
        sorted_lines = sorted(
            lines, key=lambda line: min(line[1], line[3]), reverse=True
        )
    elif bordertype == "left":
        sorted_lines = sorted(lines, key=lambda line: min(line[0], line[2]))
    elif bordertype == "right":
        sorted_lines = sorted(
            lines, key=lambda line: min(line[0], line[2]), reverse=True
        )

    for i, line in enumerate(sorted_lines):
        extended_border = extend_line_to_border(line, img_width, img_height, bordertype)
        x1, y1, x2, y2 = extended_border
        angle = np.arctan2(abs(y2 - y1), abs(x2 - x1)) * 180 / np.pi

        if not angle_outside_bounds(angle, bordertype):
            return extended_border, angle

    return extended_border, angle


def find_border_inside_area(img: np.ndarray, cut_areas: dict, bordertype: str) -> tuple:
    area = cut_areas[bordertype]

    if bordertype in ("top", "bottom"):
        cropped_img = img[area[0] : area[1], :]
    else:
        cropped_img = img[:, area[0] : area[1]]

    lines = get_lines_for_border(cropped_img, bordertype)
    border, angle = select_line_as_border(cropped_img, lines, bordertype)

    if bordertype in ("bottom"):
        border = (border[0], border[1] + area[0], border[2], border[3] + area[0])
    if bordertype in ("right"):
        border = (border[0] + area[0], border[1], border[2] + area[0], border[3])

    return border, angle


def detect_page_borders(img: np.ndarray, cut_area: dict) -> dict:
    img_width, img_height = img.shape[1], img.shape[0]

    top_border, top_border_angle = find_border_inside_area(img, cut_area, "top")
    bottom_border, bottom_border_angle = find_border_inside_area(
        img, cut_area, "bottom"
    )
    left_border, left_border_angle = find_border_inside_area(img, cut_area, "left")
    right_border, right_border_angle = find_border_inside_area(img, cut_area, "right")

    top_border = {
        "x1": top_border[0],
        "y1": top_border[1],
        "x2": top_border[2],
        "y2": top_border[3],
    }
    bottom_border = {
        "x1": bottom_border[0],
        "y1": bottom_border[1],
        "x2": bottom_border[2],
        "y2": bottom_border[3],
    }
    left_border = {
        "x1": left_border[0],
        "y1": left_border[1],
        "x2": left_border[2],
        "y2": left_border[3],
    }
    right_border = {
        "x1": right_border[0],
        "y1": right_border[1],
        "x2": right_border[2],
        "y2": right_border[3],
    }

    metadata = {
        "size": {"width": img_width, "height": img_height},
        "borders": {
            "top": top_border,
            "bottom": bottom_border,
            "left": left_border,
            "right": right_border,
        },
        "angle": {
            "top": top_border_angle,
            "bottom": bottom_border_angle,
            "left": left_border_angle,
            "right": right_border_angle,
        },
    }
    return metadata


def get_page_borders_metadata(input_folder: str, cut_range: int) -> dict:
    all_pages = os.listdir(input_folder)
    borders_metadata = {}
    for page in all_pages:
        img = cv2.imread(f"{input_folder}/{page}")
        img_height = img.shape[0]
        img_width = img.shape[1]

        cut_area = {
            "top": (0, cut_range),
            "bottom": (img_height - cut_range, img_height),
            "left": (0, cut_range),
            "right": (img_width - cut_range, img_width),
        }
        metadata = detect_page_borders(img, cut_area)

        borders_metadata[page] = metadata
    return borders_metadata
