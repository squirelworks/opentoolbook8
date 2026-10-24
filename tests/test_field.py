"""Field text is word 1 of the block at record +0x24."""

import os
import unittest
from pathlib import Path

from opentoolbook.field import field_text, page_ids

# The copyright field on page P0 of 9e954d01.tbk.
COPYRIGHT = 'Copyright ©  Nida Corporation 1997 - 2002  \r\nThis software and its supporting programs are protected by federal copyright law and all            rights are reserved by Nida Corporation.  No part or section of this software or its supporting    programs may be copied, distributed, transmitted in any form or medium electronic or           otherwise, disclosed to third parties, or used in any manner not specified in the  License            Agreement furnished by Nida Corporation.  This courseware was created with Asymetrix ToolBook I I .'


class FieldTextTests(unittest.TestCase):
    def test_p0_copyright_field(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        self.assertEqual(field_text(data, "P0", "Copyright"), COPYRIGHT)

    def test_page_ids_include_p0_and_p430(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        data = Path(path).read_bytes()
        found = page_ids(data)
        self.assertIn("P0", found)
        self.assertIn("P430", found)


if __name__ == "__main__":
    unittest.main()
