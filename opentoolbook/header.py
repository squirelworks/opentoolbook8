"""The PE header in front of a ToolBook object store."""

from __future__ import annotations

import struct
from dataclasses import dataclass

_PE32 = 0x10B
_EXPORT_INDEX = 0
_RESOURCE_INDEX = 2
_RT_VERSION = 16
_COFF_SIZE = 20
_SECTION_SIZE = 40
# PE32 optional header: NumberOfRvaAndSizes, then the data directories.
_DATA_DIRECTORY = 96


def export_module_name(data: bytes) -> str:
    """C string named by the PE export directory."""
    sections = _sections(data)
    export_rva, _size = _data_directory(data, _EXPORT_INDEX)
    export = _file_offset(sections, export_rva)
    name_rva = _u32(data, export + 12)
    return _cstring(data, _file_offset(sections, name_rva))


@dataclass(frozen=True)
class VersionFields:
    """Version-resource strings that match in the authored book and a NIDA book."""

    file_description: str
    internal_name: str
    original_filename: str
    product_version: str
    company_name: str


def version_fields(data: bytes) -> VersionFields:
    """Those five strings from the PE version resource."""
    strings = _version_strings(_version_blob(data))
    try:
        return VersionFields(
            file_description=strings["FileDescription"],
            internal_name=strings["InternalName"],
            original_filename=strings["OriginalFilename"],
            product_version=strings["ProductVersion"],
            company_name=strings["CompanyName"],
        )
    except KeyError as exc:
        raise ValueError("version resource is missing a string") from exc


def _sections(data: bytes) -> tuple[tuple[int, int, int], ...]:
    """``(virtual_address, raw_pointer, raw_size)`` for each section."""
    pe = _pe_offset(data)
    section_count = _u16(data, pe + 6)
    optional_size = _u16(data, pe + 20)
    optional = pe + 4 + _COFF_SIZE
    if _u16(data, optional) != _PE32:
        raise ValueError("not a PE32 header")
    sections: list[tuple[int, int, int]] = []
    table = optional + optional_size
    for index in range(section_count):
        entry = table + index * _SECTION_SIZE
        virtual = _u32(data, entry + 12)
        raw_size = _u32(data, entry + 16)
        raw_pointer = _u32(data, entry + 20)
        sections.append((virtual, raw_pointer, raw_size))
    return tuple(sections)


def _data_directory(data: bytes, index: int) -> tuple[int, int]:
    pe = _pe_offset(data)
    optional = pe + 4 + _COFF_SIZE
    count = _u32(data, optional + _DATA_DIRECTORY - 4)
    if index >= count:
        raise ValueError("PE data directory is absent")
    entry = optional + _DATA_DIRECTORY + index * 8
    rva = _u32(data, entry)
    size = _u32(data, entry + 4)
    if rva == 0 or size == 0:
        raise ValueError("PE data directory is empty")
    return rva, size


def _pe_offset(data: bytes) -> int:
    if len(data) < 0x40 or data[:2] != b"MZ":
        raise ValueError("not a PE file")
    pe = _u32(data, 0x3C)
    if pe + 4 + _COFF_SIZE > len(data) or data[pe:pe + 4] != b"PE\0\0":
        raise ValueError("not a PE file")
    return pe


def _file_offset(sections: tuple[tuple[int, int, int], ...], rva: int) -> int:
    for virtual, raw_pointer, raw_size in sections:
        if raw_size and virtual <= rva < virtual + raw_size:
            return raw_pointer + (rva - virtual)
    raise ValueError("RVA is outside the section table")


def _cstring(data: bytes, offset: int) -> str:
    end = data.find(b"\x00", offset)
    if end < 0:
        raise ValueError("export module name is not terminated")
    try:
        return data[offset:end].decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("export module name is not ASCII") from exc


def _version_blob(data: bytes) -> bytes:
    sections = _sections(data)
    root_rva, _size = _data_directory(data, _RESOURCE_INDEX)
    root = _file_offset(sections, root_rva)
    data_rva, data_size = _resource_leaf(data, root, _resource_id(data, root, _RT_VERSION))
    start = _file_offset(sections, data_rva)
    if data_size < 6 or start + data_size > len(data):
        raise ValueError("version resource runs past the file")
    return data[start:start + data_size]


def _resource_id(data: bytes, directory: int, want: int) -> int:
    named = _u16(data, directory + 12)
    ids = _u16(data, directory + 14)
    pos = directory + 16
    for _ in range(named + ids):
        name = _u32(data, pos)
        offset = _u32(data, pos + 4)
        pos += 8
        if (name & 0x80000000) == 0 and name == want:
            return offset
    raise ValueError("version resource is absent")


def _resource_leaf(data: bytes, root: int, offset_field: int) -> tuple[int, int]:
    if offset_field & 0x80000000:
        directory = root + (offset_field & 0x7FFFFFFF)
        count = _u16(data, directory + 12) + _u16(data, directory + 14)
        if count < 1:
            raise ValueError("version resource is absent")
        return _resource_leaf(data, root, _u32(data, directory + 20))
    entry = root + offset_field
    return _u32(data, entry), _u32(data, entry + 4)


def _version_strings(blob: bytes) -> dict[str, str]:
    found: dict[str, str] = {}

    def walk(off: int) -> None:
        length = _u16(blob, off)
        value_length = _u16(blob, off + 2)
        value_type = _u16(blob, off + 4)
        if length < 6 or off + length > len(blob):
            raise ValueError("version resource is truncated")
        cursor = off + 6
        chars: list[str] = []
        while cursor + 2 <= off + length:
            unit = _u16(blob, cursor)
            cursor += 2
            if unit == 0:
                break
            chars.append(chr(unit))
        else:
            raise ValueError("version key is not terminated")
        cursor = (cursor + 3) & ~3
        if value_type == 1 and value_length:
            end = cursor + value_length * 2
            if end > len(blob):
                raise ValueError("version string runs past the resource")
            found["".join(chars)] = blob[cursor:end].decode("utf-16le").split("\x00", 1)[0]
            cursor = (end + 3) & ~3
        elif value_length:
            cursor = (cursor + value_length + 3) & ~3
        limit = off + length
        while cursor + 6 <= limit:
            child = _u16(blob, cursor)
            if child < 6 or cursor + child > limit:
                break
            walk(cursor)
            cursor = (cursor + child + 3) & ~3

    walk(0)
    return found


def _u16(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 2 > len(data):
        raise ValueError("header ends early")
    return struct.unpack_from("<H", data, offset)[0]


def _u32(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise ValueError("header ends early")
    return struct.unpack_from("<I", data, offset)[0]
