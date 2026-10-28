#!/usr/bin/env python3
"""Create a NEW disposable GPT sentinel disk, not a Windows installation.

ESP/MSR/basic-data partition types exercise exclusion of an adjacent Windows-like disk.
There is no Windows OS or shared-ESP boot test here. Only the named regular file is written.
"""
import argparse
import binascii
from pathlib import Path
import struct
import uuid

SECTOR = 512
SECTORS = 512 * 1024 * 1024 // SECTOR


def header(current, backup, entries_lba, entries_crc, disk_id):
    value = bytearray(struct.pack("<8sIIIIQQQQ16sQIII", b"EFI PART", 0x10000, 92, 0, 0,
                                 current, backup, 34, SECTORS - 34, disk_id,
                                 entries_lba, 128, 128, entries_crc))
    struct.pack_into("<I", value, 16, binascii.crc32(value))
    return value.ljust(SECTOR, b"\0")


def create(directory: Path) -> Path:
    path = directory.resolve(strict=True) / "mock-windows.raw"
    entries = bytearray(128 * 128)
    parts = [
        ("c12a7328-f81f-11d2-ba4b-00a0c93ec93b", 2048, 264191, "Mock EFI system"),
        ("e3c9e316-0b5c-4db8-817d-f92df00215ae", 264192, 296959, "Mock Microsoft reserved"),
        ("ebd0a0a2-b9e5-4433-87c0-68b6b72699c7", 296960, SECTORS - 34, "Mock Windows data"),
    ]
    for index, (kind, start, end, name) in enumerate(parts):
        struct.pack_into("<16s16sQQQ72s", entries, index * 128, uuid.UUID(kind).bytes_le,
                         uuid.uuid4().bytes_le, start, end, 0, name.encode("utf-16le"))
    crc, disk_id = binascii.crc32(entries), uuid.uuid4().bytes_le
    # Exclusive creation prevents overwriting any disk/file supplied by a caller.
    with path.open("xb") as output:
        output.truncate(SECTORS * SECTOR)
        mbr = bytearray(SECTOR)
        struct.pack_into("<B3sB3sII", mbr, 446, 0, b"\0\2\0", 0xee, b"\xff\xff\xff", 1, SECTORS - 1)
        mbr[510:] = b"\x55\xaa"
        output.write(mbr)
        output.write(header(1, SECTORS - 1, 2, crc, disk_id))
        output.write(entries)
        output.seek((SECTORS - 33) * SECTOR)
        output.write(entries)
        output.write(header(SECTORS - 1, 1, SECTORS - 33, crc, disk_id))
        for _, start, _, name in parts:
            output.seek(start * SECTOR)
            output.write(("MADX PRESERVE THIS SENTINEL: " + name).encode())
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    print(create(parser.parse_args().directory))
