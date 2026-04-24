"""
Rolling-window anomaly detection for OCR transcription.

Tracks entries-per-column over a sliding window and flags columns
with anomalously low entry counts. Prevents both:
- Missing real content (retry once on anomaly)
- Getting stuck on genuinely empty pages (max 1 retry, then accept)
"""
import logging
from collections import deque
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AnomalyResult:
    is_anomaly: bool
    should_retry: bool
    reason: str


class AnomalyDetector:
    """Track entries-per-column with a sliding window. Flag anomalies."""

    def __init__(
        self,
        window: int = 20,
        z_threshold: float = 2.5,
        min_entries: int = 3,
        max_retries: int = 1,
    ):
        self._window: deque[int] = deque(maxlen=window)
        self._z_threshold = z_threshold
        self._min_entries = min_entries
        self._max_retries = max_retries
        self._retry_counts: dict[str, int] = {}

    def check(self, count: int, image_name: str) -> AnomalyResult:
        """Check if entry count is anomalous. Updates internal state.

        Returns AnomalyResult with:
        - is_anomaly: True if count is suspiciously low
        - should_retry: True if we should re-transcribe (first anomaly only)
        - reason: human-readable explanation
        """
        retries_used = self._retry_counts.get(image_name, 0)

        # Zero entries: always anomalous, but don't retry more than once
        if count == 0:
            if retries_used < self._max_retries:
                self._retry_counts[image_name] = retries_used + 1
                return AnomalyResult(
                    is_anomaly=True,
                    should_retry=True,
                    reason=f"{image_name}: 0 entries detected, retrying",
                )
            self._window.append(count)
            return AnomalyResult(
                is_anomaly=True,
                should_retry=False,
                reason=f"{image_name}: 0 entries after retry, accepting",
            )

        # Not enough history yet: use absolute floor only
        if len(self._window) < 5:
            self._window.append(count)
            if count < self._min_entries:
                return AnomalyResult(
                    is_anomaly=True,
                    should_retry=False,
                    reason=(
                        f"{image_name}: {count} entries "
                        f"(below floor {self._min_entries}, warming up)"
                    ),
                )
            return AnomalyResult(False, False, "")

        # Compute rolling statistics
        mean = sum(self._window) / len(self._window)
        variance = sum((x - mean) ** 2 for x in self._window) / len(self._window)
        std = variance**0.5

        # Use a minimum std of 20% of the mean to avoid false positives
        # when all recent values are identical (std=0)
        effective_std = max(std, mean * 0.2)

        # Threshold: mean - z * std, but at least min_entries
        threshold = max(mean - self._z_threshold * effective_std, self._min_entries)

        if count < threshold:
            if retries_used < self._max_retries:
                self._retry_counts[image_name] = retries_used + 1
                return AnomalyResult(
                    is_anomaly=True,
                    should_retry=True,
                    reason=(
                        f"{image_name}: {count} entries "
                        f"(threshold {threshold:.0f}, mean {mean:.1f}), retrying"
                    ),
                )
            self._window.append(count)
            return AnomalyResult(
                is_anomaly=True,
                should_retry=False,
                reason=(
                    f"{image_name}: {count} entries "
                    f"(threshold {threshold:.0f}, mean {mean:.1f}), "
                    f"accepting after retry"
                ),
            )

        # Normal: update window
        self._window.append(count)
        return AnomalyResult(False, False, "")

    @property
    def stats(self) -> dict:
        """Current rolling statistics."""
        if not self._window:
            return {"mean": 0, "std": 0, "n": 0}
        mean = sum(self._window) / len(self._window)
        variance = sum((x - mean) ** 2 for x in self._window) / len(self._window)
        return {
            "mean": round(mean, 1),
            "std": round(variance**0.5, 1),
            "n": len(self._window),
        }
