# opentoolbook8

opentoolbook8 is a ToolBook 8 reader. It opens a book, draws the page, and runs the book's OpenScript.

OpenScript is the language. Book script is the source text in a `.sbk` or a `.tbk`. Core is the DLLs and EXEs. Those binaries are not in this repository. The ToolBook 8.1 authoring installer is the one Denny Dedmore's reinstall page lists. That note, and the rule against serial numbers, is in `DENNY-RUNTIME.md`.

The 16-bit runtime the notes refer to is `TB80RTM` and `TB80BAS`. The notes and the unpacker live in the other repositories: `tbdecompile`, `tbworldview`, `squirreldra`, and `toolbookunpacker`. Foolbook is the other viewer. Do not import Foolbook, do not copy its painter, and do not treat Foolbook as right where it disagrees with ToolBook. ToolBook 8 is the target. A painted value comes from a reader. A reader comes from bytes that repeat across the lesson, not from one example and not from a guess that makes the picture look finished.

A record is one object in the book's directory, with a file position and a length. A follow-up read is the two bytes stored after that body when the entry asks for them. In `TB80BAS`, the message after a load is `0xE`, passed to the procedure at the start of the class slot. The book report leaves that constant out. This tree returns that pointer. It does not call the DLL.

## Commands

`python3 -m opentoolbook path/to/book.tbk` opens the book, the way ToolBook opens it. The window shows the page the startup handlers land on. Those handlers are `enterSystem`, then `enterApplication`, and the calls they make: `enterapplication`, `entersystem`, `gotopagelist`, `opensession`, and the `initialize*` calls. A quoted `go to page` in a branch the reader takes is that page. A missing `sysLevel` is `reader`. When the handlers do not name a page, the window opens on the first page stored in the book. On Logic Families that first page's `enterPage` goes to `P0` of the book `getLogoBook` names, which is `nida81.tbk` unless `logo81.tbk` or `mrj81.tbk` is found by the same search as the report. `linkDLL` is not called. `forward` is not executed. `gotoPageList` walks names that are not quoted, and the session DLL is not called, so a resumed session is not the page that opens.

`python3 -m opentoolbook path/to/book.tbk --report` prints the book report: the record count, the follow-up reads, the files the book names, and the startup call names. It does not open a window. `--report path/to/book.tbk` is the same report.

`python3 -m opentoolbook --show P300 path/to/book.tbk` opens a Tk window on the page id you typed. It draws that page and runs the OpenScript the window knows for that page. It does not follow the startup handlers to the book's opening page. `--home` is not consulted for `--show`. With a book and no `--report`, `--home` is a place to search for companion books.

Companion books such as `nida81.tbk` and `nc81*.sbk` are looked up, for the report and for opening the book, in the book's directory, then in the parent of that directory, then in `--home`. The match ignores case. `SETTLED.md` has the full order. A quoted `of book` click looks only for that exact filename in the directory of the book passed to `--show`.

## What the window does

- On `P10` the field `first` reads `Hello Student, this lesson is about:`.
- On a quiz page opened with no quiz running, OK, Next, and Skip draw the next page, and Back draws the previous page.
- A button that quotes a page opens that page. Next on `P300` opens `P400`. Selection1 names `P310` of `nida81.tbk`.
- The background, rectangles, ellipses, lines, class `0x10` polygons, fields, and button pictures are painted. The page walk also finds classes `0xD`, `0x11`, `0x13`, `0x15`, and `0x19`, and the window does not paint those. A group is not a paint; its children are. Class `0x12` pies and class `0x17` records are outside that walk and are not painted. Pattern 254 is a solid fill. Pattern 253 paints no fill. Another pattern byte is not drawn as a hatch.
- The OpenScript that runs is the subset in `SETTLED.md`: some `enterPage` field writes, a quoted `go to page`, `send next`, `send previous`, and the quiz-button cases. Opening the book follows that quoted `go to page` in the startup handlers and in the entry page's `enterPage`. `forward` has no body here. A `linkDLL` line is not called.

Also in this tree, and named in `SETTLED.md`: the object directory and the two-byte follow-up, the class-slot lookup for message `0xE` (index 0, not a DLL call), the install list (`toolbook.lst`), and the system books a book binds and pushes onto `sysBooks`. There is no authoring path.

## Notes

`SETTLED.md` is the behavior this reader implements. `FINDINGS.md` is what the bytes of `9e954d01.tbk` repeat. `RESEARCH.md` is the product and engine notes, and each claim there names its source. `OPENCODE.md` splits book script from the core. `DENNY-RUNTIME.md` and `DENNY-OBJECTS.md` are his site. `INSTRUCTOR-LAYOUT.md` is the Instructor 8.1 trees. `TB115-SYSTEM.md` is the 11.5 system books. `GHIDRA-INSTRUCTOR.md` records a finished headless pass. It is not an instruction to run Ghidra.

