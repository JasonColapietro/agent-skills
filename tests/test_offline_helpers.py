"""Regression tests for local output safety and campaign attribution."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from urllib.parse import parse_qsl, urlsplit
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


budget = load("budget", "skills/sheetfolk-budget-builder/scripts/build_budget.py")
utm = load("utm", "skills/timetopost-social-scheduler/scripts/utm.py")
NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


class BudgetTests(unittest.TestCase):
    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "budget.xlsx"
            output.write_bytes(b"existing workbook")
            with self.assertRaises(FileExistsError):
                budget.build(output, "October 2026", "monthly")
            self.assertEqual(output.read_bytes(), b"existing workbook")

    def test_cli_refuses_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "budget.xlsx"
            output.write_bytes(b"existing workbook")
            result = subprocess.run([sys.executable, str(Path(budget.__file__)), str(output)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_bytes(), b"existing workbook")

    def test_all_budget_types_calculate_income_minus_outflows(self):
        for kind in ("monthly", "sinking", "side-hustle", "combined"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / "budget.xlsx"
                budget.build(output, "October & November", kind)
                with ZipFile(output) as archive:
                    self.assertIsNone(archive.testzip())
                    root = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
                rows = root.findall("s:sheetData/s:row", NS)
                income, outflows = [], []
                for row in rows[3:-1]:
                    label = row.find("s:c/s:is/s:t", NS).text
                    (income if label in ("Income", "Side hustle income") else outflows).append(row.attrib["r"])
                total = rows[-1]
                self.assertEqual(total.find("s:c/s:is/s:t", NS).text, "NET CASH FLOW")
                for column, cell in zip(("B", "C"), total.findall("s:c", NS)[1:3]):
                    expected = "SUM(" + ",".join(column + row for row in income) + ")-SUM(" + ",".join(column + row for row in outflows) + ")"
                    self.assertEqual(cell.find("s:f", NS).text, expected)
                row = total.attrib["r"]
                self.assertEqual(total.findall("s:c", NS)[3].find("s:f", NS).text, f"B{row}-C{row}")


class AttributionTests(unittest.TestCase):
    def test_preserves_existing_attribution_duplicates_blanks_and_fragment(self):
        url = "https://example.com/page?a=1&a=2&utm_source=owner&utm_source=second&utm_medium=&utm_campaign=launch&utm_content=hero#section"
        tagged = utm.tag_url(url, "github", "skill")
        self.assertEqual(parse_qsl(urlsplit(tagged).query, keep_blank_values=True),
                         parse_qsl(urlsplit(url).query, keep_blank_values=True))
        self.assertEqual(urlsplit(tagged).fragment, "section")

    def test_only_missing_attribution_is_added(self):
        tagged = utm.tag_url("https://example.com/?utm_source=owner&coupon=yes", "github", "skill")
        pairs = dict(parse_qsl(urlsplit(tagged).query))
        self.assertEqual(pairs, {"utm_source": "owner", "coupon": "yes", "utm_medium": "skill",
                                 "utm_campaign": "agent-skills", "utm_content": "skill"})

    def test_rejects_non_http_urls(self):
        for url in ("javascript:alert(1)", "file:///tmp/file", "/relative"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                utm.tag_url(url, "github", "skill")


if __name__ == "__main__":
    unittest.main()
