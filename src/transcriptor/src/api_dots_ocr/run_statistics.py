"""
Per-column statistics accumulator for full-book transcription runs.

Tracks entry counts and prefix ratios per column, compares against
baseline distributions from the benchmark, and writes summary CSVs.
"""
import csv
import json
import logging
import re
from dataclasses import asdict, dataclass, fields
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class ColumnStats:
    image: str
    page_num: int
    column: str
    entry_count: int
    em_dash_count: int
    partner_dash_count: int
    plain_entry_count: int
    em_dash_ratio: float
    partner_dash_ratio: float
    z_score_vs_baseline: float
    anomaly: bool


class RunStatistics:
    """Accumulates per-column statistics during a full-book run."""

    def __init__(self, baseline_path: Path | None = None):
        self._rows: list[ColumnStats] = []
        self._baseline: dict | None = None
        if baseline_path and baseline_path.exists():
            with open(baseline_path) as f:
                self._baseline = json.load(f)
            logger.info("Loaded baseline from %s", baseline_path)

    def record(
        self,
        image: str,
        page_num: int,
        column: str,
        text: str,
        anomaly: bool = False,
    ) -> ColumnStats:
        """Analyze a converted text column and record statistics."""
        lines = [ln for ln in text.splitlines() if ln.strip()] if text else []
        entry_count = len(lines)

        em_dash_count = 0
        partner_dash_count = 0
        plain_count = 0

        for line in lines:
            stripped = line.strip()
            if re.match(r"^[\u2014]\s+-", stripped):
                partner_dash_count += 1
            elif stripped.startswith("\u2014"):
                em_dash_count += 1
            else:
                plain_count += 1

        total = max(entry_count, 1)
        em_ratio = em_dash_count / total
        partner_ratio = partner_dash_count / total

        z_score = 0.0
        if self._baseline and "entries_per_column" in self._baseline:
            bl = self._baseline["entries_per_column"]
            bl_mean = bl.get("mean", 0)
            bl_std = bl.get("std", 1)
            if bl_std > 0:
                z_score = (entry_count - bl_mean) / bl_std

        stats = ColumnStats(
            image=image,
            page_num=page_num,
            column=column,
            entry_count=entry_count,
            em_dash_count=em_dash_count,
            partner_dash_count=partner_dash_count,
            plain_entry_count=plain_count,
            em_dash_ratio=round(em_ratio, 4),
            partner_dash_ratio=round(partner_ratio, 4),
            z_score_vs_baseline=round(z_score, 2),
            anomaly=anomaly,
        )
        self._rows.append(stats)
        return stats

    def write_csv(self, path: Path) -> None:
        """Write accumulated statistics to CSV."""
        if not self._rows:
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        fieldnames = [f.name for f in fields(ColumnStats)]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self._rows:
                writer.writerow(asdict(row))
        logger.info("Statistics written to %s (%d rows)", path, len(self._rows))

    def print_summary(self) -> None:
        """Print aggregate statistics."""
        if not self._rows:
            print("No statistics recorded.")
            return

        counts = [r.entry_count for r in self._rows]
        total_entries = sum(counts)
        n_cols = len(counts)
        mean = total_entries / n_cols
        variance = sum((c - mean) ** 2 for c in counts) / n_cols
        std = variance**0.5
        anomalies = [r for r in self._rows if r.anomaly]

        em_ratios = [r.em_dash_ratio for r in self._rows]
        partner_ratios = [r.partner_dash_ratio for r in self._rows]

        print(f"\n{'='*60}")
        print("RUN STATISTICS SUMMARY")
        print(f"{'='*60}")
        print(f"Total columns processed: {n_cols}")
        print(f"Total entries: {total_entries}")
        print(f"Entries per column: {mean:.1f} \u00b1 {std:.1f}")
        print(f"  min: {min(counts)}, max: {max(counts)}")
        print(
            f"Em-dash ratio: {sum(em_ratios)/n_cols:.3f} "
            f"(range {min(em_ratios):.3f}-{max(em_ratios):.3f})"
        )
        print(
            f"Partner-dash ratio: {sum(partner_ratios)/n_cols:.3f} "
            f"(range {min(partner_ratios):.3f}-{max(partner_ratios):.3f})"
        )
        print(f"Anomalies: {len(anomalies)}")

        if self._baseline:
            bl = self._baseline.get("entries_per_column", {})
            bl_mean = bl.get("mean", 0)
            if bl_mean > 0:
                bl_std = bl.get("std", 1)
                z = (mean - bl_mean) / bl_std if bl_std > 0 else 0
                print(
                    f"vs. baseline: {mean:.1f} vs {bl_mean:.1f} (z={z:.2f})"
                )

        if anomalies:
            print(f"\nAnomalous columns ({len(anomalies)}):")
            for a in anomalies[:20]:
                print(f"  {a.image} ({a.column}): {a.entry_count} entries")
            if len(anomalies) > 20:
                print(f"  ... and {len(anomalies) - 20} more")
        print(f"{'='*60}\n")
