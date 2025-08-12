from pathlib import Path


def get_subdirectories(base_path: Path) -> list[Path]:
    return [entry for entry in base_path.iterdir() if entry.is_dir()]
