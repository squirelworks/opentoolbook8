# Instructor 8.1 Common Files and Program Files

Measured 24 October 2026 from the ToolBook II Instructor 8.1 author install in the Wine prefix `/tmp/tb81/wine`. The directories were read and left unchanged. No file from the install is in this repository.

The author product is on disk as two trees.

Common Files, the runtime and shared files:

`/tmp/tb81/wine/drive_c/Program Files/Common Files/click2learn`

Program Files, the author programs:

`/tmp/tb81/wine/drive_c/Program Files/click2learn`

`/tmp/tb81` contains one `Common Files` directory and one `Program Files/click2learn` directory. A name search under `/tmp`, `/home`, `/opt`, and `/workspace` found a single `Inst80.exe`, in the Program Files tree. The same search found `TB80.EXE`, `TB80BAS.DLL`, `TB80RTM.EXE`, `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk` in Common Files `TBSystem`. The three `.sbk` names also occur as 29147-byte files under `/tmp/tb115-tbsystem/zip1`. `TB80BAS.DLL` also occurs at `/tmp/refs/guest/TB80BAS.DLL` (683872 bytes). `/tmp/nida-home/TB80ANM.SBK` is 1 byte.

## The two trees

`Common Files/click2learn` holds five directories and 130 files.

| Directory | Files |
|---|---:|
| `TBSystem` | 70 |
| `Editors` | 23 |
| `Filters` | 27 |
| `Neuron` | 9 |
| `Spelling` | 1 |

`TBSystem` is the shared runtime folder for this install. Dedmore's account of one `TBSYSTEM` folder for the runtime files from ToolBook 8 upward is in `DENNY-RUNTIME.md`. His usual path is `Common Files\ToolBook\TBSystem`. On this machine the folder is `Common Files\click2learn\TBSystem`.

`Instructor8` is the only directory in `Program Files/click2learn`. That tree is 349 files. `Inst80.exe` is the Instructor program.

The parent directory `/tmp/tb81/wine/drive_c/Program Files/Common Files` also contains `Microsoft Shared` and `System`. Those are the Wine prefix's Windows common files. `Microsoft Shared/TextConv` is empty. `System` holds `ADO/msado15.dll`, `OLE DB/msdaps.dll`, `OLE DB/oledb32.dll`, and `OLE DB/msdasql.dll`. They are outside the click2learn product, and they are omitted from the lists below.

## How the earlier list combined the trees

`RESEARCH.md` gives each directory its own table, then one author basename list of 472 names drawn from 479 files. That list is the two trees together. Common Files contributes 130 files and 125 basenames. Program Files contributes 349 files and 348 basenames. The basename `relnotes.wri` occurs in both trees, so the union has 472 basenames. The NIDA name partition in `RESEARCH.md` uses that union as its author side. `tests/fixtures/install-names.txt` is the same combined list.

This note keeps the trees apart. `tests/fixtures/instructor-layout-names.txt` holds the two basename lists, and `install_partition` is the split.

## Where the named files sit

| File | Tree | Path | Bytes | Mark |
|---|---|---|---:|---|
| `tb80anm.sbk` | Common Files | `TBSystem/tb80anm.sbk` | 64023 | |
| `tb80hyp.sbk` | Common Files | `TBSystem/tb80hyp.sbk` | 140613 | |
| `tb80r.sbk` | Common Files | `TBSystem/tb80r.sbk` | 953705 | |
| `TB80.EXE` | Common Files | `TBSystem/TB80.EXE` | 66048 | PE |
| `TB80BAS.DLL` | Common Files | `TBSystem/TB80BAS.DLL` | 683872 | NE |
| `TB80RTM.EXE` | Common Files | `TBSystem/TB80RTM.EXE` | 462080 | NE |
| `Inst80.exe` | Program Files | `Instructor8/Inst80.exe` | 441344 | PE |

Each TB80 name in that table occurs once in the Instructor install, under Common Files `TBSystem`. `Inst80.exe` occurs once, under Program Files `Instructor8`.

`TB115-SYSTEM.md` lists archive copies of `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk` at 29147 bytes. The files under `/tmp/tb115-tbsystem/zip1` with those names are 29147 bytes. The Instructor originals are the three `TBSystem` rows above.

## Basename split

Comparison ignores case. A basename that occurs twice inside one tree counts once.

The 70 `TBSystem` basenames and the 348 Program Files basenames have an empty intersection. `TB80.EXE`, `TB80BAS.DLL`, `TB80RTM.EXE`, `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk` are on the Common Files side. `Inst80.exe` is on the Program Files side.

The full Common Files tree (125 basenames) against Program Files (348 basenames):

| Side | Basenames |
|---|---:|
| Common Files only | 124 |
| Program Files only | 347 |
| In both | 1 |

The shared basename is `relnotes.wri`. `Neuron/relnotes.wri` is 2322 bytes. `Instructor8/Welcome/RelNotes.WRI` is 28633 bytes. The two files have different bytes.

Five basenames occur twice inside Common Files. Each pair is the same bytes.

| Name | Paths | Bytes |
|---|---|---:|
| `DIB.DRV` | `Editors/DIB.DRV`, `TBSystem/DIB.DRV` | 30544 |
| `PALOPTX.DLL` | `Editors/PALOPTX.DLL`, `TBSystem/PALOPTX.DLL` | 48661 |
| `TB80RCA.DLL` | `Editors/tb80RCA.DLL`, `TBSystem/TB80RCA.DLL` | 169760 |
| `TB80RCR.DLL` | `Editors/tb80RCR.DLL`, `TBSystem/TB80RCR.DLL` | 67824 |
| `VEAMAA51.LEX` | `Spelling/VEAMAA51.LEX`, `TBSystem/VEAMAA51.LEX` | 204562 |

