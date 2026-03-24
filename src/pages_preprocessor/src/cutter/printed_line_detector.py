import cv2
import numpy as np


def black_white_for_print(img: np.ndarray, linetype: str) -> np.ndarray:
    if linetype == "vertical":
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grey, 100, 200, apertureSize=3)
    else:
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, (40, 1)
        )  # 40 pixels wide, 1 pixel tall
        closed = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel)
        edges = cv2.Canny(closed, 100, 200, apertureSize=3)
    return edges


def select_lines_by_angle_and_length(
    detected_lines: np.ndarray, min_angle: int, max_angle: int, min_line_length: int
) -> list:
    selected_lines = []
    if detected_lines is not None:
        for line in detected_lines:
            x1, y1, x2, y2 = line[0]
            angle = (
                np.arctan2(abs(y2 - y1), abs(x2 - x1)) * 180 / np.pi
            )  ## angle between start and end point
            length = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            if min_angle <= angle <= max_angle and length >= min_line_length:
                selected_lines.append(line[0])
    return selected_lines


def get_printed_lines(img: np.ndarray, linetype: str) -> list:
    img_black_white = black_white_for_print(img, linetype)
    if linetype in ("vertical"):
        min_angle, max_angle = 85, 95
        min_line_length, min_line_length_allowed = 100, 70
        max_line_gap = 5
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
