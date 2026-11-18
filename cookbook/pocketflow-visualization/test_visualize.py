import sys
import tempfile
import unittest
from pathlib import Path


EXAMPLE_DIR = Path(__file__).resolve().parent
REPO_ROOT = EXAMPLE_DIR.parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(EXAMPLE_DIR))

from visualize import create_d3_visualization


class CreateD3VisualizationTests(unittest.TestCase):
    def test_rejects_filename_that_escapes_output_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_dir = root / "viz"

            for filename in ("../escaped_probe", r"..\escaped_probe", ""):
                with self.subTest(filename=filename):
                    with self.assertRaises(ValueError):
                        create_d3_visualization({}, output_dir, filename)

            self.assertFalse((root / "escaped_probe.json").exists())
            self.assertFalse((root / "escaped_probe.html").exists())

    def test_writes_files_inside_output_dir(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir) / "viz"

            html_path = create_d3_visualization({}, output_dir, "safe_flow")

            expected_html_path = (output_dir / "safe_flow.html").resolve()
            self.assertEqual(Path(html_path).resolve(), expected_html_path)
            self.assertTrue((output_dir / "safe_flow.json").is_file())
            self.assertTrue(expected_html_path.is_file())


if __name__ == "__main__":
    unittest.main()
