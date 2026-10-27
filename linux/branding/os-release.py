#!/usr/bin/env python3
"""Write image identity in a staged os-release. Keep Fedora ID/ID_LIKE and version fields."""
import argparse
import json
from pathlib import Path

PRODUCT = json.loads((Path(__file__).parent / "product.json").read_text(encoding="utf-8"))


def branded_release(text: str) -> str:
    fields = {
        "NAME": PRODUCT["name"],
        "PRETTY_NAME": f"{PRODUCT['name']} {PRODUCT['version']}",
        "VARIANT": PRODUCT["name"],
        "VARIANT_ID": PRODUCT["slug"],
        "IMAGE_ID": PRODUCT["slug"],
        "IMAGE_VERSION": PRODUCT["version"],
        "HOME_URL": PRODUCT["repository"],
        "SUPPORT_URL": f"{PRODUCT['repository']}/issues",
        "BUG_REPORT_URL": f"{PRODUCT['repository']}/issues",
    }
    retained = [line for line in text.splitlines() if line.partition("=")[0] not in fields]
    return "\n".join(retained + [f'{key}={json.dumps(value)}' for key, value in fields.items()]) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    args.path.write_text(branded_release(args.path.read_text(encoding="utf-8")), encoding="utf-8")
