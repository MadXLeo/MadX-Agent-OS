"""The inventory counts matches, not only lines; compatibility triage is explicit."""
import importlib.util
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("branding_inventory", Path(__file__).resolve().parents[2] / "scripts/madx/inventory-branding.py")
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)


def test_every_case_insensitive_occurrence_including_same_line_is_counted():
    rows = list(inventory.occurrences("sample.ts", "Herald herald HERALD\nwindow.heraldOS"))
    assert [(row["line"], row["column"]) for row in rows] == [(1, 1), (1, 8), (1, 15), (2, 8)]


def test_attribution_and_compatibility_have_distinct_reasons():
    assert inventory.classify("NOTICE", "Herald OS", "Herald")[0] == "6"
    assert inventory.classify("app.ts", "window.heraldOS", "window.heraldOS")[0] == "4"
    assert inventory.classify("sample.test.ts", "Herald OS", "Herald")[0] == "5"
    assert inventory.classify("app.ts", 'title: "Herald OS"', "Herald")[0] == "1"
    assert inventory.classify("linux/bin/herald-os", 'die("run herald-os setup")', "herald-os")[0] == "2"
