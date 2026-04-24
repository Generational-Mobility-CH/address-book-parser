from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageChops
from pdf2image import convert_from_path
from tqdm import tqdm


def find_vertical_split(np_img):
    min_split_grad_ratio = 0.05
    h, w = np_img.shape
    _, bw = cv2.threshold(np_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    bw = 255 - bw
    proj = np.sum(bw // 255, axis=0)
    proj_smooth = cv2.GaussianBlur(proj.astype(np.float32), (51, 1), 0)
    proj_smooth = (proj_smooth - proj_smooth.min()) / (np.ptp(proj_smooth) + 1e-9)
    left = int(w * 0.25)
    right = int(w * 0.75)
    middle = proj_smooth[left:right]
    valley_rel = int(np.argmin(middle))
    split_x = left + valley_rel
    margin = int(w * min_split_grad_ratio)
    split_x = max(margin, min(w - margin, split_x))

    return split_x


def autocrop(pimg: Image.Image) -> Image.Image:
    bg = Image.new(pimg.mode, pimg.size, (255, 255, 255))
    diff = ImageChops.difference(pimg, bg)
    bbox = diff.getbbox()

    return pimg.crop(bbox) if bbox else pimg


def process_pdf(path: Path, output_path: Path) -> None:
    base = path.stem
    pages = convert_from_path(path, dpi=300, fmt="jpg")

    for i, pil_img in enumerate(tqdm(pages, desc=base)):
        page_num = i + 1
        rgb = np.array(pil_img)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        split_x = find_vertical_split(gray)
        h, w = gray.shape
        pad = int(0.01 * w)

        left_box = (0, 0, min(split_x + pad, w), h)
        right_box = (max(split_x - pad, 0), 0, w, h)

        left_img = pil_img.crop(left_box)
        right_img = pil_img.crop(right_box)

        left_img = autocrop(left_img).convert("RGB")
        right_img = autocrop(right_img).convert("RGB")

        left_name = output_path / f"{base}_page{page_num:04d}_col1.jpg"
        right_name = output_path / f"{base}_page{page_num:04d}_col2.jpg"

        left_img.save(left_name, quality=95)
        right_img.save(right_name, quality=95)
