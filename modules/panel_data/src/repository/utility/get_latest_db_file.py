from pathlib import Path

from modules.shared.repository.supported_file_types import SupportedFileTypes


def get_latest_db_file(
    db_path: Path, input_type: SupportedFileTypes = SupportedFileTypes.DB
) -> Path:
    db_files = sorted(
        db_path.glob(f"*.{input_type.value}"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not db_files:
        raise FileNotFoundError(f"No .{input_type} files found in {db_path}")
    return db_files[0]
