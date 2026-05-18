import unittest

from src.transcriptor.src.api_dots_ocr.anomaly_detector import AnomalyDetector


class TestAnomalyDetector(unittest.TestCase):
    def test_warmup_period(self):
        """During warmup (< 5 samples), only absolute floor triggers."""
        det = AnomalyDetector(window=10, min_entries=3)
        # Normal entries during warmup
        for i in range(4):
            result = det.check(30, f"img_{i}.jpg")
            self.assertFalse(result.is_anomaly)

    def test_absolute_floor(self):
        """Below min_entries is always anomalous."""
        det = AnomalyDetector(min_entries=5)
        result = det.check(2, "low.jpg")
        self.assertTrue(result.is_anomaly)

    def test_zero_entries_retries_once(self):
        """Zero entries triggers retry, but only once."""
        det = AnomalyDetector()
        r1 = det.check(0, "empty.jpg")
        self.assertTrue(r1.is_anomaly)
        self.assertTrue(r1.should_retry)

        r2 = det.check(0, "empty.jpg")
        self.assertTrue(r2.is_anomaly)
        self.assertFalse(r2.should_retry)  # No more retries

    def test_normal_entries_after_warmup(self):
        """Normal entries after warmup are not anomalous."""
        det = AnomalyDetector(window=10, z_threshold=2.5)
        # Fill window with normal values
        for i in range(10):
            det.check(30, f"normal_{i}.jpg")
        # Another normal value
        result = det.check(28, "test.jpg")
        self.assertFalse(result.is_anomaly)

    def test_low_count_after_warmup(self):
        """Very low count after warmup triggers anomaly."""
        det = AnomalyDetector(window=10, z_threshold=2.0, min_entries=3)
        for i in range(10):
            det.check(30, f"normal_{i}.jpg")
        # Far below mean
        result = det.check(5, "low.jpg")
        self.assertTrue(result.is_anomaly)
        self.assertTrue(result.should_retry)

    def test_retry_limit(self):
        """After max_retries, should_retry is False."""
        det = AnomalyDetector(window=10, z_threshold=2.0, max_retries=1)
        for i in range(10):
            det.check(30, f"normal_{i}.jpg")

        r1 = det.check(2, "bad.jpg")
        self.assertTrue(r1.should_retry)

        r2 = det.check(2, "bad.jpg")
        self.assertFalse(r2.should_retry)

    def test_stats_property(self):
        """Stats returns correct rolling statistics."""
        det = AnomalyDetector(window=5)
        for i in range(5):
            det.check(20 + i, f"img_{i}.jpg")
        s = det.stats
        self.assertEqual(s["n"], 5)
        self.assertAlmostEqual(s["mean"], 22.0, places=1)


if __name__ == "__main__":
    unittest.main()
