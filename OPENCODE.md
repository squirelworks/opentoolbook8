# Open code and the core

DLLs and EXEs are the core, hardcoded side of ToolBook. This note does not decompile them, paste their code, or copy them into git. The `.sbk` files are the open side. So are the handler bodies the existing readers return from the NIDA `.tbk` files.

A name is open when a `to handle`, `to get`, or `to set` line in one of those scripts starts its body. A name is on the core side of the split when one of those scripts calls it and no script in the books below defines it. The body is not in the open books. A `linkDLL` or `linkDLL32` line is open-script text: it places a DLL filename beside an identifier. This note did not open that DLL, and it does not name an export inside it.

## Books and how a call was counted

The books are `nc81base.sbk`, `nc81recs.sbk`, `nc81test.sbk`, `nc81trnr.sbk`, `nida81.tbk`, and `9e954d01.tbk`. Script text comes from `resource_scripts` (type 10) and `shared_scripts` (type 19) in `opentoolbook.script`. Both readers returned. `nida81.tbk` has a zero type 19 directory, so `shared_scripts` returns no shared script. The four `.sbk` files each have one type 10 script and no type 19 script.

| File | Type 10 | Type 19 |
|---|---|---|
| `nc81base.sbk` | resource 129, one script | none |
| `nc81recs.sbk` | resource 268, one script | none |
| `nc81test.sbk` | resource 741, one script | none |
| `nc81trnr.sbk` | resource 428, one script | none |
| `nida81.tbk` | resources 158, 159, 160, 161, 165 | none |
| `9e954d01.tbk` | resources 372, 373, 374, 376 | resources 100, 101, 102, 103 |

A definition is a line that matches `to handle`, `to get`, or `to set`, then a name. A call site is an identifier followed by `(`, or the name in `send name`. Comments, from `--` to the end of the line, are skipped. Characters inside double quotes are skipped. A line inside a `linkDLL` or `linkDLL32` block declares an identifier, so that line is not a call. A parenthesis after `if`, `and`, `or`, or `when` groups an expression, so those four words are not calls. The same name in any letter case is one name.

A name seen at one call site is one call site. It is still listed.

The lists below are that type 10 and type 19 text. The button reader is separate, and the last section says what it adds.

## The quiz check is open code

`response = answer of this page` is open code inside `nc81test.sbk`. Type 10 resource 741 contains that line twice.

`to get gotoNextQuestionEx` sets `score = 0`, then sets `score = 100` when `response = answer of this page`. It then calls `storeQuestionResponse`. `to get gotoPreviousQuestionEx` uses the same comparison: `score = 100` on that line, and `score = 0` on the other branch, then the same `storeQuestionResponse` call.

`getquizResponse` and `storeQuestionResponse` are defined in that script, and the scripts call them, so they stay on the open side of the split.

- `to get getquizResponse` is called 4 times, all in `nc81test.sbk`.
- `to get storeQuestionResponse int test, int question, string response, int score` is called 3 times: twice in `nc81test.sbk`, and once in `9e954d01.tbk` type 19 resource 102.

Type 19 resource 102 of `9e954d01.tbk` is also open code. Its `to handle buttonClick` contains `response = answer of this page` once, sets `score = 100` or `score = 0`, and calls `storeQuestionResponse` once. `getquizResponse` does not appear there. That handler reads `text of field "response"`.

## Handlers defined in the open books

The four `.sbk` files define 218 handlers. Each name occurs once in those four files. The two `.tbk` files add 46 definition lines. Together that is 264 definition lines and 231 different names. Every definition is `to get` or `to handle`. These scripts contain no `to set`.

A call of one of these 231 names is open code calling open code. Those calls are not in the boundary list. 106 of the 231 names occur as calls in this type 10 and type 19 text.

### nc81base.sbk

Type 10 resource 129. 46 handlers, each a `to get`.

