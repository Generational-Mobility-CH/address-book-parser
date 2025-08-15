import os
import re

import cv2
import numpy as np

from modules.pages_preprocessor.src.cutter.line_operations import (
    extend_line_to_border,
    connect_lowest_highest_points,
)
from modules.pages_preprocessor.src.cutter.printed_line_detector import (
    black_white_for_print,
    select_lines_by_angle_and_length,
)
from sklearn.linear_model import LinearRegression

from modules.pages_preprocessor.src.jpg_preprocessing.get_avg_border_coords import (
    get_avg_coords,
)


def discard_parallel_lines(vertical_lines: list) -> np.ndarray:
    points_on_line = []
    for x1, y1, x2, y2 in vertical_lines:
        points_on_line.append((x1, y1))
        points_on_line.append((x2, y2))
    array_points_on_line = np.array(points_on_line)

    all_points_y = array_points_on_line[:, 1]
    all_points_x = array_points_on_line[:, 0].reshape(-1, 1)
    regression_line = LinearRegression().fit(all_points_y.reshape(-1, 1), all_points_x)

    predicted_values = regression_line.predict(all_points_y.reshape(-1, 1))
    residuals = np.abs(all_points_x - predicted_values)

    inliers = (
        residuals < 2
    )  ## threshold for outliers --> lines consisting of residuals > 2 are dropped
    points_to_keep = array_points_on_line[inliers.flatten()]

    return points_to_keep


def get_iterative_printed_lines(
    img: np.ndarray, linetype: str
) -> list:  ##TODO: change usage to get_printed_lines() --> needs adding an argument max_line_gap to pass
    img_black_white = black_white_for_print(img, linetype)
    if linetype in ("vertical"):
        min_angle, max_angle = 85, 95
        min_line_length, min_line_length_allowed = 100, 70
        max_line_gap = 2
    else:
        min_angle, max_angle = -10, 10
        min_line_length, min_line_length_allowed = 250, 100
        max_line_gap = 200

    while min_line_length >= min_line_length_allowed:
        all_lines = cv2.HoughLinesP(
            image=img_black_white,
            rho=1,
            theta=np.pi / 180,
            threshold=100,
            lines=np.array([]),
            minLineLength=min_line_length,
            maxLineGap=max_line_gap,
        )
        selected_lines = select_lines_by_angle_and_length(
            all_lines, min_angle, max_angle, min_line_length
        )
        if selected_lines:
            break
        min_line_length -= 5
    return selected_lines


def find_multi_column_line(
    img: np.ndarray,
    column_number: int,
    column_width: int,
    pixel_tolerance: int,
    color: tuple,
) -> (
    tuple
):  ##TODO: drop pixel_tolerance arg, as you are now passing it with 0 everywhere
    img_height, img_width = img.shape[0], img.shape[1]
    crop_x1 = (column_number * column_width) - pixel_tolerance
    crop_x2 = (column_number * column_width) + pixel_tolerance
    crop_y2 = int(
        round(img_height * 0.75, 0)
    )  ## 0.75 to look for lines only in upper 75% of page: ignore ads at the bottom
    img_crop = img.copy()
    img_crop = img_crop[0:crop_y2, crop_x1:crop_x2]

    all_vertical_lines = get_iterative_printed_lines(img_crop, "vertical")
    for (
        line
    ) in all_vertical_lines:  ##TODO: delete this code when line drawing not needed
        x1, y1, x2, y2 = line
        x1 += crop_x1
        x2 += crop_x1
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

    if not all_vertical_lines:
        return img, None

    points_of_true_line = discard_parallel_lines(all_vertical_lines)
    if points_of_true_line.size == 0:
        return img, None

    line_lowest_highest = connect_lowest_highest_points(points_of_true_line)

    x1, y1, x2, y2 = line_lowest_highest
    x1 += crop_x1
    x2 += crop_x1
    line_lowest_highest = x1, y1, x2, y2
    column_line = extend_line_to_border(
        line_lowest_highest, img_width, img_height, "vertical"
    )

    x1, y1, x2, y2 = column_line
    column_line_angle = np.arctan2((y2 - y1), (x2 - x1)) * 180 / np.pi
    if column_line_angle < 85 or column_line_angle > 95:
        column_line = None
    else:
        x1, y1, x2, y2 = column_line
        cv2.line(img, (x1, y1), (x2, y2), color, 2)

    column_line = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
    column_line_metadata = {"line": column_line, "angle": column_line_angle}

    return img, column_line_metadata


