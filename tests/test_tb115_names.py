"""TB115 common-file names against the Instructor 8.1 TBSystem names.

The two fixtures are the basenames listed in TB115-SYSTEM.md. The split is
install_partition. A shared name keeps the Instructor 8.1 spelling.
"""

import unittest
from pathlib import Path

from opentoolbook.partition import NamePartition, install_partition

TB80 = Path("tests/fixtures/tb80-tbsystem-names.txt")
TB115 = Path("tests/fixtures/tb115-tbsystem-names.txt")

# Instructor 8.1 spellings of the 18 names that occur on both sides.
BOTH = (
    "Asymgif.ocx",
    "dzactx.dll",
    "ISGDI32.DLL",
    "ISGDI32.INI",
    "PALOPTX.DLL",
    "tb80actr.sbk",
    "tb80aicc.sbk",
    "tb80anm.sbk",
    "tb80ftp.sbk",
    "tb80hyp.sbk",
    "tb80r.sbk",
    "TBCOM.DLL",
    "TBINET32.DLL",
    "TBKSLICE.DLL",
    "Tbload.exe",
    "TBUTIL32.dll",
    "TList4.ocx",
    "WINSOX.EXE",
)


def load_names(path: Path) -> tuple[str, ...]:
    """One basename per line. Blank lines and ``#`` comments are skipped."""
    names = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        names.append(line)
    return tuple(names)


class TB115NameTests(unittest.TestCase):
    def test_tbsystem_names_partition(self):
        tb80 = load_names(TB80)
        tb115 = load_names(TB115)
        self.assertEqual(len(tb80), 70)
        self.assertEqual(len(tb115), 182)
        self.assertEqual(len({name.casefold() for name in tb80}), 70)
        self.assertEqual(len({name.casefold() for name in tb115}), 182)
        part = install_partition(tb80, tb115)
        self.assertIsInstance(part, NamePartition)
        self.assertEqual(part.both, BOTH)
        self.assertEqual(len(part.author_only), 52)
        self.assertEqual(len(part.distribution_only), 164)
        self.assertIn("TB80.EXE", part.author_only)
        self.assertIn("TB80BAS.DLL", part.author_only)
        self.assertIn("TB80RTM.EXE", part.author_only)
        self.assertIn("tb80.ini", part.author_only)
        self.assertIn("tb115hyp.sbk", part.distribution_only)
        self.assertIn("tb105hyp.sbk", part.distribution_only)
        self.assertIn("tb115r.sbk", part.distribution_only)
        self.assertIn("TB115.EXE", part.distribution_only)
        self.assertIn("TB115BAS.DLL", part.distribution_only)
        self.assertIn("TB115RTM.DLL", part.distribution_only)
        self.assertIn("TB90.EXE", part.distribution_only)
        self.assertIn("TB90BAS.DLL", part.distribution_only)
        self.assertIn("TB90RTM.DLL", part.distribution_only)
        shared = {name.casefold() for name in part.both}
        author = {name.casefold() for name in part.author_only}
        other = {name.casefold() for name in part.distribution_only}
        self.assertTrue(shared.isdisjoint(author))
        self.assertTrue(shared.isdisjoint(other))
        self.assertTrue(author.isdisjoint(other))
        self.assertIn("tb80hyp.sbk", shared)
        self.assertIn("tb80anm.sbk", shared)
        self.assertIn("tb80r.sbk", shared)
        self.assertFalse(hasattr(part, "required"))
