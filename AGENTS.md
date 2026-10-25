# opentoolbook8

You own this repository. The user does not review your work.

- Commit on `main` and push to `origin main`.
- Do not open a pull request. Do not create a branch. Do not ask the user to check, review, or merge anything.
- Run `python3 -m unittest discover -s tests` before the push. If a test fails, fix it and run the tests again. Do not push a failing tree.
- One settled behavior per push. If it is not in `SETTLED.md`, do not invent it. Add the behavior to `SETTLED.md` in the same push.
- Write notes into the repo in the same push that produces them. Product and engine notes go in `RESEARCH.md`, with the source named. A behavior the reader implements goes in `SETTLED.md`.
- OpenScript is the language. Book script is the source text in a `.sbk` or a `.tbk`. Core is the DLLs and EXEs.
- `python3 -m opentoolbook book.tbk` opens the book on the page its startup handlers name, or on the first stored page when they do not. `--report` prints the report and does not open a window. `--show PAGE` draws that page id and does not follow those handlers. `linkDLL` and `forward` are not executed. `gotoPageList` does not name a quoted page, so a resumed session is not the page that opens.
- The ToolBook 8.1 authoring installer is the one Denny Dedmore's reinstall page lists. That note is in `DENNY-RUNTIME.md`. Never record a serial number. Never commit a proprietary binary or DLL.
- Do not force-disassemble unknown data. No `ForceDisassembleC8` and no `ForceDisassemblePrologues`. Describe code that a call path or a clean import reached. Do not run Ghidra.

opentoolbook8 is a ToolBook 8 reader. It opens a book, draws the page, and runs the book's OpenScript. Foolbook is the other viewer. Do not import Foolbook, do not copy its painter, and do not treat Foolbook as right where it disagrees with ToolBook. ToolBook 8 is the target. A painted value comes from a reader. A reader comes from bytes that repeat across the lesson, not from one example and not from a guess that makes the picture look finished. Each push makes the window or the engine do something a person can see. Tests pass before the push. SETTLED.md lists every new fact that push implements. FINDINGS.md is only for a byte the viewer is blocked on. A push that only adds a note is a failed push.
