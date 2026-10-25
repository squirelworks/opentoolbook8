# opentoolbook8

Rebuilding ToolBook 8 from analysis, so a book can run on a current operating system.

The 16-bit runtime is `TB80RTM` and `TB80BAS`. The notes and the unpacker live in the other repositories: `tbdecompile`, `tbworldview`, `squirreldra`, and `toolbookunpacker`. Foolbook is the viewer that already opens pages. Foolcourse, Foollege, and Foolversity sit above that viewer. This repository is the runtime those books need: object records, the class procedure a load calls, and the NIDA course shell around a lesson.

A record is one object in the book's directory, with a file position and a length.
A follow-up read is the two bytes stored after that body when the entry asks for them.
The message after a load is 0xe, passed to the procedure at the start of the class slot, and the report leaves that constant out.

What works in this tree:

- A page window: `python3 -m opentoolbook --show P300 path/to/book.tbk` draws that page.
- The object directory, the body read, and the two-byte follow-up when the entry asks for one.
- The class procedure for message `0xE`. It is the far pointer at the start of that class's `0x76`-byte slot. The lookup uses index 0.
- The NIDA menu export (`nida:m3search`), the disc table (`CAILT.DAT`), the install list (`toolbook.lst`), and the system books a lesson names.
- One rating folder from the key-disk creator: the description, the shift calendar, the encoded settings line, and the three versioned records.

opentoolbook8 is a ToolBook 8 reader. It opens a book, draws the page, and runs the book's OpenScript. Foolbook is the other viewer. Do not import Foolbook, do not copy its painter, and do not treat Foolbook as right where it disagrees with ToolBook. ToolBook 8 is the target. A painted value comes from a reader. A reader comes from bytes that repeat across the lesson, not from one example and not from a guess that makes the picture look finished. Each push makes the window or the engine do something a person can see. Tests pass before the push. SETTLED.md lists every new fact that push implements. FINDINGS.md is only for a byte the viewer is blocked on. A push that only adds a note is a failed push.

`SETTLED.md` is the behavior this reader implements. `FINDINGS.md` is what the bytes of `9e954d01.tbk` repeat. `RESEARCH.md` is the product and engine notes, and each claim there names its source.

On a live stop with the lesson already open, handle `0x0C1E` had class word `0x0001`. The lookup returned `0x2BAF:0000`, the live selector of the class dispatcher, and `ECX` was `0x76`. The 412-byte record takes the same path. This boot did not reach that return.

## From scratch

You need Python 3.11 or newer. The repository is private, so download it from the GitHub page while you are logged in. That is the Code button, then Download ZIP. The file is `opentoolbook8-main.zip`. Put that file in `~/FU`.

Check Python:

```bash
python3 --version
```

If that is older than 3.11, install a newer Python before the block below. On Debian or Ubuntu, `python3 -m venv` also needs the venv package:

```bash
sudo apt install python3-venv python3-pip
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

The commands below take a book or a NIDA folder that is already on your computer. Put its path in the command.

```bash
python3 -m opentoolbook path/to/book.tbk
python3 -m opentoolbook --show P300 path/to/book.tbk
python3 -m opentoolbook --catalog path/to/courses.xml
python3 -m opentoolbook --catalog path/to/TBK
python3 -m opentoolbook --cailt path/to/CAILT.DAT 9E954D01
python3 -m opentoolbook --home path/to/TBK path/to/book.tbk
python3 -m opentoolbook --keydisk path/to/rating
python3 -m unittest discover -s tests
```

The tests use synthetic books and a synthetic menu. `OPENTOOLBOOK_TBK` points the extra tests at a lesson book.

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

A new PowerShell window needs `.\.venv\Scripts\Activate.ps1` from the repo folder before the next commands. Use `python` in that window:

```powershell
python -m opentoolbook path\to\book.tbk
python -m opentoolbook --show P300 path\to\book.tbk
python -m opentoolbook --catalog path\to\courses.xml
python -m opentoolbook --catalog path\to\TBK
python -m opentoolbook --cailt path\to\CAILT.DAT 9E954D01
python -m opentoolbook --home path\to\TBK path\to\book.tbk
python -m opentoolbook --keydisk path\to\rating
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
