"""Firmware must boot the patched appended partition, not an unrelated ISO file."""
import binascii
import importlib.util
import io
from pathlib import Path
import struct

import pytest

spec = importlib.util.spec_from_file_location("efi_boot", Path(__file__).resolve().parents[1] / "vm/efi-boot.py")
efi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(efi)


def hybrid_iso():
    image = bytearray(72 * 2048)
    table = bytearray(128 * 128)
    table[128:144] = efi.ESP
    struct.pack_into("<QQ", table, 128 + 32, 256, 271)
    header = bytearray(512)
    header[:8] = b"EFI PART"
    struct.pack_into("<II", header, 8, 0x10000, 92)
    struct.pack_into("<QIII", header, 72, 2, 128, 128, binascii.crc32(table))
    struct.pack_into("<I", header, 16, binascii.crc32(header[:92]))
    image[512:1024] = header
    image[1024:1024 + len(table)] = table
    image[16 * 2048:16 * 2048 + 7] = b"\x01CD001\x01"
    boot = bytearray(2048)
    boot[:7] = b"\x00CD001\x01"
    boot[7:30] = b"EL TORITO SPECIFICATION\0"
    struct.pack_into("<I", boot, 71, 24)
    image[17 * 2048:18 * 2048] = boot
    catalog = bytearray(2048)
    catalog[0] = 1
    catalog[30:32] = b"\x55\xaa"
    struct.pack_into("<H", catalog, 28, (-sum(struct.unpack("<16H", catalog[:32]))) % 65536)
    catalog[32] = 0x88
    struct.pack_into("<BBH", catalog, 64, 0x91, 0xEF, 1)
    catalog[96] = 0x88
    struct.pack_into("<I", catalog, 104, 64)
    image[24 * 2048:25 * 2048] = catalog
    image[48 * 2048:48 * 2048 + 8] = b"ISO copy"
    image[64 * 2048:64 * 2048 + 8] = b"EFI boot"
    return image


def test_extracts_the_actual_boot_partition_and_checks_replacement_bytes(tmp_path):
    source, expected = tmp_path / "installer.iso", tmp_path / "efi.img"
    original = hybrid_iso()
    source.write_bytes(original)
    report = efi.inspect("extract", source, expected)
    assert report["partition"] == 2 and report["offset"] == 64 * 2048
    assert expected.read_bytes() == original[64 * 2048:68 * 2048]
    assert efi.inspect("verify", source, expected) == report
    with pytest.raises(FileExistsError):
        efi.inspect("extract", source, expected)
    patched = b"patched!" + expected.read_bytes()[8:]
    expected.write_bytes(patched)
    with pytest.raises(ValueError, match="differs"):
        efi.inspect("verify", source, expected)
    original[64 * 2048:68 * 2048] = patched
    source.write_bytes(original)
    assert efi.inspect("verify", source, expected)["sha256"] != report["sha256"]


@pytest.mark.parametrize("defect, message", [
    ("header", "header checksum"), ("table", "table checksum"),
    ("catalog", "boot catalog"), ("wrong_copy", "does not match"),
    ("truncated", "outside the file"),
])
def test_refuses_corrupt_or_mismatched_boot_metadata(defect, message):
    image = hybrid_iso()
    if defect == "header":
        image[512 + 24] ^= 1
    elif defect == "table":
        image[1024 + 128] ^= 1
    elif defect == "catalog":
        image[24 * 2048 + 30] ^= 1
    elif defect == "wrong_copy":
        struct.pack_into("<I", image, 24 * 2048 + 104, 48)
    else:
        image = image[:65 * 2048]
    with pytest.raises(ValueError, match=message):
        efi.locate(io.BytesIO(image))


def test_extract_cannot_escape_the_test_workspace(tmp_path):
    folder = tmp_path / "workspace"
    folder.mkdir()
    source = folder / "installer.iso"
    source.write_bytes(hybrid_iso())
    with pytest.raises(ValueError, match="workspace"):
        efi.inspect("extract", source, tmp_path / "outside.img")
