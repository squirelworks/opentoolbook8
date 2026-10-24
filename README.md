# opentoolbook8

Rebuilding ToolBook 8 from analysis, so a book can run on a current operating system.

The 16-bit runtime is `TB80RTM` and `TB80BAS`. The notes and the unpacker live in the other repositories: `tbdecompile`, `tbworldview`, `squirreldra`, and `toolbookunpacker`. Foolbook is the viewer that already opens pages. Foolcourse, Foollege, and Foolversity sit above that viewer. This repository is the runtime those books need: object records, the class procedure a load calls, and the NIDA course shell around a lesson.

What works in this tree:

- The object directory, the body read, and the two-byte follow-up when the entry asks for one.
- The class procedure for message `0xE`. It is the far pointer at the start of that class's `0x76`-byte slot. The lookup uses index 0.
- The NIDA menu export (`nida:m3search`), the disc table (`CAILT.DAT`), the install list (`toolbook.lst`), and the system books a lesson names.
- One rating folder from the key-disk creator: the description, the shift calendar, the encoded settings line, and the three versioned records.

A page is not drawn here, and OpenScript is not run here. Those are what the viewer already does.

On a live stop with the lesson already open, handle `0x0C1E` had class word `0x0001`. The lookup returned `0x2BAF:0000`, the live selector of the class dispatcher, and `ECX` was `0x76`. The 412-byte record takes the same path. This boot did not reach that return.

## From scratch

You need Git and Python 3.11 or newer. Check both:

```bash
git --version
python3 --version
```

If `python3 --version` is older than 3.11, install a newer Python before the block below. On Debian or Ubuntu, `python3 -m venv` also needs the venv package:

```bash
sudo apt install python3-venv python3-pip
```

Paste this into a terminal. It clones the repo if `~/FU/opentoolbook8` is not already a checkout, stays on `main`, makes a virtualenv, installs, and prints the command list.

```bash
mkdir -p ~/FU
cd ~/FU
if [ ! -d opentoolbook8/.git ]; then
  git clone https://github.com/squirelworks/opentoolbook8.git
fi
cd opentoolbook8
git fetch origin
git checkout -B main origin/main
git pull --ff-only origin main
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
python3 -m opentoolbook --catalog path/to/courses.xml
python3 -m opentoolbook --cailt path/to/CAILT.DAT 9E954D01
python3 -m opentoolbook --home path/to/TBK path/to/book.tbk
python3 -m opentoolbook --keydisk path/to/rating
python3 -m unittest discover -s tests
```

The tests use synthetic books and a synthetic menu. `OPENTOOLBOOK_TBK` points the extra tests at a lesson book.

```bash
OPENTOOLBOOK_TBK=path/to/book.tbk python3 -m unittest discover -s tests
```

Later, from the same folder, with the virtualenv activated:

```bash
git pull --ff-only origin main
python3 -m pip install -e .
```

### Windows

In PowerShell, check Git and Python:

```powershell
git --version
py -3 --version
```

`py -3 --version` needs to say 3.11 or newer. Then paste this. It clones into `%USERPROFILE%\FU\opentoolbook8`.

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\FU" | Out-Null
Set-Location "$env:USERPROFILE\FU"
if (-not (Test-Path opentoolbook8\.git)) {
  git clone https://github.com/squirelworks/opentoolbook8.git
}
Set-Location opentoolbook8
git fetch origin
git checkout -B main origin/main
git pull --ff-only origin main
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
python -m opentoolbook --catalog path\to\courses.xml
python -m opentoolbook --cailt path\to\CAILT.DAT 9E954D01
python -m opentoolbook --home path\to\TBK path\to\book.tbk
python -m opentoolbook --keydisk path\to\rating
python -m unittest discover -s tests
```
