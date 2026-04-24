import cv2
import numpy as np


def black_white_for_borders(img: np.ndarray, linetype: str) -> np.ndarray:
    if linetype in ("top", "bottom"):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(grey, 100, 200, apertureSize=3)
    else:
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 10))
        closed = cv2.morphologyEx(grey, cv2.MORPH_CLOSE, kernel)
        blurred = cv2.GaussianBlur(closed, (3, 3), 0)
        edges = cv2.Canny(blurred, threshold1=20, threshold2=60, apertureSize=3)
    return edges


def select_lines_by_angle(
    all_lines: np.ndarray,
    min_angle: int,
    max_angle: int,
    img_width: int,
    img_height: int,
    bordertype: str,
) -> list:
    output_lines = []

    if all_lines is not None:
        for line in all_lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(abs(y2 - y1), abs(x2 - x1)) * 180 / np.pi
            if angle >= min_angle and angle <= max_angle:
                output_lines.append((x1, y1, x2, y2))
    if all_lines is None or len(output_lines) == 0:
        x2 = img_width
        y2 = img_height
        if bordertype == "top":
            output_lines.append((0, 0, x2, 0))
        if bordertype == "bottom":
            output_lines.append((0, y2, x2, y2))
        if bordertype == "left":
            output_lines.append((0, 0, 0, y2))
        if bordertype == "right":
            output_lines.append((x2, 0, x2, y2))
    return output_lines


def get_lines_for_border(img: np.ndarray, bordertype: str) -> list:
    img_black_white = black_white_for_borders(img, bordertype)
    if bordertype in ("top", "bottom"):
        min_angle, max_angle = -5, 5
    else:
        min_angle, max_angle = 80, 100

    all_lines = cv2.HoughLinesP(
        image=img_black_white,
        rho=1,
        theta=np.pi / 180,
        threshold=100,
        lines=np.array([]),
        minLineLength=150,
        maxLineGap=10,
    )
    img_height, img_width = img.shape[0], img.shape[1]
    output_lines = select_lines_by_angle(
        all_lines, min_angle, max_angle, img_width, img_height, bordertype
    )
    return output_lines