`tbkcache.ini` occurs twice inside `Instructor8`, at different sizes. `Instructor8/spclst/styles/tbkcache.ini` is 6281 bytes. `Instructor8/template/tbkcache.ini` is 6704 bytes.

The Common Files basename list keeps the first spelling in case-insensitive path order. `Editors` sorts ahead of `TBSystem`, so the shared DLL spellings in the fixture are `tb80RCA.DLL` and `tb80RCR.DLL`.

## Common Files against the TB115 zip names

The TB115 inventory is the 182 basenames in `tests/fixtures/tb115-tbsystem-names.txt`, also listed in `TB115-SYSTEM.md`. Those names are the three ToolBook 11.5 common-file archives. `install_partition` of the 70 Instructor `TBSystem` basenames against that list is the split in `TB115-SYSTEM.md` and `tests/test_tb115_names.py`: 18 names in both, 52 names only in the Instructor `TBSystem` directory, 164 names only in the archives.

The 18 shared basenames, in the Instructor spelling, are `Asymgif.ocx`, `dzactx.dll`, `ISGDI32.DLL`, `ISGDI32.INI`, `PALOPTX.DLL`, `tb80actr.sbk`, `tb80aicc.sbk`, `tb80anm.sbk`, `tb80ftp.sbk`, `tb80hyp.sbk`, `tb80r.sbk`, `TBCOM.DLL`, `TBINET32.DLL`, `TBKSLICE.DLL`, `Tbload.exe`, `TBUTIL32.dll`, `TList4.ocx`, and `WINSOX.EXE`.

`TB80.EXE`, `TB80BAS.DLL`, and `TB80RTM.EXE` are among the 52 names that the Instructor `TBSystem` directory has and the TB115 name list lacks.

The overlap of the whole Common Files tree with the TB115 inventory is those same 18 names. Each of them is a `TBSystem` basename.

`TBSystem` is the TB80-era counterpart of those common-file archives. It is one directory under Common Files, it holds the TB80 runtime files, 18 of its basenames are on the TB115 inventory, and the TB80 engine names `TB80.EXE`, `TB80BAS.DLL`, and `TB80RTM.EXE` are on the Instructor side of that comparison.

## How a mark was read

A name ending in `.exe`, `.dll`, `.ocx`, `.drv`, or `.flt` is marked from its first bytes. The DOS header is read, then the signature at the `e_lfanew` offset. `NE` is the 16-bit signature. `PE` is the 32-bit signature. Any other first bytes would be recorded as neither. Every file with one of those endings in these two trees is NE or PE. A name with any other ending has a blank mark. No further bytes were decoded.

## Common Files

Paths are relative to `Program Files/Common Files/click2learn`.

### `TBSystem`

70 files.

| Bytes | Path | Mark |
|---:|---|---|
| 1638 | `TBSystem/asym.ini` |  |
| 29696 | `TBSystem/Asymgif.ocx` | PE |
| 30544 | `TBSystem/DIB.DRV` | NE |
| 48661 | `TBSystem/DIBUTIL.DLL` | NE |
| 253952 | `TBSystem/dzactx.dll` | PE |
| 802816 | `TBSystem/ISGDI32.DLL` | PE |
| 4338 | `TBSystem/ISGDI32.INI` |  |
| 119296 | `TBSystem/Oxs.dll` | PE |
| 48661 | `TBSystem/PALOPTX.DLL` | NE |
| 83520 | `TBSystem/PCDLIB.DLL` | NE |
| 2336 | `TBSystem/PCDXBMP.DLL` | NE |
| 33088 | `TBSystem/PHOTO.DLL` | NE |
| 236734 | `TBSystem/PXENGWIN.DLL` | NE |
| 67984 | `TBSystem/TB2FTP.DLL` | NE |
| 66048 | `TBSystem/TB80.EXE` | PE |
| 1669 | `TBSystem/tb80.ini` |  |
| 207989 | `TBSystem/tb80actr.sbk` |  |
| 247296 | `TBSystem/TB80ACX.DLL` | PE |
| 85719 | `TBSystem/tb80aicc.sbk` |  |
| 64023 | `TBSystem/tb80anm.sbk` |  |
| 705824 | `TBSystem/TB80ATH.EXE` | NE |
| 683872 | `TBSystem/TB80BAS.DLL` | NE |
| 68640 | `TBSystem/TB80BMP.DLL` | NE |
| 193216 | `TBSystem/TB80CMP.DLL` | NE |
| 27552 | `TBSystem/TB80CVT.DLL` | NE |
| 106432 | `TBSystem/TB80EDT.DLL` | NE |
| 219872 | `TBSystem/TB80ENU1.DLL` | NE |
| 79360 | `TBSystem/TB80ENU2.DLL` | PE |
| 551968 | `TBSystem/TB80ENU3.DLL` | NE |
| 397824 | `TBSystem/TB80ENU4.DLL` | PE |
| 78848 | `TBSystem/TB80F32L.dll` | PE |
| 101152 | `TBSystem/TB80FLT.DLL` | NE |
| 242983 | `TBSystem/tb80ftp.sbk` |  |
| 140613 | `TBSystem/tb80hyp.sbk` |  |
| 63872 | `TBSystem/TB80JPG.DLL` | NE |
| 97792 | `TBSystem/TB80LNL.DLL` | NE |
| 23552 | `TBSystem/TB80MAIN.EXE` | PE |
| 24800 | `TBSystem/TB80MM.DLL` | NE |
| 3352 | `TBSystem/TB80MM.INI` |  |
| 67360 | `TBSystem/TB80NET.EXE` | NE |
| 206528 | `TBSystem/TB80OCX.DLL` | NE |
| 85952 | `TBSystem/TB80OLE.DLL` | NE |
| 953705 | `TBSystem/tb80r.sbk` |  |
| 169760 | `TBSystem/TB80RCA.DLL` | NE |
| 67824 | `TBSystem/TB80RCR.DLL` | NE |
| 109056 | `TBSystem/TB80RMT.DLL` | PE |
| 462080 | `TBSystem/TB80RTM.EXE` | NE |
| 65536 | `TBSystem/TB80RUN.EXE` | PE |
| 64128 | `TBSystem/TB80UTL.DLL` | NE |
| 75328 | `TBSystem/TB80VBX.DLL` | NE |
| 76512 | `TBSystem/TB80W16.DLL` | NE |
| 83456 | `TBSystem/TB80W32.DLL` | PE |
| 41783 | `TBSystem/TB80XTR.DLL` | NE |
| 31616 | `TBSystem/TBCBT.DLL` | NE |
| 53248 | `TBSystem/TBCOM.DLL` | PE |
| 66560 | `TBSystem/TBDB3.DLL` | NE |
| 36800 | `TBSystem/TBDLG.DLL` | NE |
| 15616 | `TBSystem/TBDOS.DLL` | NE |
| 21952 | `TBSystem/TBFILE32.DLL` | NE |
| 532480 | `TBSystem/TBINET32.DLL` | PE |
| 57344 | `TBSystem/TBKSLICE.DLL` | PE |
| 87040 | `TBSystem/Tbload.exe` | PE |
| 30880 | `TBSystem/TBPDX.DLL` | NE |
| 19552 | `TBSystem/TBREG.DLL` | NE |
| 40960 | `TBSystem/TBUTIL32.dll` | PE |
| 40608 | `TBSystem/TBWIN.DLL` | NE |
| 267264 | `TBSystem/Tlist16p.ocx` | NE |
| 460744 | `TBSystem/TList4.ocx` | PE |
| 204562 | `TBSystem/VEAMAA51.LEX` |  |
| 86496 | `TBSystem/WINSOX.EXE` | NE |