- `to get initializeBase  cmdLine`
- `to get placeLessonA`
- `to get placeLesson`
- `to get pushTranslationBook`
- `to get specialFunctions int key`
- `to get processHelpRequest`
- `to get processQuizScore int score`
- `to get gotoQuizPage`
- `to get getMenuPage`
- `to get gotoMenuPage`
- `to get setupMenuPageLocal`
- `to get setupMenuPageEx`
- `to get setupMenuPage string menupage, int mode`
- `to get clearMenuFlags`
- `to get clearMenuFlag index`
- `to get setMenuFlag index`
- `to get getMenuFlag index`
- `to get specifyMenuColors  color1, color2`
- `to get getMenuTextColor iColor`
- `to get setMenuTextColor string oName, iColor`
- `to get clearExperimentFlags`
- `to get setExperimentFlag int index`
- `to get checkExperimentFlags int count`
- `to get pushPage`
- `to get popPage`
- `to get savePage`
- `to get restorePage`
- `to get savePageAndBook string pagename`
- `to get restorePageAndBook`
- `to get clearPageList`
- `to get addToPageList`
- `to get processNewPage`
- `to get gotoPageList`
- `to get getExternalValue string exname`
- `to get openSubBook string pagename, string bookname`
- `to get closeSubBook`
- `to get getPreviousBook`
- `to get setSection string section`
- `to get getLogoBook`
- `to get setupAndGoto string pagename`
- `to get setupAndGotoEx int pagenumber`
- `to get setupAndWait string pagename`
- `to get setupAndGotoBook string pagename, string bookname`
- `to get setupAndGotoBookEx int pagenumber, string bookname`
- `to get setupAndWaitBook string pagename, string bookname`
- `to get getCurrentPath`

### nc81recs.sbk

Type 10 resource 268. 17 handlers, each a `to get`.

- `to get initializeRecs`
- `to get getStudentInfo`
- `to get getFirst`
- `to get getLast`
- `to get getId`
- `to get getClass`
- `to get openSession`
- `to get checkSession`
- `to get startSession`
- `to get restartSession`
- `to get closeSession`
- `to get bookmarkSession`
- `to get writeResponse int testno, int questionno, string response, int score`
- `to get writeResponseB int testno, int questionno, int partno, string response, int score`
- `to get writeResponseC int testno, int questionno, int total, int score`
- `to get PutVar int vNumber, string value`
- `to get GetVar int vNumber`

### nc81test.sbk

Type 10 resource 741. 90 handlers: 89 `to get` and one `to handle`.

