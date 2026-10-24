"""Common Files basenames against the Program Files author tree.

The fixture is the Instructor 8.1 install under /tmp/tb81/wine, split by
directory. install_partition keeps the Common Files spelling of a shared name.
The TB115 name comparison stays in test_tb115_names.
"""

import unittest
from pathlib import Path

from opentoolbook.partition import NamePartition, install_partition

LAYOUT = Path("tests/fixtures/instructor-layout-names.txt")
TB80 = Path("tests/fixtures/tb80-tbsystem-names.txt")

COMMON_ONLY = (
    "TB80.EXE",
    "TB80BAS.DLL",
    "TB80RTM.EXE",
    "tb80anm.sbk",
    "tb80hyp.sbk",
    "tb80r.sbk",
)

PROGRAM_ONLY = ("Inst80.exe",)


def load_sections(path: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Read the ``[common]`` and ``[program]`` sections."""
    common: list[str] = []
    program: list[str] = []
    section: list[str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[common]":
            section = common
            continue
        if line == "[program]":
            section = program
            continue
        if section is None:
            raise ValueError(line)
        section.append(line)
    return tuple(common), tuple(program)


def load_names(path: Path) -> tuple[str, ...]:
    """One basename per line. Blank lines and ``#`` comments are skipped."""
    names = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return tuple(names)


class InstructorLayoutTests(unittest.TestCase):
    def test_common_files_partition_from_program_files(self):
        common, program = load_sections(LAYOUT)
        self.assertEqual(len(common), 125)
        self.assertEqual(len(program), 348)
        self.assertEqual(len({name.casefold() for name in common}), 125)
        self.assertEqual(len({name.casefold() for name in program}), 348)
        part = install_partition(common, program)
        self.assertIsInstance(part, NamePartition)
        self.assertEqual(part.both, ("relnotes.wri",))
        self.assertEqual(len(part.author_only), 124)
        self.assertEqual(len(part.distribution_only), 347)
        for name in COMMON_ONLY:
            self.assertIn(name, part.author_only)
        for name in PROGRAM_ONLY:
            self.assertIn(name, part.distribution_only)
        program_keys = {name.casefold() for name in program}
        for name in COMMON_ONLY:
            self.assertNotIn(name.casefold(), program_keys)
        common_keys = {name.casefold() for name in common}
        for name in PROGRAM_ONLY:
            self.assertNotIn(name.casefold(), common_keys)
        self.assertFalse(hasattr(part, "required"))

    def test_tbsystem_names_sit_in_common_files(self):
        common, program = load_sections(LAYOUT)
        tb80 = load_names(TB80)
        self.assertEqual(len(tb80), 70)
        common_keys = {name.casefold() for name in common}
        for name in tb80:
            self.assertIn(name.casefold(), common_keys)
        part = install_partition(tb80, program)
        self.assertEqual(part.both, ())
        self.assertEqual(len(part.author_only), 70)
        self.assertEqual(len(part.distribution_only), 348)
        self.assertIn("TB80.EXE", part.author_only)
        self.assertIn("TB80BAS.DLL", part.author_only)
        self.assertIn("TB80RTM.EXE", part.author_only)
        self.assertIn("Inst80.exe", part.distribution_only)