### `Editors`

23 files.

| Bytes | Path | Mark |
|---:|---|---|
| 154144 | `Editors/BITED80.EXE` | NE |
| 131404 | `Editors/Bited80.hlp` |  |
| 30544 | `Editors/DIB.DRV` | NE |
| 117280 | `Editors/ICONED80.EXE` | NE |
| 67383 | `Editors/Iconed80.hlp` |  |
| 16544 | `Editors/medimpt.m80` |  |
| 43968 | `Editors/MEDMANT.DLL` | NE |
| 73760 | `Editors/medwavet.m80` |  |
| 63840 | `Editors/MENUED80.EXE` | NE |
| 67323 | `Editors/Menued80.hlp` |  |
| 83520 | `Editors/PALED80.EXE` | NE |
| 79127 | `Editors/Paled80.hlp` |  |
| 123296 | `Editors/PALOPT.EXE` | NE |
| 13932 | `Editors/PALOPT.HLP` |  |
| 48661 | `Editors/PALOPTX.DLL` | NE |
| 99440 | `Editors/tb80bit.m80` |  |
| 169760 | `Editors/tb80RCA.DLL` | NE |
| 67824 | `Editors/tb80RCR.DLL` | NE |
| 46560 | `Editors/tb80RED.DLL` | NE |
| 121728 | `Editors/WAVEED80.EXE` | NE |
| 86217 | `Editors/Waveed80.hlp` |  |
| 40288 | `Editors/WINCOMT.DLL` | NE |
| 39200 | `Editors/WRKBNCHT.DLL` | NE |

### `Filters`

27 files.

| Bytes | Path | Mark |
|---:|---|---|
| 83968 | `Filters/IBGIF2.FLT` | PE |
| 103424 | `Filters/IBJPG2.FLT` | PE |
| 202240 | `Filters/IBPCD2.FLT` | PE |
| 760 | `Filters/IBPCD2.INI` |  |
| 80896 | `Filters/IBPCX2.FLT` | PE |
| 79360 | `Filters/IBTGA2.FLT` | PE |
| 105472 | `Filters/IBTIF2.FLT` | PE |
| 158208 | `Filters/IMCD32.FLT` | PE |
| 173056 | `Filters/IMCD42.FLT` | PE |
| 68096 | `Filters/IMCDR2.FLT` | PE |
| 453 | `Filters/IMCDR2.INI` |  |
| 146944 | `Filters/IMDRW2.FLT` | PE |
| 556 | `Filters/IMDRW2.INI` |  |
| 227328 | `Filters/IMDXF2.FLT` | PE |
| 4719 | `Filters/IMDXF2.INI` |  |
| 160768 | `Filters/IMHG32.FLT` | PE |
| 5839 | `Filters/IMHG32.INI` |  |
| 155648 | `Filters/IMPCT2.FLT` | PE |
| 1303 | `Filters/IMPCT2.INI` |  |
| 84992 | `Filters/IMPIC2.FLT` | PE |
| 1183 | `Filters/IMPIC2.INI` |  |
| 120832 | `Filters/IMPIF2.FLT` | PE |
| 1228 | `Filters/IMPIF2.INI` |  |
| 155648 | `Filters/IMPS_2.FLT` | PE |
| 6321 | `Filters/IMPS_2.INI` |  |
| 229888 | `Filters/IPHGW2.FLT` | PE |
| 247 | `Filters/IPHGW2.INI` |  |

### `Neuron`

9 files.

| Bytes | Path | Mark |
|---:|---|---|
| 141 | `Neuron/CONFIRM.REG` |  |
| 1391 | `Neuron/NEURON.CNT` |  |
| 77848 | `Neuron/NEURON.HLP` |  |
| 191488 | `Neuron/NEURON.OCX` | PE |
| 140 | `Neuron/NONSEC.REG` |  |
| 119360 | `Neuron/NP16NEUR.DLL` | NE |
| 296960 | `Neuron/NP32NEUR.DLL` | PE |
| 2322 | `Neuron/relnotes.wri` |  |
| 135 | `Neuron/SECURE.REG` |  |

