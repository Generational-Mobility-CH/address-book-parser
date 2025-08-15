import os
import re

import cv2
import numpy as np

from modules.pages_preprocessor.src.cutter.line_operations import (
    extend_line_to_border,
    connect_lowest_highest_points,
)
from modules.pages_preprocessor.src.cutter.printed_line_detector import (
    get_printed_lines,
)
from modules.pages_preprocessor.src.jpg_preprocessing.blackout_page_borders import (
    crop_around_polygon,
)


def get_line_lowest_highest(vertical_lines: list) -> tuple:
    points_on_line = []
    for x1, y1, x2, y2 in vertical_lines:
        points_on_line.append((x1, y1))
        points_on_line.append((x2, y2))
    array_points_on_line = np.array(points_on_line)

    highest_point = np.argmax(array_points_on_line[:, 1])
    lowest_point = np.argmin(array_points_on_line[:, 1])
    highest_point_x, highest_point_y = array_points_on_line[highest_point]
    lowest_point_x, lowest_point_y = array_points_on_line[lowest_point]

    line_lowest_highest = (
        lowest_point_x,
        lowest_point_y,
        highest_point_x,
        highest_point_y,
    )
    return line_lowest_highest


def find_column_line(
    img: np.ndarray, column_number: int, column_width: int, pixel_tolerance: int
) -> tuple:
    img_height, img_width = img.shape[0], img.shape[1]
    crop_x1 = (column_number * column_width) - pixel_tolerance
    crop_x2 = (column_number * column_width) + pixel_tolerance
    img_crop = img.copy()
    img_crop = img_crop[:, crop_x1:crop_x2]

    all_vertical_lines = get_printed_lines(img_crop, "vertical")

    points_on_line = []
    for x1, y1, x2, y2 in all_vertical_lines:
        points_on_line.append((x1, y1))
        points_on_line.append((x2, y2))
    array_points_on_line = np.array(points_on_line)

    if array_points_on_line.size > 0:
        line_lowest_highest = connect_lowest_highest_points(array_points_on_line)
        x1, y1, x2, y2 = line_lowest_highest
        x1 += crop_x1
        x2 += crop_x1
        line_lowest_highest = x1, y1, x2, y2
        column_line = extend_line_to_border(
            line_lowest_highest, img_width, img_height, "vertical"
        )
        # x1, y1, x2, y2 = column_line
        # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
    else:
        img_half_width = img_width / 2
        column_line = (img_half_width, 0, img_half_width, img_height)

    return img, column_line


def cut_columns(input_folder: str, output_folder: str, ncols: int) -> None:
    all_pages = os.listdir(input_folder)
    for page in all_pages:
        page_number = int(re.sub(r"\D", "", page))
        # print(page_number)
        img = cv2.imread(f"{input_folder}/{page}")
        img_width, img_height = img.shape[1], img.shape[0]

        col_width = img_width // ncols
        pixel_tolerance = int(round(col_width * 0.2, 0))

        all_column_lines = []
        for column in range(1, ncols):
            img, column_line = find_column_line(img, column, col_width, pixel_tolerance)
            all_column_lines.append(column_line)
        # cv2.imwrite(f"{output_folder}/page{page_number}.jpg", img)

        for i in range(ncols):
            img_column = img.copy()
            if i == 0:
                column_line = all_column_lines[0]

                column_topleft = [0, 0]
                column_topright = [column_line[0], 0]
                column_bottomright = [column_line[2], img_height]
                column_bottomleft = [0, img_height]

            elif i == ncols - 1:
                column_line = all_column_lines[-1]

                column_topleft = [column_line[0], 0]
                column_topright = [img_width, 0]
                column_bottomright = [img_width, img_height]
                column_bottomleft = [column_line[2], img_height]

            else:
                first_column_line = all_column_lines[i - 1]
                second_column_line = all_column_lines[i]

                column_topleft = [first_column_line[0], 0]
                column_topright = [second_column_line[0], 0]
                column_bottomright = [second_column_line[2], img_height]
                column_bottomleft = [first_column_line[2], img_height]

            column_polygon = [
                column_topleft,
                column_topright,
                column_bottomright,
                column_bottomleft,
            ]
            img_column = crop_around_polygon(img_column, column_polygon)

            column_number = i + 1
            cv2.imwrite(
                f"{output_folder}/page{page_number}_{column_number}.jpg", img_column
            )
