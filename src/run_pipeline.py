"""
Run the parsing pipeline on dots.ocr v3 and/or old mocr data.

Creates temporary directory structures with junctions to isolate
specific year subdirectories, then calls main() with controlled
input/output paths.

Usage:
    python -m src.run_pipeline                    # 1943 test run (new + old)
    python -m src.run_pipeline --years 1938 1939  # specific years
    python -m src.run_pipeline --all              # all 74 years (1877-1954)
    python -m src.run_pipeline --old-only         # only old mocr data (1938-1944)
    python -m src.run_pipeline --new-only         # only new v3 data
"""
import argparse
import os
import sqlite3
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

from src.__main__ import main
from src.run_books import ALL_YEARS
from src.setup import setup
from src.shared.common.paths import DATA_PATH

INPUT_ROOT = DATA_PATH / "transcriptions" / "legacy_json"
OUTPUT_DIR = DATA_PATH / "db"

# Years that have old mocr comparison data
_OLD_MOCR_YEARS = {1938, 1939, 1940, 1941, 1942, 1943, 1944}


def _create_junction_dir(
    years: list[int],
    suffix: str = "",
) -> Path:
    """Create a temp dir with junctions to Basel_YYYY[suffix] subdirs.

    For new v3 data (suffix=""), uses _v3 directories.
    For old mocr data, pass suffix="_old_mocr".
    """
    tmp = Path(tempfile.mkdtemp(prefix="pipeline_"))
    for year in years:
        dir_suffix = suffix if suffix else "_v3"
        source = INPUT_ROOT / f"Basel_{year}{dir_suffix}"
        if source.exists():
            target = tmp / f"Basel_{year}"
            os.system(f'mklink /J "{target}" "{source}"')
        else:
            print(f"WARNING: {source} not found, skipping year {year}")
    return tmp


def _cleanup_junction_dir(tmp: Path) -> None:
    """Remove junctions and temp dir."""
    for entry in tmp.iterdir():
        if entry.is_dir():
            # Junctions are removed with rmdir (does not delete target)
            os.system(f'rmdir "{entry}"')
    tmp.rmdir()


def _backup_db(db_path: Path) -> None:
    """Back up an existing DB to a versioned zip in backup/."""
    if not db_path.exists():
        return
    backup_dir = db_path.parent / "backup"
    backup_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime("%d_%m_%Y")
    version = 1
    while True:
        backup_name = f"{db_path.stem}_{today}_v{version}.zip"
        backup_path = backup_dir / backup_name
        if not backup_path.exists():
            break
        version += 1
    with zipfile.ZipFile(backup_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(db_path, db_path.name)
    print(f"Backed up {db_path.name} -> backup/{backup_name}")


def _print_db_stats(db_path: Path, label: str) -> None:
    """Print record counts and field distributions from a DB."""
    if not db_path.exists():
        print(f"  {label}: DB not found at {db_path}")
        return

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Persons count
        cursor.execute("SELECT COUNT(*) FROM persons")
        total = cursor.fetchone()[0]
        print(f"\n  {label}: {total} person records")

        # Per year
        cursor.execute(
            "SELECT year, COUNT(*) FROM persons GROUP BY year ORDER BY year"
        )
        for year, count in cursor.fetchall():
            print(f"    {year}: {count}")

        # Telephone/postcheck distribution
        cursor.execute("SELECT COUNT(*) FROM persons WHERE telephone = 1")
        tel = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM persons WHERE postcheck = 1")
        post = cursor.fetchone()[0]
        print(f"    telephone=True: {tel} ({tel/total*100:.1f}%)" if total else "")
        print(f"    postcheck=True: {post} ({post/total*100:.1f}%)" if total else "")

        # Pfx distribution
        cursor.execute(
            "SELECT prefix, COUNT(*) FROM persons WHERE prefix != '' "
            "GROUP BY prefix ORDER BY COUNT(*) DESC LIMIT 10"
        )
        pfx_rows = cursor.fetchall()
        if pfx_rows:
            print(f"    prefix distribution:")
            for pfx, count in pfx_rows:
                print(f"      {pfx}: {count}")

        # Companies
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='companies'"
        )
        if cursor.fetchone():
            cursor.execute("SELECT COUNT(*) FROM companies")
            comp_total = cursor.fetchone()[0]
            print(f"    companies: {comp_total}")


def run():
    parser = argparse.ArgumentParser(
        description="Run parsing pipeline on OCR data"
    )
    parser.add_argument(
        "--years",
        type=int,
        nargs="+",
        default=[1943],
        help="Years to process (default: 1943 test run)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Process all 74 years (1877-1954)",
    )
    parser.add_argument(
        "--old-only",
        action="store_true",
        help="Only process old mocr data",
    )
    parser.add_argument(
        "--new-only",
        action="store_true",
        help="Only process new dots.ocr-1.5 data",
    )
    args = parser.parse_args()

    years = ALL_YEARS if args.all else args.years
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    time_stamp = f"{datetime.now():%b %d - %H%M}"
    setup(time_stamp, [DATA_PATH, INPUT_ROOT, OUTPUT_DIR])

    if len(years) == len(ALL_YEARS):
        year_label = "all_1877_1954"
    elif len(years) > 5:
        year_label = f"{years[0]}_{years[-1]}_{len(years)}yr"
    else:
        year_label = "_".join(str(y) for y in years)

    # New dots.ocr v3 data
    if not args.old_only:
        print(f"\n{'='*60}")
        print(
            f"Processing NEW v3 data: {len(years)} years "
            f"({years[0]}-{years[-1]})"
        )
        print(f"{'='*60}")

        tmp_new = _create_junction_dir(years)
        db_new = OUTPUT_DIR / f"dots_ocr_v3_{year_label}.db"

        _backup_db(db_new)
        if db_new.exists():
            db_new.unlink()

        try:
            main(tmp_new, db_new)
        finally:
            _cleanup_junction_dir(tmp_new)

        _print_db_stats(db_new, "NEW")

    # Old mocr data (only available for 1938-1944)
    if not args.new_only:
        old_years = [y for y in years if y in _OLD_MOCR_YEARS]
        if not old_years:
            print("\nSkipping OLD mocr — no old_mocr data for selected years.")
        else:
            old_label = "_".join(str(y) for y in old_years)
            print(f"\n{'='*60}")
            print(f"Processing OLD mocr data: {old_years}")
            print(f"{'='*60}")

            tmp_old = _create_junction_dir(old_years, suffix="_old_mocr")
            db_old = OUTPUT_DIR / f"old_mocr_{old_label}_COMPARISON.db"

            _backup_db(db_old)
            if db_old.exists():
                db_old.unlink()

            try:
                main(tmp_old, db_old)
            finally:
                _cleanup_junction_dir(tmp_old)

            _print_db_stats(db_old, "OLD")


if __name__ == "__main__":
    run()
