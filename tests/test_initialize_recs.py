"""``initializeRecs`` fills ``__lessonVars`` and ``GetVar`` reads it back."""

import os
import unittest
from pathlib import Path

from opentoolbook.initialize import initialize, run_literals
from opentoolbook.props import UserProperties
from opentoolbook.send import Chain

RECS = """to get initializeRecs
\tlocal int error
\tsystem string __lessonVars[100]

\terror = getStudentInfo()

\tstep i from 1 to 100
\t\t__lessonVars[i] = "1"
\tend step

\treturn 0
end
"""

GETVAR = """to get GetVar int vNumber
\tsystem string __lessonVars[100]
\tlocal string result
\tresult = ""
\tif  (vNumber > 0)  and (vNumber <= 100)  then
\t\tresult = __lessonVars[vNumber]
\tend if
\treturn result
end
"""


class InitializeRecsTests(unittest.TestCase):
    def test_get_var_returns_what_initialize_recs_set(self):
        chain = Chain((("nc81recs.sbk", {"initializerecs": RECS, "getvar": GETVAR}),))
        props = UserProperties()
        done = initialize(chain, "initializeRecs", props)
        self.assertEqual(done.skipped, ["getStudentInfo"])
        self.assertEqual(done.value, 0)
        self.assertEqual(len(done.assigned), 100)
        self.assertEqual(props.get("__lessonVars[1]"), "1")
        self.assertEqual(props.get("__LESSONVARS[100]"), "1")
        self.assertIsNone(props.get("__lessonVars[101]"))
        self.assertEqual(initialize(chain, "GetVar", props, (7,)).value, "1")
        self.assertEqual(initialize(chain, "GetVar", props, (0,)).value, "")
        self.assertEqual(initialize(chain, "GetVar", props, (101,)).value, "")

    def test_a_step_with_unknown_bounds_is_skipped(self):
        props = UserProperties()
        done = run_literals("step i from 1 to __count\n  __x[i] = 1\nend step", props)
        self.assertEqual(done.skipped, ["step i from 1 to __count"])
        self.assertEqual(props.items(), ())

    def test_get_first_is_unchanged(self):
        from opentoolbook.enter import get_first

        props = UserProperties()
        run_literals(RECS, props)
        self.assertEqual(get_first(props.get("__studentFirst")), "Student")

    def test_the_real_system_book(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        from opentoolbook.send import handler_chain
        from opentoolbook.shelf import search_roots

        lesson = Path(path)
        chain = handler_chain(lesson.read_bytes(), lesson.name, search_roots(lesson, None))
        if chain.find("initializeRecs") is None:
            self.skipTest("nc81recs.sbk is not beside the lesson")
        props = UserProperties()
        done = initialize(chain, "initializeRecs", props)
        self.assertEqual(done.skipped, ["getStudentInfo"])
        self.assertEqual(initialize(chain, "GetVar", props, (42,)).value, "1")
        self.assertIsNone(props.get("__studentFirst"))


if __name__ == "__main__":
    unittest.main()
