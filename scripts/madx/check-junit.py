#!/usr/bin/env python3
"""Require executed tests without failures or unreviewed skips."""
import argparse
import json
import xml.etree.ElementTree as ET


def check(path, allowed_skips=None):
    allowed_skips = allowed_skips or {}
    cases = ET.parse(path).getroot().findall(".//testcase")
    errors, executed = [], 0
    for case in cases:
        name = case.get("classname", "").rsplit(".", 1)[-1] + "." + case.get("name", "")
        if case.find("failure") is not None or case.find("error") is not None:
            errors.append(f"failed: {name}")
        elif case.find("skipped") is not None:
            if not allowed_skips.get(name):
                errors.append(f"unexpected skip: {name}: {case.find('skipped').get('message', '')}")
            else:
                print(f"Reviewed platform exclusion: {name}: {allowed_skips[name]}")
        else:
            executed += 1
    if not executed:
        errors.append("no passing executed tests")
    if errors:
        raise ValueError("required native evidence is incomplete:\n" + "\n".join(errors))
    return executed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report")
    parser.add_argument("--allow-skipped", help="JSON map of exact module.test names to review reasons")
    args = parser.parse_args()
    allowed = {}
    if args.allow_skipped:
        with open(args.allow_skipped, encoding="utf-8") as stream:
            allowed = json.load(stream)
    print(f"Required tests executed successfully: {check(args.report, allowed)}")