- `to get initializeTest`
- `to get setQuizPass int pass`
- `to get saveResponse int test, int question, string response, int tries`
- `to get saveResponseB int test, int question, int part, string response, int tries`
- `to get saveEmbedded int test, int question, string response`
- `to get saveEmbeddedB int test, int question, int part, string response`
- `to get incorrectEmbedded`
- `to get setupFillinFields`
- `to get incorrectFillin string page1, string page2`
- `to get doNumeric int xkey`
- `to get doAlphabetic int xkey`
- `to get setupFormFields`
- `to get getNtries`
- `to get setupQuiz int objectiveCount`
- `to get loadM3Data filename`
- `to get setupQuizEx string qType, int objectiveCount, string page1, string page2, string page3`
- `to get setQuizStartPage int test`
- `to handle timerNotify timerId`
- `to get startCompletionPass`
- `to get startChangePass`
- `to get startCritiquePass`
- `to get gotoNextQuestionEx`
- `to get gotoPreviousQuestionEx`
- `to get setupQuizPage iPage`
- `to get quizDisplayTime int iPage`
- `to get quizTimedOut`
- `to get closeQuizTimer`
- `to get getquizResponse`
- `to get handleQuizClick vTarget`
- `to get returnToQuiz`
- `to get manageQuizButtons string vLabel`
- `to get handleQuizKey int key`
- `to get addQuestions int start, int stop, int count`
- `to get addQuestionsFromPool string pool, int count`
- `to get clearPool`
- `to get addObjectiveToPool int obj, int start, int stop, int count`
- `to get addObjectiveToPoolEx int obj, string questions, int count`
- `to get setupPool`
- `to get addQuesterQuestions int testno`
- `to get getNextQuestion`
- `to get getPreviousQuestion`
- `to get gotoNextQuestion int offset`
- `to get getQuestionIndex`
- `to get getQuestionReview`
- `to get wasQuestionAttempted`
- `to get getQuestionResponse`
- `to get storeQuestionResponse int test, int question, string response, int score`
- `to get storeQuestionSkipped int test, int question`
- `to get setQuestionIndex int index`
- `to get getQuestionAt int index`
- `to get getNextSkipped`
- `to get getPreviousSkipped`
- `to get getSkippedCount`
- `to get getObjectiveCount`
- `to get getObjectiveLevel`
- `to get getObjectiveScore int objective`
- `to get getQuizScore`
- `to get getQuizScorePM`
- `to get getCritiqueMode`
- `to get setQuizMode int mode`
- `to get getQuizMode`
- `to get getQuizPass`
- `to get incQuizPass`
- `to get saveQuizResults`
- `to get setExperimentNumber int number`
- `to get getExperimentNumber`
- `to get writeExperimentGrade int score`
- `to get clearRandomSet`
- `to get generateRandomSet iStart, iStop, iCount`
- `to get addToRandomSet iStart, iStop, iCount`
- `to get jumbleSet`
- `to get orderSet`
- `to get setRandomIndex iIndex`
- `to get getRandomIndex`
- `to get getNextRandom`
- `to get getRandom iIndex`
- `to get clearRandomSetX int numbers[] by reference`
- `to get generateRandomSetX int numbers[] by reference, int iStart, int iStop, int iCount`
- `to get addToRandomSetX int numbers[] by reference, int iStart, int iStop, int iCount`
- `to get jumbleSetX int numbers[] by reference`
- `to get orderSetX int numbers[] by reference`
- `to get setRandomIndexX int numbers[] by reference, iIndex`
- `to get getNextRandomX int numbers[] by reference`
- `to get getPreviousRandomX int numbers[] by reference`
- `to get getRandomX int numbers[] by reference, iIndex`
- `to get fixQuestionPages`
- `to get getTestInfo`
- `to get writeTestInfo string info`
- `to get getNextTest int nTests`
- `to get getRandomTest int nTests`

### nc81trnr.sbk

Type 10 resource 428. 65 handlers: 63 `to get` and two `to handle`.

- `to handle linkMemFunctions32`
- `to handle unlinkMemFunctions32`
- `to get initializeTrnr`
- `to get startExperiment`
- `to get endExperiment`
- `to get getTrainerAddress`
- `to get setTrainerAddress int address`
- `to get getTrainerType`
- `to get getTrainerCode string lookup`
- `to get getTrainerPort`
- `to get checkComm130`
- `to get sendFaults130 string faults`
- `to get saveSettings130`
- `to get loadSettings130`
- `to get studentControl130 logical student, logical faults`
- `to get checkCards130 int pc1, int pc2, int pc3`
- `to get checkComm130E`
- `to get startCai130E`
- `to get endCai130E`
- `to get readVoltages130E`
- `to get setVoltages130E int nlv, int plv`
- `to get setSwitches130E string onSwitches`
- `to get sendFaults130E string faults`
- `to get saveSettings130E`
- `to get loadSettings130E`
- `to get studentControl130E logical student, logical faults`
- `to get malfunctionWarning130E logical warning`
- `to get checkCards130E int pc1, int pc2, int pc3`
- `to get checkCommTd2000`
- `to get startCaiTd2000`
- `to get endCaiTd2000`
- `to get setVoltageTd2000 string voltage`
- `to get readVoltageTd2000`
- `to get setSwitchesTd2000 string onSwitches`
- `to get sendFaultsTd2000 string faults`
- `to get saveSettingsTd2000`
- `to get loadSettingsTd2000`
- `to get studentControlTd2000 logical student`
- `to get addressUnitTd2000 int address`
- `to get addressUnitsTd2000 int address1, int address2`
- `to get checkCardsTd2000  int pc1`
- `to get getExperimentStatus`
- `to get sendFaults5050 string faults`
- `to get clearFaults5050`
- `to get verifyMain5050 string onSwitches`
- `to get readMain5050`
- `to get verifyExternal5050 string onSwitches`
- `to get readExternal5050`
- `to get enablePower5050`
- `to get disablePower5050`
- `to get setSelector5050 int selector`
- `to get setProcess5050 int process`
- `to get checkComm205E`
- `to get readFrequency205E`
- `to get setFrequency205E real frequency`
- `to get readVolume205E`
- `to get readCard205E`
- `to get incVolume205E int delta`
- `to get decVolume205E int delta`
- `to get setVolume205E int volume`
- `to get setFault205E int fault`
- `to get eraseFault205E int fault`
- `to get clearFaults205E`
- `to get setPower205E string power`
- `to get setControl205E string control`

