from pathlib import Path

from src.pages_preprocessor.src.columns_cutter import process_pdf
from src.shared.common.paths import DATA_PATH


def main(input_path: Path, output_path: Path) -> None:
    pdfs = sorted(input_path.glob("*.pdf"))

    if not pdfs:
        print(f"No PDFs found in {input_path}")
        return

    for p in pdfs:
        process_pdf(p, output_path)

    print(f"Info: Done — images saved to: {output_path}")


if __name__ == "__main__":
    input_dir = DATA_PATH / "pdf"
    output_dir = DATA_PATH / "jpg"

    output_dir.mkdir(parents=True, exist_ok=True)

    main(input_dir, output_dir)
