"""Handlers whose bodies are in the nc81 system books.

The names come from the type 10 source. The reader does not call them.
"""

import os
import unittest
from pathlib import Path

from opentoolbook.script import book_handlers, resource_scripts

from lesson import companion


# kind, name. Measured from the type 10 source of each book.
HANDLERS = {
    "nc81base.sbk": (
        ("get", "initializeBase"),
        ("get", "placeLessonA"),
        ("get", "placeLesson"),
        ("get", "pushTranslationBook"),
        ("get", "specialFunctions"),
        ("get", "processHelpRequest"),
        ("get", "processQuizScore"),
        ("get", "gotoQuizPage"),
        ("get", "getMenuPage"),
        ("get", "gotoMenuPage"),
        ("get", "setupMenuPageLocal"),
        ("get", "setupMenuPageEx"),
        ("get", "setupMenuPage"),
        ("get", "clearMenuFlags"),
        ("get", "clearMenuFlag"),
        ("get", "setMenuFlag"),
        ("get", "getMenuFlag"),
        ("get", "specifyMenuColors"),
        ("get", "getMenuTextColor"),
        ("get", "setMenuTextColor"),
        ("get", "clearExperimentFlags"),
        ("get", "setExperimentFlag"),
        ("get", "checkExperimentFlags"),
        ("get", "pushPage"),
        ("get", "popPage"),
        ("get", "savePage"),
        ("get", "restorePage"),
        ("get", "savePageAndBook"),
        ("get", "restorePageAndBook"),
        ("get", "clearPageList"),
        ("get", "addToPageList"),
        ("get", "processNewPage"),
        ("get", "gotoPageList"),
        ("get", "getExternalValue"),
        ("get", "openSubBook"),
        ("get", "closeSubBook"),
        ("get", "getPreviousBook"),
        ("get", "setSection"),
        ("get", "getLogoBook"),
        ("get", "setupAndGoto"),
        ("get", "setupAndGotoEx"),
        ("get", "setupAndWait"),
        ("get", "setupAndGotoBook"),
        ("get", "setupAndGotoBookEx"),
        ("get", "setupAndWaitBook"),
        ("get", "getCurrentPath"),
    ),
    "nc81recs.sbk": (
        ("get", "initializeRecs"),
        ("get", "getStudentInfo"),
        ("get", "getFirst"),
        ("get", "getLast"),
        ("get", "getId"),
        ("get", "getClass"),
        ("get", "openSession"),
        ("get", "checkSession"),
        ("get", "startSession"),
        ("get", "restartSession"),
        ("get", "closeSession"),
        ("get", "bookmarkSession"),
        ("get", "writeResponse"),
        ("get", "writeResponseB"),
        ("get", "writeResponseC"),
        ("get", "PutVar"),
        ("get", "GetVar"),
    ),
    "nc81test.sbk": (
        ("get", "initializeTest"),
        ("get", "setQuizPass"),
        ("get", "saveResponse"),
        ("get", "saveResponseB"),
        ("get", "saveEmbedded"),
        ("get", "saveEmbeddedB"),
        ("get", "incorrectEmbedded"),
        ("get", "setupFillinFields"),
        ("get", "incorrectFillin"),
        ("get", "doNumeric"),
        ("get", "doAlphabetic"),
        ("get", "setupFormFields"),
        ("get", "getNtries"),
        ("get", "setupQuiz"),
        ("get", "loadM3Data"),
        ("get", "setupQuizEx"),
        ("get", "setQuizStartPage"),
        ("handle", "timerNotify"),
        ("get", "startCompletionPass"),
        ("get", "startChangePass"),
        ("get", "startCritiquePass"),
        ("get", "gotoNextQuestionEx"),
        ("get", "gotoPreviousQuestionEx"),
        ("get", "setupQuizPage"),
        ("get", "quizDisplayTime"),
        ("get", "quizTimedOut"),
        ("get", "closeQuizTimer"),
        ("get", "getquizResponse"),
        ("get", "handleQuizClick"),
        ("get", "returnToQuiz"),
        ("get", "manageQuizButtons"),
        ("get", "handleQuizKey"),
        ("get", "addQuestions"),
        ("get", "addQuestionsFromPool"),
        ("get", "clearPool"),
        ("get", "addObjectiveToPool"),
        ("get", "addObjectiveToPoolEx"),
        ("get", "setupPool"),
        ("get", "addQuesterQuestions"),
        ("get", "getNextQuestion"),
        ("get", "getPreviousQuestion"),
        ("get", "gotoNextQuestion"),
        ("get", "getQuestionIndex"),
        ("get", "getQuestionReview"),
        ("get", "wasQuestionAttempted"),
        ("get", "getQuestionResponse"),
        ("get", "storeQuestionResponse"),
        ("get", "storeQuestionSkipped"),
        ("get", "setQuestionIndex"),
        ("get", "getQuestionAt"),
        ("get", "getNextSkipped"),
        ("get", "getPreviousSkipped"),
        ("get", "getSkippedCount"),
        ("get", "getObjectiveCount"),
        ("get", "getObjectiveLevel"),
        ("get", "getObjectiveScore"),
        ("get", "getQuizScore"),
        ("get", "getQuizScorePM"),
        ("get", "getCritiqueMode"),
        ("get", "setQuizMode"),
        ("get", "getQuizMode"),
        ("get", "getQuizPass"),
        ("get", "incQuizPass"),
        ("get", "saveQuizResults"),
        ("get", "setExperimentNumber"),
        ("get", "getExperimentNumber"),
        ("get", "writeExperimentGrade"),
        ("get", "clearRandomSet"),
        ("get", "generateRandomSet"),
        ("get", "addToRandomSet"),
        ("get", "jumbleSet"),
        ("get", "orderSet"),
        ("get", "setRandomIndex"),
        ("get", "getRandomIndex"),
        ("get", "getNextRandom"),
        ("get", "getRandom"),
        ("get", "clearRandomSetX"),
        ("get", "generateRandomSetX"),
        ("get", "addToRandomSetX"),
        ("get", "jumbleSetX"),
        ("get", "orderSetX"),
        ("get", "setRandomIndexX"),
        ("get", "getNextRandomX"),
        ("get", "getPreviousRandomX"),
        ("get", "getRandomX"),
        ("get", "fixQuestionPages"),
        ("get", "getTestInfo"),
        ("get", "writeTestInfo"),
        ("get", "getNextTest"),
        ("get", "getRandomTest"),
    ),
    "nc81trnr.sbk": (
        ("handle", "linkMemFunctions32"),
        ("handle", "unlinkMemFunctions32"),
        ("get", "initializeTrnr"),
        ("get", "startExperiment"),
        ("get", "endExperiment"),
        ("get", "getTrainerAddress"),
        ("get", "setTrainerAddress"),
        ("get", "getTrainerType"),
        ("get", "getTrainerCode"),
        ("get", "getTrainerPort"),
        ("get", "checkComm130"),
        ("get", "sendFaults130"),
        ("get", "saveSettings130"),
        ("get", "loadSettings130"),
        ("get", "studentControl130"),
        ("get", "checkCards130"),
        ("get", "checkComm130E"),
        ("get", "startCai130E"),
        ("get", "endCai130E"),
        ("get", "readVoltages130E"),
        ("get", "setVoltages130E"),
        ("get", "setSwitches130E"),
        ("get", "sendFaults130E"),
        ("get", "saveSettings130E"),
        ("get", "loadSettings130E"),
        ("get", "studentControl130E"),
        ("get", "malfunctionWarning130E"),
        ("get", "checkCards130E"),
        ("get", "checkCommTd2000"),
        ("get", "startCaiTd2000"),
        ("get", "endCaiTd2000"),
        ("get", "setVoltageTd2000"),
        ("get", "readVoltageTd2000"),
        ("get", "setSwitchesTd2000"),
        ("get", "sendFaultsTd2000"),
        ("get", "saveSettingsTd2000"),
        ("get", "loadSettingsTd2000"),
        ("get", "studentControlTd2000"),
        ("get", "addressUnitTd2000"),
        ("get", "addressUnitsTd2000"),
        ("get", "checkCardsTd2000"),
        ("get", "getExperimentStatus"),
        ("get", "sendFaults5050"),
        ("get", "clearFaults5050"),
        ("get", "verifyMain5050"),
        ("get", "readMain5050"),
        ("get", "verifyExternal5050"),
        ("get", "readExternal5050"),
        ("get", "enablePower5050"),
        ("get", "disablePower5050"),
        ("get", "setSelector5050"),
        ("get", "setProcess5050"),
        ("get", "checkComm205E"),
        ("get", "readFrequency205E"),
        ("get", "setFrequency205E"),
        ("get", "readVolume205E"),
        ("get", "readCard205E"),
        ("get", "incVolume205E"),
        ("get", "decVolume205E"),
        ("get", "setVolume205E"),
        ("get", "setFault205E"),
        ("get", "eraseFault205E"),
        ("get", "clearFaults205E"),
        ("get", "setPower205E"),
        ("get", "setControl205E"),
    ),
}


