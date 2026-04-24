"""
Orchestrate dots.ocr-1.5 transcription for a directory of column images.

Groups lcol/rcol images by page number, transcribes each column,
and writes legacy JSON files compatible with the main parsing pipeline.
Supports file-based caching, anomaly detection, and concurrent processing.
"""
import json
import logging
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path

from src.transcriptor.src.api_dots_ocr.anomaly_detector import AnomalyDetector
from src.transcriptor.src.api_dots_ocr.format_converter import count_entries
from src.transcriptor.src.api_dots_ocr.transcribe import transcribe_image_raw

logger = logging.getLogger(__name__)

# Matches column image filenames like "lcol_page123.jpg" or "rcol_page0456.jpg"
_IMAGE_PATTERN = re.compile(r"^(lcol|rcol)_page(\d+)\.jpg$")


@dataclass
class TranscriptionResult:
    written: list[Path] = field(default_factory=list)
    skipped_cached: list[Path] = field(default_factory=list)
    anomalies: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def _group_images_by_page(
    image_dir: Path,
) -> dict[int, dict[str, Path]]:
    """Group lcol/rcol images by page number.

    Returns {page_num: {"lcol": Path, "rcol": Path}}.
    """
    pages: dict[int, dict[str, Path]] = {}
    for img_path in sorted(image_dir.glob("*.jpg")):
        m = _IMAGE_PATTERN.match(img_path.name)
        if not m:
            continue
        col_type = m.group(1)
        page_num = int(m.group(2))
        if page_num not in pages:
            pages[page_num] = {}
        pages[page_num][col_type] = img_path
    return dict(sorted(pages.items()))


def transcribe_to_legacy_json(
    image_dir: Path,
    output_dir: Path,
    api_key: str,
    base_url: str,
    anomaly_detector: AnomalyDetector | None = None,
    max_workers: int = 4,
) -> TranscriptionResult:
    """Process all column images in image_dir, write legacy JSON files.

    Args:
        image_dir: Directory containing lcol_pageNNN.jpg / rcol_pageNNN.jpg
        output_dir: Where to write page_NNNN.json files
        api_key: dots.ocr API key
        base_url: dots.ocr API base URL
        anomaly_detector: Optional anomaly detector for entry count monitoring
        max_workers: Number of concurrent transcription threads (default: 4)

    Returns:
        TranscriptionResult with lists of written files, cached skips,
        anomalies, and errors.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir = output_dir / "raw"
    raw_dir.mkdir(exist_ok=True)
    pages = _group_images_by_page(image_dir)
    total_pages = len(pages)
    result = TranscriptionResult()
    lock = threading.Lock()

    logger.info(
        "Starting transcription: %d pages from %s (workers=%d)",
        total_pages,
        image_dir,
        max_workers,
    )

    # Filter cached pages before submitting to executor
    pages_to_process = {}
    for page_num, columns in pages.items():
        output_file = output_dir / f"page_{page_num:04d}.json"
        if output_file.exists():
            result.skipped_cached.append(output_file)
        else:
            pages_to_process[page_num] = columns

    def _process_page(page_num: int, columns: dict[str, Path]) -> None:
        """Transcribe both columns of a page and write JSON + raw .txt."""
        output_file = output_dir / f"page_{page_num:04d}.json"
        text_columns = {}
        col_counts = {}

        for col_key, col_label in [("lcol", "Spalte01"), ("rcol", "Spalte02")]:
            img_path = columns.get(col_key)
            if not img_path:
                text_columns[col_label] = ""
                col_counts[col_key] = 0
                continue

            try:
                numbered, converted = transcribe_image_raw(
                    img_path, api_key, base_url
                )
            except Exception as e:
                error_msg = f"{img_path.name}: {e}"
                logger.error("Transcription failed: %s", error_msg)
                with lock:
                    result.errors.append(error_msg)
                text_columns[col_label] = ""
                col_counts[col_key] = 0
                continue

            # Save raw numbered output
            raw_file = raw_dir / f"page_{page_num:04d}_{col_key}_raw.txt"
            raw_file.write_text(numbered, encoding="utf-8")

            text = converted
            entry_count = count_entries(text)
            col_counts[col_key] = entry_count

            # Anomaly detection (needs lock — updates rolling window)
            if anomaly_detector and text:
                with lock:
                    anomaly = anomaly_detector.check(
                        entry_count, img_path.name
                    )
                if anomaly.is_anomaly:
                    logger.warning("ANOMALY: %s", anomaly.reason)
                    with lock:
                        result.anomalies.append(anomaly.reason)
                    if anomaly.should_retry:
                        logger.info("Retrying %s...", img_path.name)
                        try:
                            numbered, converted = transcribe_image_raw(
                                img_path, api_key, base_url
                            )
                            raw_file.write_text(numbered, encoding="utf-8")
                            text = converted
                            entry_count = count_entries(text)
                            col_counts[col_key] = entry_count
                        except Exception as e:
                            logger.error(
                                "Retry failed: %s: %s", img_path.name, e
                            )

            text_columns[col_label] = text

        # Write legacy JSON
        page_data = {
            "pdfPageNumber": page_num,
            "surnameRange": [],
            "textColumns": text_columns,
        }
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(page_data, f, ensure_ascii=False, indent=2)

        with lock:
            result.written.append(output_file)

        lcol_n = col_counts.get("lcol", 0)
        rcol_n = col_counts.get("rcol", 0)
        with lock:
            done = len(result.written) + len(result.skipped_cached)
            print(
                f"  [{done}/{total_pages}] {output_file.name} "
                f"(lcol: {lcol_n}, rcol: {rcol_n} entries)"
            )

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(_process_page, page_num, columns): page_num
            for page_num, columns in pages_to_process.items()
        }
        for future in as_completed(futures):
            page_num = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error("Page %d failed: %s", page_num, e)
                with lock:
                    result.errors.append(f"page_{page_num:04d}: {e}")

    logger.info(
        "Transcription complete: %d written, %d cached, %d anomalies, %d errors",
        len(result.written),
        len(result.skipped_cached),
        len(result.anomalies),
        len(result.errors),
    )
    return result
