import tempfile
import unittest
from pathlib import Path

from PIL import Image

from scripts import pdf_contact_sheets


class ContactSheetTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.pages = self.root / "pages"
        self.output = self.root / "sheets"
        self.pages.mkdir()
        for index in range(1, 4):
            image = Image.new("RGB", (120, 180), color=(index * 40, 80, 120))
            image.save(self.pages / f"page-{index:03d}.png")

    def tearDown(self):
        self.temp.cleanup()

    def test_splits_pages_and_labels_each_thumbnail(self):
        sheets = pdf_contact_sheets.create_contact_sheets(
            self.pages,
            self.output,
            per_sheet=2,
            columns=2,
            thumbnail_width=60,
        )

        self.assertEqual([path.name for path in sheets], [
            "contact-sheet-01.png",
            "contact-sheet-02.png",
        ])
        self.assertTrue(all(path.is_file() for path in sheets))
        with Image.open(sheets[0]) as sheet:
            self.assertGreater(sheet.width, 120)
            self.assertGreater(sheet.height, 180)

    def test_rejects_directory_without_page_images(self):
        empty = self.root / "empty"
        empty.mkdir()

        with self.assertRaisesRegex(ValueError, "No page PNGs"):
            pdf_contact_sheets.create_contact_sheets(empty, self.output)


if __name__ == "__main__":
    unittest.main()