## From scratch

You need Python 3.11 or newer. The repository is private, so download it from the GitHub page while you are logged in. That is the Code button, then Download ZIP. The file is `opentoolbook8-main.zip`. Put that file in `~/FU`.

Check Python:

```bash
python3 --version
```

If that is older than 3.11, install a newer Python before the block below. On Debian or Ubuntu, `python3 -m venv` also needs the venv package. The page window needs Tk for that same `python3`:

```bash
sudo apt install python3-venv python3-pip python3-tk
```

Paste this into a terminal after the zip is in `~/FU`. It unpacks the zip, renames the folder to `opentoolbook8`, makes a virtualenv, installs, and prints the command list. If the zip is still in Downloads, move it first: `mkdir -p ~/FU && mv ~/Downloads/opentoolbook8-main.zip ~/FU/`.

```bash
mkdir -p ~/FU
cd ~/FU
rm -rf opentoolbook8-main
python3 -m zipfile -e opentoolbook8-main.zip ~/FU
rm -rf opentoolbook8
mv opentoolbook8-main opentoolbook8
cd opentoolbook8
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -e .
python3 -m opentoolbook --help
```

`source .venv/bin/activate` is what makes `python3` see this install. Each new terminal starts without it. From `~/FU/opentoolbook8`, run `source .venv/bin/activate` again before the commands below.

The commands below take a book that is already on your computer. Put its path in the command. The first command opens the book on its opening page. `--report` prints the report and does not open a window. `--show` opens the page id written in that command. `--home` names a ToolBook install folder to search and report.

```bash
python3 -m opentoolbook path/to/book.tbk
python3 -m opentoolbook path/to/book.tbk --report
python3 -m opentoolbook --show P300 path/to/book.tbk
python3 -m opentoolbook --home path/to/TBK path/to/book.tbk
python3 -m unittest discover -s tests
```

The tests use synthetic books. `OPENTOOLBOOK_TBK` points the extra tests at a lesson book.

```bash
OPENTOOLBOOK_TBK=path/to/book.tbk python3 -m unittest discover -s tests
```

A newer zip, with the virtualenv already in place:

```bash
cd ~/FU
rm -rf opentoolbook8-main
python3 -m zipfile -e opentoolbook8-main.zip ~/FU
cp -a opentoolbook8-main/. opentoolbook8/
cd opentoolbook8
source .venv/bin/activate
python3 -m pip install -e .
```

### Windows

In PowerShell, `py -3 --version` needs to say 3.11 or newer. Download the same zip while logged in, and leave it in Downloads. Then paste this. It unpacks into `%USERPROFILE%\FU\opentoolbook8`.

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\FU" | Out-Null
Set-Location "$env:USERPROFILE\FU"
if (Test-Path opentoolbook8-main) { Remove-Item -Recurse -Force opentoolbook8-main }
if (Test-Path opentoolbook8) { Remove-Item -Recurse -Force opentoolbook8 }
Expand-Archive -Path "$env:USERPROFILE\Downloads\opentoolbook8-main.zip" -DestinationPath .
Rename-Item opentoolbook8-main opentoolbook8
Set-Location opentoolbook8
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e .
python -m opentoolbook --help
```

If activation says running scripts is disabled, run this once, then the activate line again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

A new PowerShell window needs `.\.venv\Scripts\Activate.ps1` from the repo folder before the next commands. Use `python` in that window. The first command opens the book on its opening page. `--report` prints the report and does not open a window. `--show` opens the page id written in that command.

```powershell
python -m opentoolbook path\to\book.tbk
python -m opentoolbook path\to\book.tbk --report
python -m opentoolbook --show P300 path\to\book.tbk
python -m opentoolbook --home path\to\TBK path\to\book.tbk
python -m unittest discover -s tests
```

A newer zip on Windows, with the virtualenv already in place:

```powershell
Set-Location "$env:USERPROFILE\FU"
if (Test-Path opentoolbook8-main) { Remove-Item -Recurse -Force opentoolbook8-main }
Expand-Archive -Path "$env:USERPROFILE\Downloads\opentoolbook8-main.zip" -DestinationPath .
Get-ChildItem -Force opentoolbook8-main | Copy-Item -Destination opentoolbook8 -Recurse -Force
Set-Location opentoolbook8
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

### Git

If Git is already signed in, this is the same install with clone instead of the zip:

```bash
mkdir -p ~/FU
cd ~/FU
git clone https://github.com/squirelworks/opentoolbook8.git
cd opentoolbook8
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -U pip
python3 -m pip install -e .
python3 -m opentoolbook --help
```

Later: `git pull --ff-only origin main`, then `python3 -m pip install -e .` with the virtualenv activated.