### `Spelling`

1 file.

| Bytes | Path | Mark |
|---:|---|---|
| 204562 | `Spelling/VEAMAA51.LEX` |  |

## Program Files

Paths are relative to `Program Files/click2learn`. `Instructor8` is the only child of that directory.

### `Instructor8`

35 files.

| Bytes | Path | Mark |
|---:|---|---|
| 421888 | `Instructor8/AUTORUN.EXE` | PE |
| 8798 | `Instructor8/Autorun.ICO` |  |
| 56969 | `Instructor8/axf.dtd` |  |
| 17648 | `Instructor8/blank.tbk` |  |
| 121249 | `Instructor8/decrypt.exe` | NE |
| 24615 | `Instructor8/DECRYPT.HLP` |  |
| 5183 | `Instructor8/distrib.wri` |  |
| 139487 | `Instructor8/impulse.exe` | NE |
| 18419 | `Instructor8/INST80.CNT` |  |
| 441344 | `Instructor8/Inst80.exe` | PE |
| 6354973 | `Instructor8/INST80.HLP` |  |
| 980 | `Instructor8/inst80.ini` |  |
| 1032 | `Instructor8/Inst80.pal` |  |
| 70132 | `Instructor8/INST80.SBK` |  |
| 545071 | `Instructor8/logread.exe` | PE |
| 43362 | `Instructor8/logread.hlp` |  |
| 902550 | `Instructor8/mercury.jar` |  |
| 184830 | `Instructor8/PATHANIM.HLP` |  |
| 95927 | `Instructor8/remover.exe` | PE |
| 766 | `Instructor8/remover.ico` |  |
| 426209 | `Instructor8/Repair80.exe` | PE |
| 766 | `Instructor8/scrwalk.ico` |  |
| 178875 | `Instructor8/scrwalk.tbk` |  |
| 480 | `Instructor8/startup.ini` |  |
| 3086352 | `Instructor8/tb80.sbk` |  |
| 2392403 | `Instructor8/tb80a.sbk` |  |
| 2120361 | `Instructor8/tb80acta.sbk` |  |
| 617740 | `Instructor8/tb80axf.sbk` |  |
| 74386 | `Instructor8/tb80ftp.exe` | PE |
| 100533 | `Instructor8/TB80FTP.HLP` |  |
| 619201 | `Instructor8/tb80i.sbk` |  |
| 62053 | `Instructor8/tb80lmx.sbk` |  |
| 1130973 | `Instructor8/tb80web.sbk` |  |
| 256257 | `Instructor8/tb80x.sbk` |  |
| 342145 | `Instructor8/UnInst80.isu` |  |

### `Instructor8/Catalog`

126 files.

