import os

import cv2
import numpy as np

from modules.pages_preprocessor.src.cutter.line_operations import extend_line_to_border
from modules.pages_preprocessor.src.cutter.printed_line_detector import (
    get_printed_lines,
)
from modules.pages_preprocessor.src.jpg_preprocessing.blackout_page_borders import (
    crop_around_polygon,
)


def find_header_line(img: np.ndarray) -> np.ndarray:
    img_width, img_height = img.shape[1], img.shape[0]

    all_horizontal_lines = get_printed_lines(img, "horizontal")
    lowest_line = max(all_horizontal_lines, key=lambda line: min(line[1], line[3]))

    header_line = extend_line_to_border(
        lowest_line, img_width, img_height, "horizontal"
    )

    header_topleft = [0, 0]
    header_topright = [img_width, 0]
    header_bottomright = [img_width, header_line[3]]
    header_bottomleft = [0, header_line[1]]

    header_polygon = [
        header_topleft,
        header_topright,
        header_bottomright,
        header_bottomleft,
    ]
    img = crop_around_polygon(img, header_polygon)

    return img


def cut_header(input_folder: str, output_folder: str) -> None:
    all_pages = os.listdir(input_folder)
    for page in all_pages:
        img = cv2.imread(f"{input_folder}/{page}")
        cropped_img = img[0:500, :]
        cropped_img = find_header_line(cropped_img)
        cv2.imwrite(f"{output_folder}/{page}", cropped_img)