### nida81.tbk

13 handlers across five type 10 resources. Resources 158, 159, 160, and 161 each define the same two names. The four scripts are four different texts.

Type 10 resources 158, 159, 160, and 161, each:

- `To handle enterpage`
- `to handle updatesettings`

Type 10 resource 165:

- `to handle enterApplication`
- `to handle author`
- `to handle enterBook`
- `to handle enterPage`
- `to handle keyup key`

### 9e954d01.tbk

33 handlers: 22 in four type 10 resources and 11 in four type 19 resources. Resources 372, 373, and 374 each define the same five names. The three scripts are three different texts.

Type 10 resources 372, 373, and 374, each:

- `to handle enterPage`
- `to handle buttonClick`
- `to handle okClicked`
- `to handle keyUp`
- `to handle keyDown key`

Type 10 resource 376:

- `to handle enterSystem cmdLine`
- `to handle enterApplication`
- `to handle author`
- `to handle reader`
- `to handle enterBook`
- `to handle enterPage`
- `to handle keyup key`

Type 19 resource 100:

- `to handle EnterPage`
- `to handle leavePage`
- `to handle buttonClick`
- `to handle keyUp key`

Type 19 resource 101:

- `to handle keyChar key`

Type 19 resource 102:

- `to handle buttonClick`

Type 19 resource 103:

- `to handle enterPage`
- `to handle buttonClick`
- `to handle keyUp`
- `to handle keyDown key`
- `to handle keyChar key`

The same name in more than one resource is still one open name. `enterPage` is defined 11 times across `nida81.tbk` and `9e954d01.tbk`, under the spellings `enterpage`, `EnterPage`, and `enterPage`. `buttonClick`, `keyUp`, `keyDown`, `keyChar`, `okClicked`, `updatesettings`, `author`, `enterApplication`, and `enterBook` are the other names with more than one body.

## Boundary names

These 101 names are called from the type 10 and type 19 text above. No `to handle`, `to get`, or `to set` in these six books defines them. The body is not in the open books. The counts are call sites in that text.

78 of them are outside the OpenScript keyword list. 66 of those 78 also appear in a `linkDLL` or `linkDLL32` declaration in the open script. 12 are called with no such declaration. 23 are OpenScript keywords from `opentoolbook.keywords`, the keyword ids the reader uses to expand these scripts. The scripts call those keywords, and no open handler here defines them.

The 101 names account for 891 call sites.

### Called, and declared with linkDLL in the open script

The open script names a DLL file on the `linkDLL` line. The function body is not in the open books. The DLL was not opened. This list does not say which export inside that file implements the name.