def detect_multicol_metadata(
    img: np.ndarray, col_width: int, ncols: int, pixel_tolerance: int
) -> tuple:  ##TODO: join with get_multi_columns_metadata
    all_columns_metadata = {}
    for column in range(1, ncols):
        if column == 1:
            color = (0, 0, 255)
        elif column == ncols - 1:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        img, column_line_metadata = find_multi_column_line(
            img, column, col_width, pixel_tolerance, color
        )
        all_columns_metadata[f"column_{column}"] = column_line_metadata

    return img, all_columns_metadata


def get_multi_columns_metadata(
    input_folder: str, output_folder: str, ncols: int
) -> dict:
    all_pages = os.listdir(input_folder)
    multicolumn_metadata = {}
    for page in all_pages:
        page_number = int(re.sub(r"\D", "", page))
        # print(page_number)
        img = cv2.imread(f"{input_folder}/{page}")
        img_width = img.shape[1]

        col_width = img_width // ncols
        pixel_tolerance = int(round(col_width * 0.2, 0))

        img, metadata = detect_multicol_metadata(img, col_width, ncols, pixel_tolerance)

        cv2.imwrite(f"{output_folder}/page{page_number}.jpg", img)
        multicolumn_metadata[page] = metadata

    return multicolumn_metadata