class SystemBookHandlerTests(unittest.TestCase):
    def test_nc81base_nc81recs_nc81test_nc81trnr_handlers(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        self.assertEqual(set(HANDLERS), {
            "nc81base.sbk",
            "nc81recs.sbk",
            "nc81test.sbk",
            "nc81trnr.sbk",
        })
        seen = []
        for name, expected in HANDLERS.items():
            script = resource_scripts(companion(path, name).read_bytes())
            self.assertEqual(len(script), 1)
            found = book_handlers(name, script[0].source)
            self.assertEqual(
                [(item.book, item.kind, item.name) for item in found],
                [(name, kind, handler) for kind, handler in expected],
            )
            seen.extend(item.name.lower() for item in found)
            self.assertNotIn("set", {item.kind for item in found})
        self.assertEqual(len(seen), len(set(seen)))
        self.assertIn("handlequizclick", seen)
        self.assertIn("getquizscore", seen)
        self.assertIn("gotonextquestionex", seen)
        self.assertIn("timernotify", seen)

    def test_nc81base_nc81recs_nc81test_nc81trnr_handler_split(self):
        path = os.environ.get("OPENTOOLBOOK_TBK")
        if not path or not os.path.isfile(path):
            self.skipTest("set OPENTOOLBOOK_TBK to 9e954d01.tbk")
        samples = {
            ("nc81base.sbk", "initializeBase"): "cmdLine",
            ("nc81base.sbk", "specifyMenuColors"): "color1, color2",
            ("nc81base.sbk", "getCurrentPath"): "",
            ("nc81base.sbk", "getExternalValue"): "string exname",
            ("nc81recs.sbk", "initializeRecs"): "",
            ("nc81recs.sbk", "writeResponse"): "int testno, int questionno, string response, int score",
            ("nc81test.sbk", "timerNotify"): "timerId",
            ("nc81test.sbk", "setupQuizEx"): "string qType, int objectiveCount, string page1, string page2, string page3",
            ("nc81test.sbk", "clearRandomSetX"): "int numbers[] by reference",
            ("nc81test.sbk", "getNextQuestion"): "",
            ("nc81trnr.sbk", "linkMemFunctions32"): "",
            ("nc81trnr.sbk", "sendFaults130"): "string faults",
            ("nc81trnr.sbk", "checkCardsTd2000"): "int pc1",
            ("nc81trnr.sbk", "getTrainerCode"): "string lookup",
        }
        checked = set()
        for name in HANDLERS:
            source = resource_scripts(companion(path, name).read_bytes())[0].source
            found = book_handlers(name, source)
            self.assertEqual(len(found), len(HANDLERS[name]))
            for item in found:
                head_end = item.body_start
                self.assertGreater(head_end, 0)
                self.assertEqual(source[head_end - 1], "\n")
                previous = source.rfind("\n", 0, head_end - 1)
                line = source[previous + 1:head_end - 1].rstrip("\r")
                prefix = f"to {item.kind} {item.name}"
                self.assertTrue(line == prefix or line.startswith(prefix + " ") or line.startswith(prefix + "\t"))
                self.assertEqual(item.arguments, line[len(prefix):].strip())
                key = (item.book, item.name)
                if key in samples:
                    self.assertEqual(item.arguments, samples[key])
                    checked.add(key)
            if name == "nc81base.sbk":
                external = next(item for item in found if item.name == "getExternalValue")
                self.assertTrue(source[external.body_start:].startswith("\r\n"))
            if name == "nc81trnr.sbk":
                trainer = next(item for item in found if item.name == "getTrainerCode")
                self.assertTrue(source[trainer.body_start:].startswith("    local string data"))
        self.assertEqual(checked, set(samples))


if __name__ == "__main__":
    unittest.main()