| Name | Call sites | DLL file the script names |
|---|---|---|
| `GetPrivateProfileIntA` | 42 | `kernel32.dll` |
| `WritePrivateProfileStringA` | 28 | `kernel32.dll` |
| `GetPrivateProfileStringA` | 23 | `kernel32.dll` |
| `GlobalAlloc` | 13 | `kernel32.dll` |
| `GlobalFree` | 13 | `kernel32.dll` |
| `GlobalLock` | 13 | `kernel32.dll` |
| `GlobalUnlock` | 13 | `kernel32.dll` |
| `RecReadVariable` | 8 | `nc81rec.dll` |
| `RecWriteVariable` | 8 | `nc81rec.dll` |
| `SendMessageA` | 7 | `user32.dll` |
| `fileExists32` | 2 | `tbfile32.dll` |
| `GetSystemMetrics` | 2 | `user32.dll` |
| `GetTickCount` | 2 | `kernel32.dll` |
| `IntReadCardTd2000` | 2 | `nc81int.dll` |
| `IntSetFault205E` | 2 | `nc81int.dll` |
| `RecCheckStatus` | 2 | `nc81rec.dll` |
| `RecWriteResponse` | 2 | `nc81rec.dll` |
| `GetVersion` | 1 (one call site) | `kernel32.dll` |
| `IntAddressUnitsTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntAddressUnitTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntCheckComm130E` | 1 (one call site) | `nc81int.dll` |
| `IntCheckComm205E` | 1 (one call site) | `nc81int.dll` |
| `IntCheckCommTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntClearFaults5050` | 1 (one call site) | `nc81int.dll` |
| `IntDecVolume205E` | 1 (one call site) | `nc81int.dll` |
| `IntDisablePower5050` | 1 (one call site) | `nc81int.dll` |
| `IntEnablePower5050` | 1 (one call site) | `nc81int.dll` |
| `IntEndCai130E` | 1 (one call site) | `nc81int.dll` |
| `IntEndCaiTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntEraseFault205E` | 1 (one call site) | `nc81int.dll` |
| `IntIncVolume205E` | 1 (one call site) | `nc81int.dll` |
| `IntLoadSettings130E` | 1 (one call site) | `nc81int.dll` |
| `IntLoadSettingsTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntMalfunctionWarning130E` | 1 (one call site) | `nc81int.dll` |
| `IntReadCard130E` | 1 (one call site) | `nc81int.dll` |
| `IntReadCard205E` | 1 (one call site) | `nc81int.dll` |
| `IntReadExternal5050` | 1 (one call site) | `nc81int.dll` |
| `IntReadFrequency205E` | 1 (one call site) | `nc81int.dll` |
| `IntReadMain5050` | 1 (one call site) | `nc81int.dll` |
| `IntReadVoltages130E` | 1 (one call site) | `nc81int.dll` |
| `IntReadVoltageTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntReadVolume205E` | 1 (one call site) | `nc81int.dll` |
| `IntSaveSettings130E` | 1 (one call site) | `nc81int.dll` |
| `IntSaveSettingsTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntSendFault130E` | 1 (one call site) | `nc81int.dll` |
| `IntSendFault5050` | 1 (one call site) | `nc81int.dll` |
| `IntSendFaultTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntSetControl205E` | 1 (one call site) | `nc81int.dll` |
| `IntSetFrequency205E` | 1 (one call site) | `nc81int.dll` |
| `IntSetPower205E` | 1 (one call site) | `nc81int.dll` |
| `IntSetProcess5050` | 1 (one call site) | `nc81int.dll` |
| `IntSetSelector5050` | 1 (one call site) | `nc81int.dll` |
| `IntSetSwitches130E` | 1 (one call site) | `nc81int.dll` |
| `IntSetSwitchesTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntSetVoltages130E` | 1 (one call site) | `nc81int.dll` |
| `IntSetVoltageTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntStartCai130E` | 1 (one call site) | `nc81int.dll` |
| `IntStartCaiTd2000` | 1 (one call site) | `nc81int.dll` |
| `IntStudentControl130E` | 1 (one call site) | `nc81int.dll` |
| `IntStudentControlTd2000` | 1 (one call site) | `nc81int.dll` |
| `PostMessageA` | 1 (one call site) | `user32.dll` |
| `RecBookmarkSession` | 1 (one call site) | `nc81rec.dll` |
| `RecClearVariables` | 1 (one call site) | `nc81rec.dll` |
| `RecCloseSession` | 1 (one call site) | `nc81rec.dll` |
| `RecRestartSession` | 1 (one call site) | `nc81rec.dll` |
| `RecStartSession` | 1 (one call site) | `nc81rec.dll` |