def cut_multi_columns(
    input_folder: str, output_folder: str, ncols: int, metadata: dict
) -> None:
    all_pages = os.listdir(input_folder)
    nlines = ncols - 1

    average_even, average_uneven = get_avg_coords(metadata, [])

    for page in all_pages:
        page_number = int(re.sub(r"\D", "", page))
        img = cv2.imread(f"{input_folder}/{page}")
        img_width, img_height = img.shape[1], img.shape[0]

        page_metadata = metadata[page]

        columns = [f"column_{i}" for i in range(1, ncols)]

        avg_angle_diffs = {}
        for column in columns:
            if page_number % 2 == 0:
                avg_angle = average_even[f"{column}_angle"]
            else:
                avg_angle = average_uneven[f"{column}_angle"]
            diff = avg_angle - 90
            avg_angle_diffs[column] = diff

        page_angle_diffs = {}
        for i, col in enumerate(columns):
            if page_metadata[col] is not None:
                angle = page_metadata[col]["angle"]
                diff = angle - 90
                page_angle_diffs[i] = round(diff, 0)

        if len(page_angle_diffs) > 2:
            signs = [1 if diff > 0 else -1 for diff in page_angle_diffs.values()]
            majority_sign = 1 if signs.count(1) > signs.count(-1) else -1

            for idx, diff in page_angle_diffs.items():
                sign = 1 if diff > 0 else -1
                if sign != majority_sign:
                    page_metadata[columns[idx]] = None

        for column, diff in avg_angle_diffs.items():
            observed_sign = 1 if diff > 0 else -1
            average_sign = 1 if diff > 0 else -1
            if observed_sign != average_sign or abs(diff) > 0.50:
                page_metadata[column] = None

        none_entries = [key for key, value in page_metadata.items() if value is None]
        count_none = len(none_entries)

        if count_none == 0:
            print(f"Page {page_number} all lines already detected")
            continue

        if 0 < count_none < ncols:
            known_columns = {
                i: page_metadata[col]["line"]
                for i, col in enumerate(columns)
                if page_metadata.get(col) is not None
            }
            known_indices = sorted(known_columns.keys())

            adjacent_colwidths_top = []
            adjacent_colwidths_bottom = []

            for i in range(len(known_indices) - 1):
                current_idx = known_indices[i]
                next_idx = known_indices[i + 1]
                if next_idx - current_idx == 1:
                    dist_top = abs(
                        known_columns[next_idx]["x1"] - known_columns[current_idx]["x1"]
                    )
                    dist_bottom = abs(
                        known_columns[next_idx]["x2"] - known_columns[current_idx]["x2"]
                    )

                    adjacent_colwidths_top.append(dist_top)
                    adjacent_colwidths_bottom.append(dist_bottom)

                if adjacent_colwidths_top and adjacent_colwidths_bottom:
                    colwidth_top = sum(adjacent_colwidths_top) / len(
                        adjacent_colwidths_top
                    )
                    colwidth_bottom = sum(adjacent_colwidths_bottom) / len(
                        adjacent_colwidths_bottom
                    )
                elif len(known_indices) >= 2:
                    first_known = known_indices[0]
                    last_known = known_indices[-1]
                    dist_firstlast_top = abs(
                        known_columns[last_known]["x1"]
                        - known_columns[first_known]["x1"]
                    )
                    dist_firstlast_bottom = abs(
                        known_columns[last_known]["x2"]
                        - known_columns[first_known]["x2"]
                    )
                    ncols_middle = last_known - first_known
                    colwidth_top = dist_firstlast_top / ncols_middle
                    colwidth_bottom = dist_firstlast_bottom / ncols_middle
                else:
                    colwidth_top = img_width // ncols
                    colwidth_bottom = img_width // ncols

                missing_indices = [
                    i for i, col in enumerate(columns) if page_metadata[col] is None
                ]

                while missing_indices:
                    progress = False
                    for i, col in enumerate(columns):
                        if page_metadata[col] is None:
                            left_known = [
                                j for j in range(i - 1, -1, -1) if j in known_columns
                            ]
                            right_known = [
                                j for j in range(i + 1, nlines, 1) if j in known_columns
                            ]
                            interpolated = False
                            if len(left_known) >= 2:
                                left_1, left_2 = left_known[0], left_known[1]
                                dist_top = (
                                    known_columns[left_1]["x1"]
                                    - known_columns[left_2]["x1"]
                                )
                                dist_bottom = (
                                    known_columns[left_1]["x2"]
                                    - known_columns[left_2]["x2"]
                                )
                                x_top = known_columns[left_1]["x1"] + dist_top
                                x_bottom = known_columns[left_1]["x2"] + dist_bottom
                                interpolated = True
                            elif len(right_known) >= 2:
                                right_1, right_2 = right_known[0], right_known[1]
                                dist_top = (
                                    known_columns[right_2]["x1"]
                                    - known_columns[right_1]["x1"]
                                )
                                dist_bottom = (
                                    known_columns[right_2]["x2"]
                                    - known_columns[right_1]["x2"]
                                )
                                ncols_middle = right_known[0] - i
                                x_top = (
                                    known_columns[right_1]["x1"]
                                    - dist_top * ncols_middle
                                )
                                x_bottom = (
                                    known_columns[right_1]["x2"]
                                    - dist_bottom * ncols_middle
                                )
                                interpolated = True
                            elif len(left_known) >= 1:
                                prev_known = left_known[0]
                                x_top = known_columns[prev_known]["x1"] + colwidth_top
                                x_bottom = (
                                    known_columns[prev_known]["x2"] + colwidth_bottom
                                )
                                interpolated = True

                            if interpolated:
                                column_line = (
                                    int(round(x_top)),
                                    0,
                                    int(round(x_bottom)),
                                    img_height,
                                )
                                x1, y1, x2, y2 = column_line
                                known_columns[i] = {
                                    "x1": x1,
                                    "y1": y1,
                                    "x2": x2,
                                    "y2": y2,
                                }
                                page_metadata[columns[i]] = {
                                    "x1": x1,
                                    "y1": y1,
                                    "x2": x2,
                                    "y2": y2,
                                }
                                missing_indices.remove(i)
                                progress = True
                                cv2.line(img, (x1, y1), (x2, y2), (255, 16, 240), 2)
                                print(f"Page {page_number}: {columns[i]} interpolated")

                    if not progress:
                        print(
                            f"Page {page_number}: stopping, cannot interpolate columns {missing_indices}"
                        )
            cv2.imwrite(f"{output_folder}/page{page_number}.jpg", img)
        else:
            print(f"Page {page_number} no lines detected")
        # #
        #
        #
        #
        #     else:
        #         dist_top = int(round((page_metadata[f"column_{ncols-1}"][0] - page_metadata["column_1"][0])/2,0))
        #         dist_bottom = int(round((page_metadata[f"column_{ncols-1}"][2] - page_metadata["column_1"][2])/2,0))
        #         x_top = page_metadata["column_1"][0] + dist_top
        #         x_bottom = page_metadata["column_1"][2] + dist_bottom
        #         print(f"Page {page_number} column 2 interpolated")
        #
        #     column_line = (x_top, 0, x_bottom, img_height)
        #     x1, y1, x2, y2 = column_line
        #     cv2.line(img, (x1, y1), (x2, y2), (255, 16, 240), 2)
        #     cv2.imwrite(f"{output_folder}/page{page_number}.jpg", img)
        # elif count_none > 1 and count_none < ncols:
        #     '''
        #     if only one column is detected: use the average distance and add / subtract that from found column
        #     '''
        #     #if "column_1" not in none_entries:
        #     print(f"Page {page_number}: more than 1 col missing")
        # else:
        #     '''
        #     if no column is detected: use the average position of all columns
        #     '''
        #     print(f"Page {page_number}: all columns missing")