| Bytes | Path | Mark |
|---:|---|---|
| 108155 | `Instructor8/Catalog/abullet.spb` |  |
| 109910 | `Instructor8/Catalog/actdelay.spb` |  |
| 8581 | `Instructor8/Catalog/Action Objects.ini` |  |
| 237707 | `Instructor8/Catalog/Action Objects.wbk` |  |
| 457027 | `Instructor8/Catalog/Action Objects.wbx` |  |
| 153701 | `Instructor8/Catalog/acttimer.spb` |  |
| 288063 | `Instructor8/Catalog/allmedia.spb` |  |
| 136983 | `Instructor8/Catalog/automenu.spb` |  |
| 101816 | `Instructor8/Catalog/bullets.spb` |  |
| 87495 | `Instructor8/Catalog/butnedit.spb` |  |
| 4113 | `Instructor8/Catalog/Buttons.ini` |  |
| 109543 | `Instructor8/Catalog/Buttons.wbk` |  |
| 297239 | `Instructor8/Catalog/Buttons.wbx` |  |
| 104363 | `Instructor8/Catalog/callout.spb` |  |
| 57947 | `Instructor8/Catalog/Catalog Blank Cache.tbk` |  |
| 16259 | `Instructor8/Catalog/Catalog Blank Category.tbk` |  |
| 16259 | `Instructor8/Catalog/Catalog Blank Spec Cache.tbk` |  |
| 441408 | `Instructor8/Catalog/Catalog Spec Cache.tbk` |  |
| 1760 | `Instructor8/Catalog/catalog.ini` |  |
| 24500 | `Instructor8/Catalog/CATOBJT.HLP` |  |
| 6759 | `Instructor8/Catalog/click2learn.author.ini` |  |
| 372565 | `Instructor8/Catalog/click2learn.author.wbk` |  |
| 455813 | `Instructor8/Catalog/click2learn.author.wbx` |  |
| 1048 | `Instructor8/Catalog/click2learn.pal` |  |
| 12196 | `Instructor8/Catalog/CLIPWID.HLP` |  |
| 87355 | `Instructor8/Catalog/clipwid.spb` |  |
| 8206 | `Instructor8/Catalog/Draw Objects.ini` |  |
| 149063 | `Instructor8/Catalog/Draw Objects.wbk` |  |
| 452985 | `Instructor8/Catalog/Draw Objects.wbx` |  |
| 283967 | `Instructor8/Catalog/dropbin.spb` |  |
| 12497 | `Instructor8/Catalog/EVALBOOK.HLP` |  |
| 108138 | `Instructor8/Catalog/evalbook.spb` |  |
| 11733 | `Instructor8/Catalog/EVALPAGE.HLP` |  |
| 116375 | `Instructor8/Catalog/evalpage.spb` |  |
| 62029 | `Instructor8/Catalog/extjava.spb` |  |
| 154884 | `Instructor8/Catalog/fldglist.spb` |  |
| 175266 | `Instructor8/Catalog/fldolist.spb` |  |
| 56859 | `Instructor8/Catalog/genedit.spb` |  |
| 11814 | `Instructor8/Catalog/IMAGEMAP.HLP` |  |
| 170730 | `Instructor8/Catalog/imagemap.spb` |  |
| 11398 | `Instructor8/Catalog/IMGEDIT.HLP` |  |
| 96467 | `Instructor8/Catalog/imgedit.spb` |  |
| 82699 | `Instructor8/Catalog/inetauto.spb` |  |
| 80368 | `Instructor8/Catalog/liblogin.spb` |  |
| 107076 | `Instructor8/Catalog/listedit.spb` |  |
| 120468 | `Instructor8/Catalog/marquee.spb` |  |
| 1721 | `Instructor8/Catalog/Media (Animated).ini` |  |
| 190404 | `Instructor8/Catalog/Media (Animated).wbk` |  |
| 218557 | `Instructor8/Catalog/Media (Animated).wbx` |  |
| 16259 | `Instructor8/Catalog/Media (Backdrops).ini` |  |
| 18613209 | `Instructor8/Catalog/Media (Backdrops).wbk` |  |
| 1063909 | `Instructor8/Catalog/Media (Backdrops).wbx` |  |
| 45418 | `Instructor8/Catalog/Media (Clipart).ini` |  |
| 5188295 | `Instructor8/Catalog/Media (Clipart).wbk` |  |
| 3826933 | `Instructor8/Catalog/Media (Clipart).wbx` |  |
| 35164 | `Instructor8/Catalog/Media (Icons).ini` |  |
| 357795 | `Instructor8/Catalog/Media (Icons).wbk` |  |
| 3476871 | `Instructor8/Catalog/Media (Icons).wbx` |  |
| 13288 | `Instructor8/Catalog/Media (Tiled Backdrops).ini` |  |
| 1930465 | `Instructor8/Catalog/Media (Tiled Backdrops).wbk` |  |
| 1044433 | `Instructor8/Catalog/Media (Tiled Backdrops).wbx` |  |
| 16596 | `Instructor8/Catalog/Media Players.ini` |  |
| 658231 | `Instructor8/Catalog/Media Players.wbk` |  |
| 941911 | `Instructor8/Catalog/Media Players.wbx` |  |
| 50275 | `Instructor8/Catalog/mediabtn.spb` |  |
| 268283 | `Instructor8/Catalog/mtchitem.spb` |  |
| 271729 | `Instructor8/Catalog/mtchobj.spb` |  |
| 293037 | `Instructor8/Catalog/multdrop.spb` |  |
| 278057 | `Instructor8/Catalog/multiobj.spb` |  |
| 272641 | `Instructor8/Catalog/multline.spb` |  |
| 288093 | `Instructor8/Catalog/multwid.spb` |  |
| 136 | `Instructor8/Catalog/My Objects.ini` |  |
| 19016 | `Instructor8/Catalog/My Objects.wbk` |  |
| 84849 | `Instructor8/Catalog/My Objects.wbx` |  |
| 272519 | `Instructor8/Catalog/namepart.spb` |  |
| 32862 | `Instructor8/Catalog/Navigation Objects.ini` |  |
| 2777159 | `Instructor8/Catalog/Navigation Objects.wbk` |  |
| 1500039 | `Instructor8/Catalog/Navigation Objects.wbx` |  |
| 149770 | `Instructor8/Catalog/neuron.spb` |  |
| 280045 | `Instructor8/Catalog/orderobj.spb` |  |
| 242801 | `Instructor8/Catalog/orderwid.spb` |  |
| 115230 | `Instructor8/Catalog/pagemenu.spb` |  |
| 3511 | `Instructor8/Catalog/Pages.ini` |  |
| 14289261 | `Instructor8/Catalog/Pages.wbk` |  |
| 776449 | `Instructor8/Catalog/Pages.wbx` |  |
| 6737 | `Instructor8/Catalog/Placeholder Objects.ini` |  |
| 179077 | `Instructor8/Catalog/Placeholder Objects.wbk` |  |
| 368015 | `Instructor8/Catalog/Placeholder Objects.wbx` |  |
| 347473 | `Instructor8/Catalog/popupump.spb` |  |
| 11565 | `Instructor8/Catalog/POPVID.HLP` |  |
| 235308 | `Instructor8/Catalog/popvid.spb` |  |
| 84081 | `Instructor8/Catalog/questext.spb` |  |
| 63165 | `Instructor8/Catalog/QUESTION.HLP` |  |
| 42103 | `Instructor8/Catalog/Questions (Multiple Choice).ini` |  |
| 1295499 | `Instructor8/Catalog/Questions (Multiple Choice).wbk` |  |
| 1702455 | `Instructor8/Catalog/Questions (Multiple Choice).wbx` |  |
| 26094 | `Instructor8/Catalog/Questions (True-False).ini` |  |
| 869947 | `Instructor8/Catalog/Questions (True-False).wbk` |  |
| 1428887 | `Instructor8/Catalog/Questions (True-False).wbx` |  |
| 14278 | `Instructor8/Catalog/Questions (Various).ini` |  |
| 540745 | `Instructor8/Catalog/Questions (Various).wbk` |  |
| 731987 | `Instructor8/Catalog/Questions (Various).wbx` |  |
| 182935 | `Instructor8/Catalog/realplay.spb` |  |
| 115419 | `Instructor8/Catalog/reset.spb` |  |
| 119229 | `Instructor8/Catalog/rptactn.spb` |  |
| 7865 | `Instructor8/Catalog/Scoring and Tracking.ini` |  |
| 192399 | `Instructor8/Catalog/Scoring and Tracking.wbk` |  |
| 509499 | `Instructor8/Catalog/Scoring and Tracking.wbx` |  |
| 282861 | `Instructor8/Catalog/seltext.spb` |  |
| 289965 | `Instructor8/Catalog/slider.spb` |  |
| 7477 | `Instructor8/Catalog/Text Fields.ini` |  |
| 281853 | `Instructor8/Catalog/Text Fields.wbk` |  |
| 690829 | `Instructor8/Catalog/Text Fields.wbx` |  |
| 59215 | `Instructor8/Catalog/textedit.spb` |  |
| 11301 | `Instructor8/Catalog/TIMER.HLP` |  |
| 130461 | `Instructor8/Catalog/timer.spb` |  |
| 15984 | `Instructor8/Catalog/TRIGGER.HLP` |  |
| 105809 | `Instructor8/Catalog/trigger.spb` |  |
| 254039 | `Instructor8/Catalog/truefals.spb` |  |
| 294983 | `Instructor8/Catalog/typein.spb` |  |
| 94720 | `Instructor8/Catalog/usejava.spb` |  |
| 302262 | `Instructor8/Catalog/vidsynch.spb` |  |
| 11801 | `Instructor8/Catalog/VIDWID.HLP` |  |
| 200140 | `Instructor8/Catalog/vidwid.spb` |  |
| 136309 | `Instructor8/Catalog/winmedia.spb` |  |
| 175204 | `Instructor8/Catalog/xmedit.spb` |  |

