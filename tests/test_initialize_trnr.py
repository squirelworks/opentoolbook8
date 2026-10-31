"""``initializeTrnr`` literals, and the trainer handlers that reach a DLL are skipped."""

import os
import unittest
from pathlib import Path

from opentoolbook.initialize import assignments_only, initialize, run_if_assignments
from opentoolbook.props import UserProperties
from opentoolbook.send import Chain, calls_dll, reaches_dll

LINK = 'to handle linkMemFunctions32\n\tlinkDLL32 "kernel32.dll"\n\t\tWORD GlobalAlloc(WORD,DWORD)\n\tend linkDLL32\nend\n'
UNLINK = 'to handle unlinkMemFunctions32\n\tunlinkDLL "kernel32.dll"\nend\n'
FAULTS = (
    "to get sendFaults130 string faults\n\tresult = 64\n\tconditions\n"
    "\t\twhen __trainerType = 0\n\t\t\tresult = sendFaultsTd2000()\n\tend conditions\n\treturn result\nend\n"
)
TD2000 = 'to get sendFaultsTd2000\n\tlinkDLL32 "td2000.dll"\n\tend linkDLL32\n\treturn 0\nend\n'
SETTINGS = "to get plainSettings\n\n\t__trainerAc1 = 0\n\t__trainerNlv = 0.0\n\treturn 0\nend\n"


class InitializeTrnrTests(unittest.TestCase):
    def test_dll_handlers_are_skipped(self):
        chain = Chain((("nc81trnr.sbk", {
            "linkmemfunctions32": LINK,
            "unlinkmemfunctions32": UNLINK,
            "sendfaults130": FAULTS,
            "sendfaultstd2000": TD2000,
            "plainsettings": SETTINGS,
        }),))
        self.assertTrue(calls_dll(UNLINK))
        self.assertEqual(reaches_dll(chain, "sendFaults130"), "sendFaultsTd2000")
        for name in ("linkMemFunctions32", "unlinkMemFunctions32", "sendFaults130"):
            self.assertIsNone(run_if_assignments(chain, name, UserProperties()), name)
        props = UserProperties()
        done = run_if_assignments(chain, "plainSettings", props)
        self.assertIsNotNone(done)
        self.assertEqual(dict(props.items()), {"__trainerac1": 0, "__trainernlv": 0.0})

    def test_assignments_only(self):
        self.assertTrue(assignments_only(SETTINGS))
        self.assertFalse(assignments_only(FAULTS))
        self.assertFalse(assignments_only(LINK))

    def test_the_real_system_books(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.send import handler_chain
        from opentoolbook.shelf import search_roots

        lesson = Path(path)
        chain = handler_chain(lesson.read_bytes(), lesson.name, search_roots(lesson, None))
        if chain.find("initializeTrnr") is None or chain.find("getExternalValue") is None:
            self.skipTest("nc81trnr.sbk and nc81base.sbk are not beside the lesson")
        props = UserProperties()
        done = initialize(chain, "initializeTrnr", props)
        self.assertEqual(done.skipped, ["linkDLL32 kernel32.dll"] + ["GetPrivateProfileIntA"] * 6)
        self.assertEqual(
            dict(props.items()),
            {
                "__experimentactive": 0, "__traineraddress": 0,
                "__trainernlv": 0.0, "__trainerplv": 0.0,
                "__trainerac1": 0, "__trainerdc1": 0, "__trainerac2": 0, "__trainerdc2": 0,
                "__trainersp3": 0, "__trainerdc3": 0, "__trainerfilament": 0,
            },
        )
        self.assertEqual(reaches_dll(chain, "sendFaults130"), "sendFaultsTd2000")
        for name in ("linkMemFunctions32", "unlinkMemFunctions32", "sendFaults130", "getExternalValue"):
            self.assertIsNone(run_if_assignments(chain, name, UserProperties()), name)


if __name__ == "__main__":
    unittest.main()
