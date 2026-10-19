"""예제 CSV에서 정답·split 열을 제거하고 lot의 전체 trace를 유지한다."""
import csv
import io
from pathlib import Path
import tempfile
import unittest
import zipfile

from prepare_demo_csv import prepare_demo


class DemoCsvTests(unittest.TestCase):
    def test_interleaved_lots_keep_all_step_one_rows_without_labels(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            stream = io.StringIO()
            fields = ["MaterialID", "StepID", "duration_ms", "is_test", "target", *[f"feature_{i}" for i in range(1, 21)]]
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            for identifier, time, split, step in [(10, 0, 0, 1), (20, 0, 1, 1), (30, 0, 1, 1), (20, 1, 1, 1), (20, 2, 1, 2)]:
                row = {field: 0 for field in fields}
                row.update(MaterialID=identifier, duration_ms=time, is_test=split, StepID=step)
                writer.writerow(row)
            archive = folder / "D2.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("D2.csv", stream.getvalue())
            target = folder / "demo.csv"
            self.assertEqual(prepare_demo(archive, target, group_count=1), 2)
            with target.open(encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual([row["duration_ms"] for row in rows], ["0", "1"])
            self.assertTrue(all(row["MaterialID"] == "20" for row in rows))
            self.assertNotIn("target", rows[0])
            self.assertNotIn("is_test", rows[0])


if __name__ == "__main__":
    unittest.main()