### `Instructor8/Media/cbt/female`

22 files.

| Bytes | Path | Mark |
|---:|---|---|
| 68734 | `Instructor8/Media/cbt/female/Almost.wav` |  |
| 77022 | `Instructor8/Media/cbt/female/Correct.wav` |  |
| 42364 | `Instructor8/Media/cbt/female/Excuseme.wav` |  |
| 44028 | `Instructor8/Media/cbt/female/Givebrk.wav` |  |
| 32636 | `Instructor8/Media/cbt/female/Groovy.wav` |  |
| 179582 | `Instructor8/Media/cbt/female/Incrrct.wav` |  |
| 30268 | `Instructor8/Media/cbt/female/No.wav` |  |
| 37948 | `Instructor8/Media/cbt/female/Nokiddng.wav` |  |
| 23228 | `Instructor8/Media/cbt/female/Ouch.wav` |  |
| 32492 | `Instructor8/Media/cbt/female/Partlyrt.wav` |  |
| 43132 | `Instructor8/Media/cbt/female/Righton.wav` |  |
| 57086 | `Instructor8/Media/cbt/female/Rusure.wav` |  |
| 39804 | `Instructor8/Media/cbt/female/Tryagain.wav` |  |
| 71806 | `Instructor8/Media/cbt/female/Trythis.wav` |  |
| 36860 | `Instructor8/Media/cbt/female/Urright.wav` |  |
| 43132 | `Instructor8/Media/cbt/female/Waycool.wav` |  |
| 26044 | `Instructor8/Media/cbt/female/Woops.wav` |  |
| 71934 | `Instructor8/Media/cbt/female/Wow.wav` |  |
| 75902 | `Instructor8/Media/cbt/female/Wrngagn.wav` |  |
| 31868 | `Instructor8/Media/cbt/female/Yes.wav` |  |
| 31804 | `Instructor8/Media/cbt/female/Yougotit.wav` |  |
| 13788 | `Instructor8/Media/cbt/female/Yup.wav` |  |

### `Instructor8/Media/cbt/male`

22 files.

| Bytes | Path | Mark |
|---:|---|---|
| 42364 | `Instructor8/Media/cbt/male/Almost1.wav` |  |
| 31228 | `Instructor8/Media/cbt/male/Correct1.wav` |  |
| 41340 | `Instructor8/Media/cbt/male/Excuse1.wav` |  |
| 57724 | `Instructor8/Media/cbt/male/Givebrk1.wav` |  |
| 41724 | `Instructor8/Media/cbt/male/Groovy1.wav` |  |
| 29244 | `Instructor8/Media/cbt/male/No1.wav` |  |
| 48252 | `Instructor8/Media/cbt/male/Nokid1.wav` |  |
| 80808 | `Instructor8/Media/cbt/male/Notcrct1.wav` |  |
| 35260 | `Instructor8/Media/cbt/male/Ouch1.wav` |  |
| 29500 | `Instructor8/Media/cbt/male/Partly1.wav` |  |
| 48252 | `Instructor8/Media/cbt/male/Righton1.wav` |  |
| 34364 | `Instructor8/Media/cbt/male/Rusure1.wav` |  |
| 37500 | `Instructor8/Media/cbt/male/Tryagai1.wav` |  |
| 34236 | `Instructor8/Media/cbt/male/Trythis1.wav` |  |
| 33704 | `Instructor8/Media/cbt/male/Urright1.wav` |  |
| 41724 | `Instructor8/Media/cbt/male/Waycoo1l.wav` |  |
| 27004 | `Instructor8/Media/cbt/male/Woops1.wav` |  |
| 23292 | `Instructor8/Media/cbt/male/Wow1.wav` |  |
| 38140 | `Instructor8/Media/cbt/male/Wrngag1.wav` |  |
| 23228 | `Instructor8/Media/cbt/male/Yes1.wav` |  |
| 27004 | `Instructor8/Media/cbt/male/Yougot1.wav` |  |
| 11292 | `Instructor8/Media/cbt/male/Yup1.wav` |  |

### `Instructor8/Media/Flash`

2 files.

| Bytes | Path | Mark |
|---:|---|---|
| 5473 | `Instructor8/Media/Flash/CORRECT.SWF` |  |
| 2770 | `Instructor8/Media/Flash/incorrect.swf` |  |

### `Instructor8/Packager`

12 files.

