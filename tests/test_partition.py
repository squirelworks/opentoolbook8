"""Author-install names against the NIDA course name list."""

import unittest
from pathlib import Path

from opentoolbook.partition import NamePartition, install_partition

FIXTURE = Path("tests/fixtures/install-names.txt")

# Author spellings of the 35 names that occur on both sides.
BOTH = (
    "TB80ACX.DLL",
    "tb80anm.sbk",
    "TB80BAS.DLL",
    "TB80BMP.DLL",
    "TB80CMP.DLL",
    "TB80ENU1.DLL",
    "TB80ENU2.DLL",
    "TB80F32L.dll",
    "TB80FLT.DLL",
    "tb80hyp.sbk",
    "TB80JPG.DLL",
    "TB80LNL.DLL",
    "TB80MAIN.EXE",
    "TB80MM.DLL",
    "TB80NET.EXE",
    "TB80OCX.DLL",
    "TB80OLE.DLL",
    "tb80r.sbk",
    "TB80RCR.DLL",
    "TB80RMT.DLL",
    "TB80RTM.EXE",
    "TB80RUN.EXE",
    "TB80UTL.DLL",
    "TB80VBX.DLL",
    "TB80W16.DLL",
    "TB80W32.DLL",
    "TBCBT.DLL",
    "TBDB3.DLL",
    "TBDLG.DLL",
    "TBDOS.DLL",
    "TBFILE32.DLL",
    "Tbload.exe",
    "TBPDX.DLL",
    "TBREG.DLL",
    "TBWIN.DLL",
)

DISTRIBUTION_ONLY = (
    "NC81BASE.SBK",
    "NC81INT.DLL",
    "NC81REC.DLL",
    "NC81RECS.SBK",
    "NC81TEST.SBK",
    "NC81TRNR.SBK",
    "NIDA81.TBK",
)


def load_names(path: Path) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Read the ``[author]`` and ``[distribution]`` sections."""
    author: list[str] = []
    distribution: list[str] = []
    section: list[str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[author]":
            section = author
            continue
        if line == "[distribution]":
            section = distribution
            continue
        if section is None:
            raise ValueError(line)
        section.append(line)
    return tuple(author), tuple(distribution)


class PartitionTests(unittest.TestCase):
    def test_measured_lists_split_author_from_distribution(self):
        author, distribution = load_names(FIXTURE)
        self.assertEqual(len(author), 472)
        self.assertEqual(len(distribution), 42)
        part = install_partition(author, distribution)
        self.assertIsInstance(part, NamePartition)
        self.assertEqual(part.both, BOTH)
        self.assertEqual(part.distribution_only, DISTRIBUTION_ONLY)
        self.assertEqual(len(part.author_only), 437)
        self.assertIn("Inst80.exe", part.author_only)
        self.assertIn("TB80.EXE", part.author_only)
        self.assertIn("PACKAGER.exe", part.author_only)
        self.assertIn("tb80RED.DLL", part.author_only)
        self.assertIn("TB80MM.INI", part.author_only)
        author_only = {name.casefold() for name in part.author_only}
        self.assertNotIn("tb80rtm.exe", author_only)
        self.assertNotIn("tb80bas.dll", author_only)
        self.assertNotIn("nida81.tbk", author_only)
        # The report is the partition. It does not grade a name as required.
        self.assertFalse(hasattr(part, "required"))

    def test_comparison_ignores_case_and_keeps_the_first_spelling(self):
        part = install_partition(
            ["TB80BAS.DLL", "Inst80.exe", "TB80BAS.DLL"],
            ["tb80bas.dll", "NIDA81.TBK"],
        )
        self.assertEqual(part.both, ("TB80BAS.DLL",))
        self.assertEqual(part.author_only, ("Inst80.exe",))
        self.assertEqual(part.distribution_only, ("NIDA81.TBK",))
