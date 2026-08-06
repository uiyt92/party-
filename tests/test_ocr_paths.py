import tempfile
import unittest
from pathlib import Path

from scripts.ocr import common


class OcrPathTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def test_defaults_point_to_classified_reference_paths(self):
        pdf_path, output_dir = common.resolve_ocr_paths(self.root, {})

        self.assertEqual(pdf_path, self.root / "references" / "pdf" / "카톡101.pdf")
        self.assertEqual(output_dir, self.root / "references" / "ocr")

    def test_environment_overrides_input_and_output(self):
        environment = {
            "KATALK101_PDF": str(self.root / "custom.pdf"),
            "OCR_OUTPUT_DIR": str(self.root / "custom-output"),
        }

        pdf_path, output_dir = common.resolve_ocr_paths(self.root, environment)

        self.assertEqual(pdf_path, self.root / "custom.pdf")
        self.assertEqual(output_dir, self.root / "custom-output")

    def test_local_key_is_used_only_when_environment_is_unset(self):
        local_key = self.root / "local" / "secrets" / "gcp-key.json"
        local_key.parent.mkdir(parents=True)
        local_key.write_text("{}", encoding="utf-8")
        environment = {}

        result = common.configure_google_credentials(self.root, environment)

        self.assertEqual(result, local_key)
        self.assertEqual(environment["GOOGLE_APPLICATION_CREDENTIALS"], str(local_key))

    def test_existing_google_credentials_are_not_overwritten(self):
        configured = self.root / "configured.json"
        environment = {"GOOGLE_APPLICATION_CREDENTIALS": str(configured)}

        result = common.configure_google_credentials(self.root, environment)

        self.assertEqual(result, configured)
        self.assertEqual(environment["GOOGLE_APPLICATION_CREDENTIALS"], str(configured))


if __name__ == "__main__":
    unittest.main()