| Bytes | Path | Mark |
|---:|---|---|
| 322026 | `Instructor8/Packager/_INST32I.EX_` |  |
| 8192 | `Instructor8/Packager/_ISDEL.EXE` | NE |
| 6128 | `Instructor8/Packager/_SETUP.DLL` | NE |
| 195925 | `Instructor8/Packager/_SETUP.LIB` |  |
| 72794 | `Instructor8/Packager/COMPRESS.INS` |  |
| 902744 | `Instructor8/Packager/PACKAGER.exe` | PE |
| 87552 | `Instructor8/Packager/PACKLIST.EXE` | PE |
| 995 | `Instructor8/Packager/PACKLIST.PIF` |  |
| 7216 | `Instructor8/Packager/Regsvr.exe` | NE |
| 45568 | `Instructor8/Packager/SETUP.EXE` | NE |
| 122452 | `Instructor8/Packager/SETUP.INS` |  |
| 40448 | `Instructor8/Packager/Tbisx32.dll` | PE |

### `Instructor8/Packager/ole2`

12 files.

| Bytes | Path | Mark |
|---:|---|---|
| 109056 | `Instructor8/Packager/ole2/COMPOBJ.DLL` | NE |
| 536048 | `Instructor8/Packager/ole2/OC25.DLL` | NE |
| 304640 | `Instructor8/Packager/ole2/OLE2.DLL` | NE |
| 28113 | `Instructor8/Packager/ole2/OLE2.REG` |  |
| 57328 | `Instructor8/Packager/ole2/OLE2CONV.DLL` | NE |
| 164960 | `Instructor8/Packager/ole2/OLE2DISP.DLL` | NE |
| 152976 | `Instructor8/Packager/ole2/OLE2NLS.DLL` | NE |
| 51712 | `Instructor8/Packager/ole2/OLE2PROX.DLL` | NE |
| 12976 | `Instructor8/Packager/ole2/SCP.DLL` | NE |
| 5472 | `Instructor8/Packager/ole2/STDOLE.TLB` |  |
| 157696 | `Instructor8/Packager/ole2/STORAGE.DLL` | NE |
| 177824 | `Instructor8/Packager/ole2/TYPELIB.DLL` | NE |

### `Instructor8/spclst`

3 files.

| Bytes | Path | Mark |
|---:|---|---|
| 737031 | `Instructor8/spclst/spclst.spb` |  |
| 824415 | `Instructor8/spclst/spclstld.spb` |  |
| 677836 | `Instructor8/spclst/spclstqs.spb` |  |

### `Instructor8/spclst/OUTLINES`

9 files.

| Bytes | Path | Mark |
|---:|---|---|
| 213 | `Instructor8/spclst/OUTLINES/catalog.aof` |  |
| 246 | `Instructor8/spclst/OUTLINES/generic1.aof` |  |
| 283 | `Instructor8/spclst/OUTLINES/generic2.aof` |  |
| 307 | `Instructor8/spclst/OUTLINES/generic3.aof` |  |
| 228 | `Instructor8/spclst/OUTLINES/present.aof` |  |
| 278 | `Instructor8/spclst/OUTLINES/quiz1.aof` |  |
| 275 | `Instructor8/spclst/OUTLINES/quiz2.aof` |  |
| 329 | `Instructor8/spclst/OUTLINES/skill1.aof` |  |
| 371 | `Instructor8/spclst/OUTLINES/train1.aof` |  |

### `Instructor8/spclst/styles`

72 files.

