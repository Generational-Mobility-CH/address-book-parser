"""
Migrate existing DBs from single 'coordinates' string column to 4 numeric columns.

Usage:
    uv run python -m src.migrate_coordinates                  # all DBs in data/Basel/db/
    uv run python -m src.migrate_coordinates path/to/file.db  # specific DB
"""
import argparse
import re
import sqlite3
import zipfile
from datetime import datetime
from pathlib import Path

from modules.text_parser.src.coordinate_converter import wgs84_to_lv95

DB_DIR = Path("data/Basel/db")

_COORD_RE = re.compile(r"^\s*([\d.]+),\s*([\d.]+)")


def _backup(db_path: Path) -> None:
    backup_dir = db_path.parent / "backup"
    backup_dir.mkdir(exist_ok=True)
    today = datetime.now().strftime("%d_%m_%Y")
    version = 1
    while True:
        name = f"{db_path.stem}_{today}_v{version}.zip"
        path = backup_dir / name
        if not path.exists():
            break
        version += 1
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(db_path, db_path.name)
    print(f"  Backed up -> backup/{name}")


def migrate(db_path: Path) -> None:
    print(f"\nMigrating {db_path.name} ...")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check if already migrated
    cur.execute("PRAGMA table_info(persons)")
    columns = [row[1] for row in cur.fetchall()]
    if "latitude_wgs84" in columns:
        print("  Already migrated, skipping.")
        conn.close()
        return

    if "coordinates" not in columns:
        print("  No 'coordinates' column found, skipping.")
        conn.close()
        return

    _backup(db_path)

    # Count rows
    cur.execute("SELECT COUNT(*) FROM persons")
    total = cur.fetchone()[0]

    # Add new columns
    for col in ("latitude_wgs84", "longitude_wgs84", "easting_lv95", "northing_lv95"):
        cur.execute(f"ALTER TABLE persons ADD COLUMN {col} REAL")

    # Read and convert
    cur.execute("SELECT rowid, coordinates FROM persons")
    rows = cur.fetchall()

    populated = 0
    empty = 0
    for rowid, coord_str in rows:
        if not coord_str or not coord_str.strip():
            empty += 1
            continue

        m = _COORD_RE.match(coord_str)
        if not m:
            empty += 1
            continue

        lat = float(m.group(1))
        lon = float(m.group(2))
        easting, northing = wgs84_to_lv95(lat, lon)

        cur.execute(
            "UPDATE persons SET latitude_wgs84=?, longitude_wgs84=?, "
            "easting_lv95=?, northing_lv95=? WHERE rowid=?",
            (lat, lon, easting, northing, rowid),
        )
        populated += 1

    # Drop old column (SQLite 3.35+)
    cur.execute("ALTER TABLE persons DROP COLUMN coordinates")

    conn.commit()

    # Verify
    cur.execute("SELECT COUNT(*) FROM persons")
    after = cur.fetchone()[0]

    cur.execute("SELECT latitude_wgs84, longitude_wgs84, easting_lv95, northing_lv95 FROM persons WHERE latitude_wgs84 IS NOT NULL LIMIT 1")
    sample = cur.fetchone()

    conn.close()

    print(f"  Total rows: {total} -> {after} (should match)")
    print(f"  Populated: {populated}, Empty: {empty}")
    if sample:
        print(f"  Sample: WGS84({sample[0]}, {sample[1]}) LV95(E{sample[2]:.1f}, N{sample[3]:.1f})")


def main():
    parser = argparse.ArgumentParser(description="Migrate coordinate columns in existing DBs")
    parser.add_argument("db", nargs="?", help="Specific .db file (default: all in data/Basel/db/)")
    args = parser.parse_args()

    if args.db:
        migrate(Path(args.db))
    else:
        dbs = sorted(DB_DIR.glob("*.db"))
        print(f"Found {len(dbs)} databases in {DB_DIR}")
        for db in dbs:
            migrate(db)

    print("\nDone.")


if __name__ == "__main__":
    main()