`GetPrivateProfileIntA` is declared twice in `nc81base.sbk`, once as `INT GetPrivateProfileIntA(STRING, STRING, INT, STRING)` and once as `DWORD GetPrivateProfileIntA(STRING, STRING, INT, STRING)`. Both declarations name `kernel32.dll`.

Two further identifiers are declared this way and have no call site in these scripts, so they are not in the table: `GlobalHandle` beside `kernel32.dll`, and `IntClearFaults205E` beside `nc81int.dll`. Their bodies are not in the open books either.

### Called, with no handler and no linkDLL declaration

Each of these is called from the type 10 and type 19 text. No open handler defines it, and no `linkDLL` line in these scripts names it. The body is not in the open books.

| Name | Call sites |
|---|---|
| `isObject` | 128 |
| `flushMessageQueue` | 43 |
| `pointerString32` | 11 |
| `pointerLong32` | 7 |
| `readSwitches130a` | 4 |
| `loadTranslationText` | 3 |
| `readVoltages130a` | 3 |
| `pointerDouble32` | 2 |
| `saveTranslationText` | 2 |
| `WritePrivateProfileString` | 2 |
| `getCurrentDirectory` | 1 (one call site) |
| `getCurrentDrive` | 1 (one call site) |

`readVoltages130E` is an open handler in `nc81trnr.sbk`. `readVoltages130a` is a different name. `WritePrivateProfileStringA` is the identifier in the `kernel32.dll` declaration. `WritePrivateProfileString`, without the final `A`, is a different name. `pointerString`, `pointerLong`, and `pointerDouble` are keywords. `pointerString32`, `pointerLong32`, and `pointerDouble32` are the names the scripts call.

### Called OpenScript keywords

These words are keyword ids. The scripts call them with `name(...)` or `send name`. No handler in these books defines them. The body is not in the open books.

| Name | Call sites |
|---|---|
| `button` | 119 |
| `page` | 103 |
| `field` | 75 |
| `ansiToChar` | 19 |
| `increment` | 18 |
| `charCount` | 17 |
| `wordCount` | 17 |
| `uppercase` | 16 |
| `rectangle` | 14 |
| `beep` | 9 |
| `CharToAnsi` | 8 |
| `exit` | 8 |
| `itemCount` | 6 |
| `book` | 4 |
| `random` | 4 |
| `decrement` | 3 |
| `next` | 3 |
| `truncate` | 3 |
| `sizeToPage` | 2 |
| `timerStop` | 2 |
| `offset` | 1 (one call site) |
| `previous` | 1 (one call site) |
| `timerStart` | 1 (one call site) |

## Inline buttonClick scripts

`button_clicks` also returns script text. `nida81.tbk` has 119 of those handlers and `9e954d01.tbk` has 249. The `.sbk` files have none. Every one of them is `to handle buttonClick` (the spelling of `to handle` varies). They define no other name. `buttonClick` is already defined in the type 10 and type 19 scripts of `9e954d01.tbk`, so those bodies are open code for a name already listed above.

The call-site counts in the boundary tables do not include these button scripts. Two names show up only there, both in `nida81.tbk`, and no open handler defines them. The body is not in the open books.

| Name | Call sites in inline `buttonClick` scripts |
|---|---|
| `verifyswitches130a` | 4 |
| `verifyvoltages130a` | 3 |

`readVoltages130a` has 3 call sites in the type 10 scripts, counted above, and 3 more in these `nida81.tbk` button scripts.

Counted this way, the boundary list is 103 names: the 101 from type 10 and type 19, plus `verifyswitches130a` and `verifyvoltages130a`.
