#!/usr/bin/env python3
"""Require a nonempty test report with no failures, errors or skipped tests."""
import sys
import xml.etree.ElementTree as ET


def check(path):
    cases = ET.parse(path).getroot().findall(".//testcase")
    if not cases or any(case.find(tag) is not None for case in cases for tag in ("failure", "error", "skipped")):
        raise ValueError("required native tests failed, skipped, or did not run")
    return len(cases)


if __name__ == "__main__":
    print(f"Required tests passed without skips: {check(sys.argv[1])}")