| Bytes | Path | Mark |
|---:|---|---|
| 1081229 | `Instructor8/spclst/styles/angled.ptp` |  |
| 1082937 | `Instructor8/spclst/styles/angledh.ptp` |  |
| 725193 | `Instructor8/spclst/styles/art_deco.ptp` |  |
| 512741 | `Instructor8/spclst/styles/bluebr1i.ptp` |  |
| 1056937 | `Instructor8/spclst/styles/blueintersection.ptp` |  |
| 1057947 | `Instructor8/spclst/styles/blueintersectionh.ptp` |  |
| 1110513 | `Instructor8/spclst/styles/bluelines.ptp` |  |
| 1097085 | `Instructor8/spclst/styles/bluelinesh.ptp` |  |
| 1062329 | `Instructor8/spclst/styles/coralsea.ptp` |  |
| 1062359 | `Instructor8/spclst/styles/coralseah.ptp` |  |
| 1064957 | `Instructor8/spclst/styles/earth.ptp` |  |
| 1064651 | `Instructor8/spclst/styles/earthh.ptp` |  |
| 1016511 | `Instructor8/spclst/styles/fall1i.ptp` |  |
| 890481 | `Instructor8/spclst/styles/finan1.ptp` |  |
| 791167 | `Instructor8/spclst/styles/finan1h.ptp` |  |
| 487039 | `Instructor8/spclst/styles/finan1i.ptp` |  |
| 746583 | `Instructor8/spclst/styles/granite.ptp` |  |
| 909063 | `Instructor8/spclst/styles/gray1.ptp` |  |
| 911183 | `Instructor8/spclst/styles/gray1h.ptp` |  |
| 538173 | `Instructor8/spclst/styles/gray1i.ptp` |  |
| 617233 | `Instructor8/spclst/styles/grayck1i.ptp` |  |
| 914809 | `Instructor8/spclst/styles/indust1.ptp` |  |
| 817577 | `Instructor8/spclst/styles/indust1h.ptp` |  |
| 575719 | `Instructor8/spclst/styles/indust1i.ptp` |  |
| 1543741 | `Instructor8/spclst/styles/inter1i.ptp` |  |
| 929965 | `Instructor8/spclst/styles/mil1.ptp` |  |
| 931067 | `Instructor8/spclst/styles/mil1h.ptp` |  |
| 509171 | `Instructor8/spclst/styles/mil1i.ptp` |  |
| 860125 | `Instructor8/spclst/styles/mod_offc.ptp` |  |
| 715595 | `Instructor8/spclst/styles/paint.ptp` |  |
| 1067185 | `Instructor8/spclst/styles/peacock.ptp` |  |
| 1067267 | `Instructor8/spclst/styles/peacockh.ptp` |  |
| 785391 | `Instructor8/spclst/styles/present.ptp` |  |
| 1074597 | `Instructor8/spclst/styles/rainbow.ptp` |  |
| 1074863 | `Instructor8/spclst/styles/rainbowh.ptp` |  |
| 1063159 | `Instructor8/spclst/styles/sky.ptp` |  |
| 1063159 | `Instructor8/spclst/styles/skyh.ptp` |  |
| 1072665 | `Instructor8/spclst/styles/space.ptp` |  |
| 1072905 | `Instructor8/spclst/styles/spaceh.ptp` |  |
| 856267 | `Instructor8/spclst/styles/stageb1.ptp` |  |
| 765425 | `Instructor8/spclst/styles/stageb1h.ptp` |  |
| 472213 | `Instructor8/spclst/styles/stageb1i.ptp` |  |
| 855969 | `Instructor8/spclst/styles/stager1.ptp` |  |
| 765943 | `Instructor8/spclst/styles/stager1h.ptp` |  |
| 474719 | `Instructor8/spclst/styles/stager1i.ptp` |  |
| 1065529 | `Instructor8/spclst/styles/strongline.ptp` |  |
| 1065611 | `Instructor8/spclst/styles/stronglineh.ptp` |  |
| 6281 | `Instructor8/spclst/styles/tbkcache.ini` |  |
| 909151 | `Instructor8/spclst/styles/tech1.ptp` |  |
| 799533 | `Instructor8/spclst/styles/tech1h.ptp` |  |
| 521769 | `Instructor8/spclst/styles/tech1i.ptp` |  |
| 918137 | `Instructor8/spclst/styles/tech2.ptp` |  |
| 790505 | `Instructor8/spclst/styles/tech2h.ptp` |  |
| 499089 | `Instructor8/spclst/styles/tech2i.ptp` |  |
| 2487623 | `Instructor8/spclst/styles/tech3.ptp` |  |
| 2322703 | `Instructor8/spclst/styles/tech3h.ptp` |  |
| 492071 | `Instructor8/spclst/styles/tech3i.ptp` |  |
| 1221271 | `Instructor8/spclst/styles/tech_4h.ptp` |  |
| 1229531 | `Instructor8/spclst/styles/tech_b4h.ptp` |  |
| 1235323 | `Instructor8/spclst/styles/tech_g4h.ptp` |  |
| 1081923 | `Instructor8/spclst/styles/tornedge.ptp` |  |
| 1081595 | `Instructor8/spclst/styles/tornedgeh.ptp` |  |
| 614057 | `Instructor8/spclst/styles/triang1i.ptp` |  |
| 904893 | `Instructor8/spclst/styles/usgov1.ptp` |  |
| 909751 | `Instructor8/spclst/styles/usgov1h.ptp` |  |
| 587763 | `Instructor8/spclst/styles/usgov1i.ptp` |  |
| 951983 | `Instructor8/spclst/styles/usgov2.ptp` |  |
| 877581 | `Instructor8/spclst/styles/usgov2h.ptp` |  |
| 549133 | `Instructor8/spclst/styles/usgov2i.ptp` |  |
| 922529 | `Instructor8/spclst/styles/usmil1.ptp` |  |
| 927027 | `Instructor8/spclst/styles/usmil1h.ptp` |  |
| 564949 | `Instructor8/spclst/styles/usmil1i.ptp` |  |

### `Instructor8/template`

32 files.

| Bytes | Path | Mark |
|---:|---|---|
| 573554 | `Instructor8/template/catalog.tbk` |  |
| 567736 | `Instructor8/template/catalogh.tbk` |  |
| 91798 | `Instructor8/template/default.tbk` |  |
| 91836 | `Instructor8/template/defaulth.tbk` |  |
| 590470 | `Instructor8/template/gen1ch.tbk` |  |
| 590576 | `Instructor8/template/gen1chh.tbk` |  |
| 603756 | `Instructor8/template/gen2ch.tbk` |  |
| 603864 | `Instructor8/template/gen2chh.tbk` |  |
| 517424 | `Instructor8/template/generic.tbk` |  |
| 517884 | `Instructor8/template/generich.tbk` |  |
| 661570 | `Instructor8/template/hr.tbk` |  |
| 660810 | `Instructor8/template/hrh.tbk` |  |
| 622974 | `Instructor8/template/learn1.tbk` |  |
| 623126 | `Instructor8/template/learn1h.tbk` |  |
| 357136 | `Instructor8/template/learn1i.tbk` |  |
| 228456 | `Instructor8/template/ppointi.tbk` |  |
| 648112 | `Instructor8/template/present.tbk` |  |
| 648172 | `Instructor8/template/presenth.tbk` |  |
| 577620 | `Instructor8/template/quiz1.tbk` |  |
| 575086 | `Instructor8/template/quiz1h.tbk` |  |
| 507610 | `Instructor8/template/quiz1i.tbk` |  |
| 548644 | `Instructor8/template/roi.tbk` |  |
| 548374 | `Instructor8/template/roih.tbk` |  |
| 976814 | `Instructor8/template/sales1.tbk` |  |
| 625684 | `Instructor8/template/sales1h.tbk` |  |
| 859786 | `Instructor8/template/sales2.tbk` |  |
| 860572 | `Instructor8/template/sales2h.tbk` |  |
| 583410 | `Instructor8/template/simquiz.tbk` |  |
| 583510 | `Instructor8/template/simquizh.tbk` |  |
| 6704 | `Instructor8/template/tbkcache.ini` |  |
| 597418 | `Instructor8/template/train1.tbk` |  |
| 596850 | `Instructor8/template/train1h.tbk` |  |

### `Instructor8/Welcome`

2 files.

| Bytes | Path | Mark |
|---:|---|---|
| 28633 | `Instructor8/Welcome/RelNotes.WRI` |  |
| 1359335 | `Instructor8/Welcome/Walkthrough.tbk` |  |
