import os
import re

import cv2
import numpy as np
import pandas as pd

from modules.pages_preprocessor.src.cutter.line_operations import line_intersection
from modules.pages_preprocessor.src.jpg_preprocessing.get_avg_border_coords import (
    metadata_as_df,
    get_avg_coords,
)


def is_even_page(page: str) -> bool:
    return int(re.sub(r"\D", "", page)) % 2 == 0


def crop_around_polygon(img: np.ndarray, polygon: list[list]) -> np.ndarray:
    points = np.array([polygon], dtype=np.int32)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.drawContours(
        mask, [points], contourIdx=-1, color=255, thickness=-1, lineType=cv2.LINE_AA
    )
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    x, y, w, h = cv2.boundingRect(points)
    cropped_img = masked_img[y : y + h, x : x + w]

    return cropped_img


def update_page_metadata(
    book_metadata: pd.DataFrame, avg_book_metadata: pd.Series, page: str
) -> pd.Series:
    page_metadata_df = book_metadata[book_metadata["page"] == page]
    page_metadata = page_metadata_df.iloc[0]
    page_metadata = page_metadata.drop(["page", "is_even"])
    new_page_metadata = page_metadata.copy()

    diff_page_book_metadata = (page_metadata - avg_book_metadata).abs()

    new_page_metadata[diff_page_book_metadata > 25] = avg_book_metadata[
        diff_page_book_metadata > 25
    ]
    new_page_metadata = new_page_metadata.astype(int)

    return new_page_metadata


def blackout_page_borders(
    input_folder: str, output_folder: str, borders_metadata: dict
) -> None:
    all_pages = os.listdir(input_folder)

    avg_even_page, avg_uneven_page = get_avg_coords(
        borders_metadata,
        ["angle_top", "angle_bottom", "angle_left", "angle_right", "digits"],
    )
    avg_even_page = avg_even_page.round(0).astype(int)
    avg_uneven_page = avg_uneven_page.round(0).astype(int)

    borders_metadata_df = metadata_as_df(borders_metadata)
    borders_metadata_df = borders_metadata_df.drop(
        columns=["angle_top", "angle_bottom", "angle_left", "angle_right", "digits"]
    )

    all_output_pages = borders_metadata_df["page"].values

    for page in all_pages:
        img = cv2.imread(f"{input_folder}/{page}")

        page_is_even = is_even_page(page)
        if page_is_even:
            book_avg_series = avg_even_page
        else:
            book_avg_series = avg_uneven_page

        page_metadata_new = update_page_metadata(
            borders_metadata_df, book_avg_series, page
        )

        if page not in all_output_pages:
            page_metadata_new = book_avg_series.copy()

        ## TODO: serialize?
        top_border = (
            (page_metadata_new["borders_top_x1"], page_metadata_new["borders_top_y1"]),
            (page_metadata_new["borders_top_x2"], page_metadata_new["borders_top_y2"]),
        )
        bottom_border = (
            (
                page_metadata_new["borders_bottom_x1"],
                page_metadata_new["borders_bottom_y1"],
            ),
            (
                page_metadata_new["borders_bottom_x2"],
                page_metadata_new["borders_bottom_y2"],
            ),
        )
        left_border = (
            (
                page_metadata_new["borders_left_x1"],
                page_metadata_new["borders_left_y1"],
            ),
            (
                page_metadata_new["borders_left_x2"],
                page_metadata_new["borders_left_y2"],
            ),
        )
        right_border = (
            (
                page_metadata_new["borders_right_x1"],
                page_metadata_new["borders_right_y1"],
            ),
            (
                page_metadata_new["borders_right_x2"],
                page_metadata_new["borders_right_y2"],
            ),
        )

        page_topleft = line_intersection(
            top_border, left_border
        )  ## same logic would apply with intersection between lines and file borders (e.g. (0,0),(0,img_width))
        page_topright = line_intersection(top_border, right_border)
        page_bottomleft = line_intersection(bottom_border, left_border)
        page_bottomright = line_intersection(bottom_border, right_border)

        page_polygon = [page_topleft, page_topright, page_bottomright, page_bottomleft]

        img = crop_around_polygon(img, page_polygon)

        cv2.imwrite(f"{output_folder}/{page}", img)
