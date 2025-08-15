import os

import cv2
import pandas as pd


def get_mode_img_sizes(image_files: list, filepath: str) -> tuple:
    img_heights = []
    img_widths = []
    for img_file in image_files:
        input_path = f"{filepath}/{img_file}"
        img = cv2.imread(input_path)

        img_heights.append(img.shape[0])
        img_widths.append(img.shape[1])

    mode_img_height = pd.Series(img_heights).mode().iloc[0]
    mode_img_width = pd.Series(img_widths).mode().iloc[0]
    return mode_img_height, mode_img_width


def resize_jpg(input_folder: str) -> None:
    all_pages = os.listdir(input_folder)
    mode_img_height, mode_img_width = get_mode_img_sizes(all_pages, input_folder)
    for page in all_pages:
        img = cv2.imread(f"{input_folder}/{page}")
        img_height = img.shape[0]
        img_width = img.shape[1]

        if img_height != mode_img_height or img_width != mode_img_width:
            target_size = (mode_img_width, mode_img_height)
            img = cv2.resize(img, target_size, interpolation=cv2.INTER_AREA)

            cv2.imwrite(f"{input_folder}/{page}", img)
