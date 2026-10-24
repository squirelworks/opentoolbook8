"""The PE header in front of a ToolBook object store."""

from __future__ import annotations

import struct

_PE32 = 0x10B
_EXPORT_INDEX = 0
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


def _u16(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 2 > len(data):
        raise ValueError("header ends early")
    return struct.unpack_from("<H", data, offset)[0]


def _u32(data: bytes, offset: int) -> int:
    if offset < 0 or offset + 4 > len(data):
        raise ValueError("header ends early")
    return struct.unpack_from("<I", data, offset)[0]
