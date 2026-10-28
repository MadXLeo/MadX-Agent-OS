#!/usr/bin/env python3
"""Inspect an ISO's actual UEFI boot partition; only read/write ordinary test files."""
import argparse
import binascii
import hashlib
import json
from pathlib import Path
import struct
import uuid

ESP = uuid.UUID("c12a7328-f81f-11d2-ba4b-00a0c93ec93b").bytes_le


def locate(stream):
    """Require a single El Torito EFI entry backed by the ISO's GPT EFI partition."""
    stream.seek(0, 2)
    size = stream.tell()

    def read(offset, length):
        if offset < 0 or length < 0 or offset + length > size:
            raise ValueError("ISO boot metadata is outside the file")
        stream.seek(offset)
        data = stream.read(length)
        if len(data) != length:
            raise ValueError("truncated ISO boot metadata")
        return data

    header = bytearray(read(512, 512))
    if header[:8] != b"EFI PART":
        raise ValueError("ISO requires a GPT EFI partition")
    length, checksum = struct.unpack_from("<II", header, 12)
    if not 92 <= length <= 512:
        raise ValueError("invalid GPT header length")
    struct.pack_into("<I", header, 16, 0)
    if binascii.crc32(header[:length]) != checksum:
        raise ValueError("GPT header checksum mismatch")
    table_lba, count, width, checksum = struct.unpack_from("<QIII", header, 72)
    if not 1 <= count <= 4096 or width < 128 or width % 128 or count * width > 1024 * 1024:
        raise ValueError("unsupported GPT entry table")
    entries = read(table_lba * 512, count * width)
    if binascii.crc32(entries) != checksum:
        raise ValueError("GPT table checksum mismatch")
    partitions = []
    for index in range(count):
        entry = entries[index * width:(index + 1) * width]
        if entry[:16] == ESP:
            start, end = struct.unpack_from("<QQ", entry, 32)
            partitions.append((index + 1, start * 512, (end - start + 1) * 512))
    if len(partitions) != 1:
        raise ValueError("expected exactly one GPT EFI partition")
    number, offset, length = partitions[0]
    if not 1 <= number <= 8 or not 0 < length <= 64 * 1024 * 1024:
        raise ValueError("unsupported EFI partition size or number")
    payload = read(offset, length)

    catalog = None
    for block in range(16, 128):
        descriptor = read(block * 2048, 2048)
        if descriptor[1:6] != b"CD001":
            raise ValueError("invalid ISO volume descriptor")
        if descriptor[0] == 0 and descriptor[7:39].rstrip(b"\0 ") == b"EL TORITO SPECIFICATION":
            catalog = read(struct.unpack_from("<I", descriptor, 71)[0] * 2048, 2048)
            break
        if descriptor[0] == 255:
            break
    if catalog is None or catalog[0] != 1 or catalog[30:32] != b"\x55\xaa" or sum(struct.unpack("<16H", catalog[:32])) % 65536:
        raise ValueError("missing or invalid El Torito boot catalog")
    boot_entries = []
    if catalog[1] == 0xEF:
        boot_entries.append(catalog[32:64])
    cursor = 64
    while cursor < len(catalog) and catalog[cursor] in (0x90, 0x91):
        final, platform, count = struct.unpack_from("<BBH", catalog, cursor)
        cursor += 32
        if cursor + count * 32 > len(catalog):
            raise ValueError("unsupported El Torito catalog size")
        if platform == 0xEF:
            boot_entries.extend(catalog[cursor + i * 32:cursor + (i + 1) * 32] for i in range(count))
        cursor += count * 32
        if final == 0x91:
            break
    if len(boot_entries) != 1 or boot_entries[0][0:2] != b"\x88\x00":
        raise ValueError("expected one bootable EFI El Torito image")
    boot_offset = struct.unpack_from("<I", boot_entries[0], 8)[0] * 2048
    if boot_offset != offset:
        raise ValueError("El Torito EFI image does not match the GPT EFI partition")
    return {"partition": number, "offset": offset, "bytes": length,
            "sha256": hashlib.sha256(payload).hexdigest()}, payload


def inspect(mode, source: Path, payload_path: Path):
    if not source.is_file() or source.is_symlink():
        raise ValueError("source must be an ordinary ISO file")
    if payload_path.is_symlink() or not payload_path.resolve().is_relative_to(source.resolve().parent):
        raise ValueError("EFI image must stay inside the test workspace")
    with source.open("rb") as stream:
        report, payload = locate(stream)
    if mode == "extract":
        with payload_path.open("xb") as output:
            output.write(payload)
    elif not payload_path.is_file() or payload_path.read_bytes() != payload:
        raise ValueError("bootable EFI partition differs from the patched image")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("extract", "verify"))
    parser.add_argument("source", type=Path)
    parser.add_argument("efi_image", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.mode, args.source, args.efi_image), indent=2))
