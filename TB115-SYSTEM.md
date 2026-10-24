# ToolBook 11.5 common files

Measured 24 October 2026 from three zip archives of a ToolBook 11.5 install's common files. The person who sent them described the source as the TB115 install's common files. The archives and the binaries stay out of this repository. This note compares those files with the Instructor 8.1 TBSystem list. The ToolBook 8 reader is unchanged. A behavior that shows up in these files stays labeled TB115, or with the version the file's own name and version resource carry.

Denny Dedmore writes that from ToolBook 8 upward the runtime files share one `TBSYSTEM` folder, usually `Common Files\ToolBook\TBSystem`, and that deleting the whole folder disables every engine from 8 up. The only version prefix he tells you to delete is `TB115`. His examples of a version living in a system-book name are `TB105HYP.SBK` and `TB115HYP.SBK`. That account is in `DENNY-RUNTIME.md`. His pages leave `TB80.EXE` unnamed. The Instructor 8.1 tree measured on this machine names it, along with the rest of that TBSystem directory: `TB80*.DLL`, `TB80.EXE` (PE, 66048 bytes), `TB80BAS.DLL` (NE, 683872 bytes), `TB80RTM.EXE` (NE, 462080 bytes), and the system books `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk`. Those names and sizes are the TBSystem table in `RESEARCH.md` and the files still on disk under `/tmp/tb81/wine/drive_c/Program Files/Common Files/click2learn/TBSystem`. This note reads that directory for sizes and leaves the directory as it was.

## The three archives

Each archive unpacked to a flat directory. The path of a file inside its archive is the file name. The mark is NE or PE when the first two bytes are `MZ` and the dword at offset `0x3C` points at the bytes `NE` or `PE`. Every other file is neither. No instruction bytes were decoded for that mark.

| Archive | Files | NE | PE | neither |
|---|---|---|---|---|
| TBsystem 1 | 89 | 1 | 66 | 22 |
| TBsystem 2 | 53 | 0 | 51 | 2 |
| TBsystem 3 | 40 | 1 | 35 | 4 |
| Total | 182 | 2 | 152 | 28 |

The two NE files are `PALOPTX.DLL` (48661 bytes, TBsystem 1) and `WINSOX.EXE` (86496 bytes, TBsystem 3). Both are byte-for-byte the Instructor 8.1 TBSystem copies of those names. The other 152 files whose DOS header points at `PE` are PE. The 28 files with no `MZ` header are the ini, wave, help, lexicon, and license files named in the lists below.

## Every file

### TBsystem 1

89 files.

| Bytes | File | Mark |
|---:|---|---|
| 2338 | `accent.tlx` |  |
| 29696 | `ASYMGIF.OCX` | PE |
| 21529 | `correct.tlx` |  |
| 29147 | `ctb40c.sbk` | PE |
| 29147 | `ctb40r.sbk` | PE |
| 29147 | `ctb50c.sbk` | PE |
| 29147 | `ctb60c.sbk` | PE |
| 29147 | `ctb70c.sbk` | PE |
| 29147 | `ctb80c.sbk` | PE |
| 29147 | `ctb85c.sbk` | PE |
| 262144 | `duzactx.dll` | PE |
| 253952 | `dzactx.dll` | PE |
| 105892 | `EndStep.wav` |  |
| 3120 | `Instructor115.lic` |  |
| 802816 | `ISGDI32.DLL` | PE |
| 4338 | `ISGDI32.INI` |  |
| 57344 | `Keyboard.wav` |  |
| 159744 | `KEYLIB32.dll` | PE |
| 581120 | `lame.exe` | PE |
| 121024 | `LicenseMgr115.EXE` | PE |
| 68740 | `Menued115.chm` |  |
| 147520 | `MENUED115.exe` | PE |
| 143360 | `MENUED90.exe` | PE |
| 61758 | `Menued90.hlp` |  |
| 34568 | `MouseClick.wav` |  |
| 24576 | `MouseDown.wav` |  |
| 24576 | `MouseUp.wav` |  |
| 48661 | `PALOPTX.DLL` | NE |
| 324 | `SimBlackClasses.ini` |  |
| 286784 | `SimcapAnalyzer.dll` | PE |
| 49197 | `SimRecorder.chm` |  |
| 439 | `SimRecorder.cnt` |  |
| 19653 | `SimRecorder.hlp` |  |
| 225280 | `ssce5532.dll` | PE |
| 7796 | `ssceam.tlx` |  |
| 328218 | `ssceam2.clx` |  |
| 7798 | `sscebr.tlx` |  |
| 330283 | `sscebr2.clx` |  |
| 7798 | `ssceca.tlx` |  |
| 328670 | `ssceca2.clx` |  |
| 29147 | `tb40anm.sbk` | PE |
| 29147 | `tb40hyp.sbk` | PE |
| 29147 | `tb50anm.sbk` | PE |
| 29147 | `tb50hyp.sbk` | PE |
| 29147 | `tb50r.sbk` | PE |
| 29147 | `tb60anm.sbk` | PE |
| 29147 | `tb60ftp.sbk` | PE |
| 29147 | `tb60hyp.sbk` | PE |
| 29147 | `tb60olx.sbk` | PE |
| 29147 | `tb60r.sbk` | PE |
| 29147 | `tb70actr.sbk` | PE |
| 29147 | `tb70anm.sbk` | PE |
| 29147 | `tb70ftp.sbk` | PE |
| 29147 | `tb70hyp.sbk` | PE |
| 29147 | `tb70olx.sbk` | PE |
| 29147 | `tb70r.sbk` | PE |
| 29147 | `tb80actr.sbk` | PE |
| 29147 | `tb80aicc.sbk` | PE |
| 29147 | `tb80anm.sbk` | PE |
| 29147 | `tb80ftp.sbk` | PE |
| 29147 | `tb80hyp.sbk` | PE |
| 29147 | `tb80r.sbk` | PE |
| 29147 | `tb85actr.sbk` | PE |
| 29147 | `tb85aicc.sbk` | PE |
| 29147 | `tb85anm.sbk` | PE |
| 29147 | `tb85ftp.sbk` | PE |
| 29147 | `tb85hyp.sbk` | PE |
| 29147 | `tb85r.sbk` | PE |
| 29147 | `tb89actr.sbk` | PE |
| 29147 | `tb89aicc.sbk` | PE |
| 29147 | `tb89anm.sbk` | PE |
| 29147 | `tb89ftp.sbk` | PE |
| 29147 | `tb89hyp.sbk` | PE |
| 29147 | `tb89r.sbk` | PE |
| 1097 | `tb90.ini` |  |
| 359825 | `tb90actr.sbk` | PE |
| 95975 | `tb90aicc.sbk` | PE |
| 76795 | `tb90anm.sbk` | PE |
| 29147 | `tb90ftp.sbk` | PE |
| 123011 | `tb90hyp.sbk` | PE |
| 29147 | `tb90hyp.sbk.old` | PE |
| 1008173 | `tb90r.sbk` | PE |
| 29147 | `tb90r.sbk.old` | PE |
| 29147 | `tb95actr.sbk` | PE |
| 29147 | `tb95aicc.sbk` | PE |
| 29147 | `tb95anm.sbk` | PE |
| 29147 | `tb95ftp.sbk` | PE |
| 29147 | `tb95hyp.sbk` | PE |
| 29147 | `tb95r.sbk` | PE |

### TBsystem 2

53 files.

| Bytes | File | Mark |
|---:|---|---|
| 29147 | `tb100actr.sbk` | PE |
| 29147 | `tb100aicc.sbk` | PE |
| 29147 | `tb100anm.sbk` | PE |
| 29147 | `tb100ftp.sbk` | PE |
| 29147 | `tb100hyp.sbk` | PE |
| 29147 | `tb100r.sbk` | PE |
| 29147 | `tb105actr.sbk` | PE |
| 29147 | `tb105aicc.sbk` | PE |
| 29147 | `tb105anm.sbk` | PE |
| 29147 | `tb105ftp.sbk` | PE |
| 29147 | `tb105hyp.sbk` | PE |
| 29147 | `tb105r.sbk` | PE |
| 29145 | `tb110actr.sbk` | PE |
| 29145 | `tb110aicc.sbk` | PE |
| 29145 | `tb110anm.sbk` | PE |
| 29145 | `tb110ftp.sbk` | PE |
| 29145 | `tb110hyp.sbk` | PE |
| 29145 | `tb110r.sbk` | PE |
| 1120 | `tb115.ini` |  |
| 363667 | `tb115actr.sbk` | PE |
| 96015 | `tb115aicc.sbk` | PE |
| 76941 | `tb115anm.sbk` | PE |
| 300269 | `tb115ftp.sbk` | PE |
| 123049 | `tb115hyp.sbk` | PE |
| 1251439 | `tb115r.sbk` | PE |
| 929792 | `TB90.EXE` | PE |
| 237568 | `TB90ACX.dll` | PE |
| 2285568 | `TB90ATH.DLL` | PE |
| 1531904 | `TB90BAS.DLL` | PE |
| 139264 | `TB90BMP.DLL` | PE |
| 65536 | `TB90CBT.DLL` | PE |
| 454656 | `TB90CMP.DLL` | PE |
| 49152 | `TB90DLG.DLL` | PE |
| 258048 | `TB90EDT.DLL` | PE |
| 954368 | `TB90ENU1.DLL` | PE |
| 1482752 | `TB90ENU2.DLL` | PE |
| 180224 | `TB90FLT.DLL` | PE |
| 81920 | `TB90JPG.DLL` | PE |
| 188416 | `TB90LNL.DLL` | PE |
| 69632 | `TB90MM.DLL` | PE |
| 94208 | `TB90NET.DLL` | PE |
| 94208 | `TB90OLE.DLL` | PE |
| 315392 | `TB90RCA.DLL` | PE |
| 155648 | `TB90RCR.DLL` | PE |
| 99808 | `TB90REC.exe` | PE |
| 2435 | `TB90REC.INI` |  |
| 196608 | `TB90RECD.dll` | PE |
| 139264 | `TB90RED.dll` | PE |
| 45056 | `TB90REG.DLL` | PE |
| 1716224 | `TB90RTM.DLL` | PE |
| 925696 | `TB90RUN.EXE` | PE |
| 282624 | `TB90UTL.DLL` | PE |
| 77824 | `TB90WIN.DLL` | PE |

### TBsystem 3

40 files.

| Bytes | File | Mark |
|---:|---|---|
| 1097781 | `TB115.EXE` | PE |
| 237622 | `TB115ACX.dll` | PE |
| 2711604 | `TB115ATH.DLL` | PE |
| 1577010 | `TB115BAS.DLL` | PE |
| 139314 | `TB115BMP.DLL` | PE |
| 65589 | `TB115CBT.DLL` | PE |
| 458807 | `TB115CMP.DLL` | PE |
| 49205 | `TB115DLG.DLL` | PE |
| 282679 | `TB115EDT.dll` | PE |
| 1028152 | `TB115ENU1.DLL` | PE |
| 1564728 | `TB115ENU2.DLL` | PE |
| 184373 | `TB115FLT.DLL` | PE |
| 81920 | `TB115JPG.DLL` | PE |
| 188469 | `TB115LNL.DLL` | PE |
| 69683 | `TB115MM.DLL` | PE |
| 94262 | `TB115NET.DLL` | PE |
| 94262 | `TB115OLE.DLL` | PE |
| 348221 | `TB115RCA.DLL` | PE |
| 176189 | `TB115RCR.DLL` | PE |
| 100536 | `TB115REC.exe` | PE |
| 2435 | `TB115REC.INI` |  |
| 196662 | `TB115RECD.dll` | PE |
| 139325 | `TB115RED.dll` | PE |
| 45109 | `TB115REG.DLL` | PE |
| 1720376 | `TB115RTM.DLL` | PE |
| 925750 | `TB115RUN.EXE` | PE |
| 57400 | `TB115UTIL32.dll` | PE |
| 282677 | `TB115UTL.DLL` | PE |
| 81973 | `TB115WIN.DLL` | PE |
| 65536 | `TBCOM.DLL` | PE |
| 475191 | `TBINET32.DLL` | PE |
| 65591 | `TBKSLICE.DLL` | PE |
| 397365 | `tbload.exe` | PE |
| 40960 | `TBUTIL32.dll` | PE |
| 3703 | `tech.tlx` |  |
| 460744 | `TList4.ocx` | PE |
| 2037 | `toolbook.ini` |  |
| 89 | `userdic.tlx` |  |
| 221184 | `winftp32.dll` | PE |
| 86496 | `WINSOX.EXE` | NE |

## Names against the Instructor 8.1 TBSystem directory

The Instructor 8.1 side is those 70 TBSystem basenames. The TB115 side is the 182 basenames above. Comparison ignores case. A shared name keeps the Instructor 8.1 spelling, which is what `install_partition` returns when the TB80 names are the first list. The fixtures `tests/fixtures/tb80-tbsystem-names.txt` and `tests/fixtures/tb115-tbsystem-names.txt` are these two lists.

Eighteen names are in both. Fifty-two Instructor 8.1 TBSystem names are absent here. One hundred sixty-four names are only in these archives.

### In both

TB80 bytes are the Instructor 8.1 file. TB115 bytes and the mark are the copy in these archives. Same bytes means the SHA-256 of the two files matches.

| TB80 name | TB80 bytes | TB115 name | TB115 bytes | TB115 mark | Same bytes |
|---|---:|---|---:|---|---|
| `Asymgif.ocx` | 29696 | `ASYMGIF.OCX` | 29696 | PE | yes |
| `dzactx.dll` | 253952 | `dzactx.dll` | 253952 | PE | yes |
| `ISGDI32.DLL` | 802816 | `ISGDI32.DLL` | 802816 | PE | yes |
| `ISGDI32.INI` | 4338 | `ISGDI32.INI` | 4338 |  | yes |
| `PALOPTX.DLL` | 48661 | `PALOPTX.DLL` | 48661 | NE | yes |
| `tb80actr.sbk` | 207989 | `tb80actr.sbk` | 29147 | PE | no |
| `tb80aicc.sbk` | 85719 | `tb80aicc.sbk` | 29147 | PE | no |
| `tb80anm.sbk` | 64023 | `tb80anm.sbk` | 29147 | PE | no |
| `tb80ftp.sbk` | 242983 | `tb80ftp.sbk` | 29147 | PE | no |
| `tb80hyp.sbk` | 140613 | `tb80hyp.sbk` | 29147 | PE | no |
| `tb80r.sbk` | 953705 | `tb80r.sbk` | 29147 | PE | no |
| `TBCOM.DLL` | 53248 | `TBCOM.DLL` | 65536 | PE | no |
| `TBINET32.DLL` | 532480 | `TBINET32.DLL` | 475191 | PE | no |
| `TBKSLICE.DLL` | 57344 | `TBKSLICE.DLL` | 65591 | PE | no |
| `Tbload.exe` | 87040 | `tbload.exe` | 397365 | PE | no |
| `TBUTIL32.dll` | 40960 | `TBUTIL32.dll` | 40960 | PE | yes |
| `TList4.ocx` | 460744 | `TList4.ocx` | 460744 | PE | yes |
| `WINSOX.EXE` | 86496 | `WINSOX.EXE` | 86496 | NE | yes |

`Asymgif.ocx` is `ASYMGIF.OCX` in TBsystem 1. `Tbload.exe` is `tbload.exe` in TBsystem 3. The other sixteen shared names use the same spelling on both sides.

Eight of the eighteen are the same bytes as the Instructor 8.1 file: `Asymgif.ocx`, `dzactx.dll`, `ISGDI32.DLL`, `ISGDI32.INI`, `PALOPTX.DLL`, `TBUTIL32.dll`, `TList4.ocx`, and `WINSOX.EXE`.

The six shared system books differ in size from the Instructor 8.1 books. `tb80actr.sbk`, `tb80aicc.sbk`, `tb80anm.sbk`, `tb80ftp.sbk`, `tb80hyp.sbk`, and `tb80r.sbk` in these archives are 29147 bytes. The Instructor 8.1 sizes are 207989, 85719, 64023, 242983, 140613, and 953705. The six archive copies are one file, repeated under those names. That file is described with the other copies below.

`TBCOM.DLL` is 65536 bytes here and 53248 in the Instructor 8.1 directory. `TBINET32.DLL` is 475191 here and 532480 there. `TBKSLICE.DLL` is 65591 here and 57344 there. `tbload.exe` is 397365 here and `Tbload.exe` is 87040 there.

### Only in the Instructor 8.1 TBSystem directory

These 52 names are in the Instructor 8.1 TBSystem directory and absent from the three archives. The size is the Instructor 8.1 file.

| Bytes | File |
|---:|---|
| 1638 | `asym.ini` |
| 30544 | `DIB.DRV` |
| 48661 | `DIBUTIL.DLL` |
| 119296 | `Oxs.dll` |
| 83520 | `PCDLIB.DLL` |
| 2336 | `PCDXBMP.DLL` |
| 33088 | `PHOTO.DLL` |
| 236734 | `PXENGWIN.DLL` |
| 67984 | `TB2FTP.DLL` |
| 66048 | `TB80.EXE` |
| 1669 | `tb80.ini` |
| 247296 | `TB80ACX.DLL` |
| 705824 | `TB80ATH.EXE` |
| 683872 | `TB80BAS.DLL` |
| 68640 | `TB80BMP.DLL` |
| 193216 | `TB80CMP.DLL` |
| 27552 | `TB80CVT.DLL` |
| 106432 | `TB80EDT.DLL` |
| 219872 | `TB80ENU1.DLL` |
| 79360 | `TB80ENU2.DLL` |
| 551968 | `TB80ENU3.DLL` |
| 397824 | `TB80ENU4.DLL` |
| 78848 | `TB80F32L.dll` |
| 101152 | `TB80FLT.DLL` |
| 63872 | `TB80JPG.DLL` |
| 97792 | `TB80LNL.DLL` |
| 23552 | `TB80MAIN.EXE` |
| 24800 | `TB80MM.DLL` |
| 3352 | `TB80MM.INI` |
| 67360 | `TB80NET.EXE` |
| 206528 | `TB80OCX.DLL` |
| 85952 | `TB80OLE.DLL` |
| 169760 | `TB80RCA.DLL` |
| 67824 | `TB80RCR.DLL` |
| 109056 | `TB80RMT.DLL` |
| 462080 | `TB80RTM.EXE` |
| 65536 | `TB80RUN.EXE` |
| 64128 | `TB80UTL.DLL` |
| 75328 | `TB80VBX.DLL` |
| 76512 | `TB80W16.DLL` |
| 83456 | `TB80W32.DLL` |
| 41783 | `TB80XTR.DLL` |
| 31616 | `TBCBT.DLL` |
| 66560 | `TBDB3.DLL` |
| 36800 | `TBDLG.DLL` |
| 15616 | `TBDOS.DLL` |
| 21952 | `TBFILE32.DLL` |
| 30880 | `TBPDX.DLL` |
| 19552 | `TBREG.DLL` |
| 40608 | `TBWIN.DLL` |
| 267264 | `Tlist16p.ocx` |
| 204562 | `VEAMAA51.LEX` |

`TB80.EXE` (66048 bytes), `TB80BAS.DLL` (683872 bytes), and `TB80RTM.EXE` (462080 bytes) are in that absent list. The 11.5 names in these archives are different files: `TB115.EXE` is 1097781 bytes, PE; `TB115BAS.DLL` is 1577010 bytes, PE; `TB115RTM.DLL` is 1720376 bytes, PE. A TB90 set sits beside them: `TB90.EXE` is 929792 bytes, PE; `TB90BAS.DLL` is 1531904 bytes, PE; `TB90RTM.DLL` is 1716224 bytes, PE. Those TB90 and TB115 names are TB90 and TB115.

### Only in the TB115 common files

These 164 basenames occur in the archives and do not occur in the Instructor 8.1 TBSystem directory. Sizes and marks are in the file lists above.

| File |
|---|
| `accent.tlx` |
| `correct.tlx` |
| `ctb40c.sbk` |
| `ctb40r.sbk` |
| `ctb50c.sbk` |
| `ctb60c.sbk` |
| `ctb70c.sbk` |
| `ctb80c.sbk` |
| `ctb85c.sbk` |
| `duzactx.dll` |
| `EndStep.wav` |
| `Instructor115.lic` |
| `Keyboard.wav` |
| `KEYLIB32.dll` |
| `lame.exe` |
| `LicenseMgr115.EXE` |
| `Menued115.chm` |
| `MENUED115.exe` |
| `MENUED90.exe` |
| `Menued90.hlp` |
| `MouseClick.wav` |
| `MouseDown.wav` |
| `MouseUp.wav` |
| `SimBlackClasses.ini` |
| `SimcapAnalyzer.dll` |
| `SimRecorder.chm` |
| `SimRecorder.cnt` |
| `SimRecorder.hlp` |
| `ssce5532.dll` |
| `ssceam.tlx` |
| `ssceam2.clx` |
| `sscebr.tlx` |
| `sscebr2.clx` |
| `ssceca.tlx` |
| `ssceca2.clx` |
| `tb100actr.sbk` |
| `tb100aicc.sbk` |
| `tb100anm.sbk` |
| `tb100ftp.sbk` |
| `tb100hyp.sbk` |
| `tb100r.sbk` |
| `tb105actr.sbk` |
| `tb105aicc.sbk` |
| `tb105anm.sbk` |
| `tb105ftp.sbk` |
| `tb105hyp.sbk` |
| `tb105r.sbk` |
| `tb110actr.sbk` |
| `tb110aicc.sbk` |
| `tb110anm.sbk` |
| `tb110ftp.sbk` |
| `tb110hyp.sbk` |
| `tb110r.sbk` |
| `TB115.EXE` |
| `tb115.ini` |
| `tb115actr.sbk` |
| `TB115ACX.dll` |
| `tb115aicc.sbk` |
| `tb115anm.sbk` |
| `TB115ATH.DLL` |
| `TB115BAS.DLL` |
| `TB115BMP.DLL` |
| `TB115CBT.DLL` |
| `TB115CMP.DLL` |
| `TB115DLG.DLL` |
| `TB115EDT.dll` |
| `TB115ENU1.DLL` |
| `TB115ENU2.DLL` |
| `TB115FLT.DLL` |
| `tb115ftp.sbk` |
| `tb115hyp.sbk` |
| `TB115JPG.DLL` |
| `TB115LNL.DLL` |
| `TB115MM.DLL` |
| `TB115NET.DLL` |
| `TB115OLE.DLL` |
| `tb115r.sbk` |
| `TB115RCA.DLL` |
| `TB115RCR.DLL` |
| `TB115REC.exe` |
| `TB115REC.INI` |
| `TB115RECD.dll` |
| `TB115RED.dll` |
| `TB115REG.DLL` |
| `TB115RTM.DLL` |
| `TB115RUN.EXE` |
| `TB115UTIL32.dll` |
| `TB115UTL.DLL` |
| `TB115WIN.DLL` |
| `tb40anm.sbk` |
| `tb40hyp.sbk` |
| `tb50anm.sbk` |
| `tb50hyp.sbk` |
| `tb50r.sbk` |
| `tb60anm.sbk` |
| `tb60ftp.sbk` |
| `tb60hyp.sbk` |
| `tb60olx.sbk` |
| `tb60r.sbk` |
| `tb70actr.sbk` |
| `tb70anm.sbk` |
| `tb70ftp.sbk` |
| `tb70hyp.sbk` |
| `tb70olx.sbk` |
| `tb70r.sbk` |
| `tb85actr.sbk` |
| `tb85aicc.sbk` |
| `tb85anm.sbk` |
| `tb85ftp.sbk` |
| `tb85hyp.sbk` |
| `tb85r.sbk` |
| `tb89actr.sbk` |
| `tb89aicc.sbk` |
| `tb89anm.sbk` |
| `tb89ftp.sbk` |
| `tb89hyp.sbk` |
| `tb89r.sbk` |
| `TB90.EXE` |
| `tb90.ini` |
| `tb90actr.sbk` |
| `TB90ACX.dll` |
| `tb90aicc.sbk` |
| `tb90anm.sbk` |
| `TB90ATH.DLL` |
| `TB90BAS.DLL` |
| `TB90BMP.DLL` |
| `TB90CBT.DLL` |
| `TB90CMP.DLL` |
| `TB90DLG.DLL` |
| `TB90EDT.DLL` |
| `TB90ENU1.DLL` |
| `TB90ENU2.DLL` |
| `TB90FLT.DLL` |
| `tb90ftp.sbk` |
| `tb90hyp.sbk` |
| `tb90hyp.sbk.old` |
| `TB90JPG.DLL` |
| `TB90LNL.DLL` |
| `TB90MM.DLL` |
| `TB90NET.DLL` |
| `TB90OLE.DLL` |
| `tb90r.sbk` |
| `tb90r.sbk.old` |
| `TB90RCA.DLL` |
| `TB90RCR.DLL` |
| `TB90REC.exe` |
| `TB90REC.INI` |
| `TB90RECD.dll` |
| `TB90RED.dll` |
| `TB90REG.DLL` |
| `TB90RTM.DLL` |
| `TB90RUN.EXE` |
| `TB90UTL.DLL` |
| `TB90WIN.DLL` |
| `tb95actr.sbk` |
| `tb95aicc.sbk` |
| `tb95anm.sbk` |
| `tb95ftp.sbk` |
| `tb95hyp.sbk` |
| `tb95r.sbk` |
| `tech.tlx` |
| `toolbook.ini` |
| `userdic.tlx` |
| `winftp32.dll` |

## System-book names

No file in the three archives ends in `.tbk`. Seventy-seven names end in `.sbk`. Two further names, `tb90hyp.sbk.old` and `tb90r.sbk.old`, carry `.sbk` in the name. Every one of those 79 names contains a version token (`tb40` through `tb115`, or `ctb40` through `ctb85`).

Dedmore's examples are `TB105HYP.SBK` and `TB115HYP.SBK`. This tree has `tb105hyp.sbk` and `tb115hyp.sbk`.

`tb105hyp.sbk` is 29147 bytes. It is one of 62 names that are the same 29147 bytes, SHA-256 `3d25f5b0d545f25cf95d4a50a16760fb6c0057afeed8d7cedd307d39125e7a60`. The PE version resource on that file, read by `version_fields`, is file description `ToolBook`, internal name `TB110`, original filename `TB110.EXE`, product version `11.00.37`, company `SumTotal Systems, Inc.` The export name is `MINSTB32.dll`. The ToolBook object store (`03 4A 42 4F`) is at offset 16440. The reader walks 10 records and returns no book script.

The 62 names are:

`ctb40c.sbk`, `ctb40r.sbk`, `ctb50c.sbk`, `ctb60c.sbk`, `ctb70c.sbk`, `ctb80c.sbk`, `ctb85c.sbk`, `tb40anm.sbk`, `tb40hyp.sbk`, `tb50anm.sbk`, `tb50hyp.sbk`, `tb50r.sbk`, `tb60anm.sbk`, `tb60ftp.sbk`, `tb60hyp.sbk`, `tb60olx.sbk`, `tb60r.sbk`, `tb70actr.sbk`, `tb70anm.sbk`, `tb70ftp.sbk`, `tb70hyp.sbk`, `tb70olx.sbk`, `tb70r.sbk`, `tb80actr.sbk`, `tb80aicc.sbk`, `tb80anm.sbk`, `tb80ftp.sbk`, `tb80hyp.sbk`, `tb80r.sbk`, `tb85actr.sbk`, `tb85aicc.sbk`, `tb85anm.sbk`, `tb85ftp.sbk`, `tb85hyp.sbk`, `tb85r.sbk`, `tb89actr.sbk`, `tb89aicc.sbk`, `tb89anm.sbk`, `tb89ftp.sbk`, `tb89hyp.sbk`, `tb89r.sbk`, `tb90ftp.sbk`, `tb90hyp.sbk.old`, `tb90r.sbk.old`, `tb95actr.sbk`, `tb95aicc.sbk`, `tb95anm.sbk`, `tb95ftp.sbk`, `tb95hyp.sbk`, `tb95r.sbk`, `tb100actr.sbk`, `tb100aicc.sbk`, `tb100anm.sbk`, `tb100ftp.sbk`, `tb100hyp.sbk`, `tb100r.sbk`, `tb105actr.sbk`, `tb105aicc.sbk`, `tb105anm.sbk`, `tb105ftp.sbk`, `tb105hyp.sbk`, `tb105r.sbk`.

That list includes the Instructor 8.1 system-book names `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk`, and it includes `tb105hyp.sbk`. The repeated file carries the TB110 version resource quoted above. The archive copies of `tb80anm.sbk`, `tb80hyp.sbk`, and `tb80r.sbk` are 29147 bytes. The Instructor 8.1 files of those names are 64023, 140613, and 953705 bytes.

Six more names are one file of 29145 bytes, SHA-256 `bb4dc448d1dc772ef7163fb07506e81b3470dcb685dac26aa6f934650f6151cf`:

`tb110actr.sbk`, `tb110aicc.sbk`, `tb110anm.sbk`, `tb110ftp.sbk`, `tb110hyp.sbk`, `tb110r.sbk`.

The version resource on that file is file description `ToolBook`, internal name `TB115`, original filename `TB115.EXE`, product version `11.50.12`, company `SumTotal Systems, Inc.` The export name is `MINSTB32.dll`. The object store is at offset 16438. The reader walks 10 records and returns no book script. `tb110hyp.sbk` is this file.

`tb115hyp.sbk` is a different file: 123049 bytes. Its version resource is internal name `TB115`, original filename `TB115.EXE`, product version `11.50.12`, company `SumTotal Systems, Inc.` The reader returned book script from it. The result is in the next section.

`sscebr.tlx` and `ssceca.tlx` are the same 7798 bytes. They are lexicon files. The five book calls were applied only to names containing `.sbk`.

## What the ToolBook 8 readers returned

The calls were the ones already written for a ToolBook 8 book. `resource_scripts`, `shared_scripts`, and `book_handlers` are `opentoolbook/script.py` on this branch, which is `origin/main` at `ba9ad22`. `book_handlers` is already on that commit, so the `cursor/sbk-handlers-d825` branch was not checked out. `export_module_name` and `version_fields` are `opentoolbook/header.py` at `0f7db87` on `cursor/author-book-header-d825`. That branch is not merged here. The header module was loaded from a separate worktree.

Text expanded from an `.sbk` is book script. `book_handlers` lists a column-0 line `to handle`, `to get`, or `to set` in that text. It does not call the handler. OpenScript is the language of those handlers.

Every name containing `.sbk` was passed to all five calls. The first 16 bytes of every one of those 79 files are `4d5a90000300000004000000ffff0000`.

`export_module_name` returned `MINSTB32.dll` for all 79. `version_fields` returned for all 79. `resource_scripts` returned for all 79. `book_handlers` was then run on each expanded type 10 script. On the two hyperlink books that returned type 19 text, `book_handlers` was run on that text as well.

The same five calls on the Instructor 8.1 `tb80hyp.sbk` (140613 bytes, in the TBSystem directory above) returned export `MINSTB32.dll`, file description `Toolbook II`, internal name `TB80`, original filename `TB80.EXE`, product version `8.10.128`, company `Click2learn, Inc.`, 3 type 10 scripts, and 2 type 19 scripts. That file was a check that the calls run on an Instructor 8.1 system book. It is not one of the archive files.

### Books that returned book script

Eleven files are larger than the two repeated stubs, and each of those eleven is its own bytes. File description is `ToolBook` and the company is `SumTotal Systems, Inc.` on all eleven. The original filename is `TB90.EXE` on the TB90 books and `TB115.EXE` on the TB115 books.

| File | Bytes | Records | Internal | Product version | Type 10 | Chars | Handlers | Type 19 |
|---|---:|---:|---|---|---:|---:|---:|---|
| `tb90actr.sbk` | 359825 | 48 | `TB90` | `9.00.409` | 12 | 226583 | 371 | 0 |
| `tb90aicc.sbk` | 95975 | 21 | `TB90` | `9.01.505` | 3 | 30972 | 59 | 0 |
| `tb90anm.sbk` | 76795 | 16 | `TB90` | `9.00.409` | 1 | 32731 | 47 | 0 |
| `tb90hyp.sbk` | 123011 | 26 | `TB90` | `9.00.409` | 3 | 51547 | 116 | 2 |
| `tb90r.sbk` | 1008173 | 148 | `TB90` | `9.01.526` | 61 | 573219 | 923 | refused |
| `tb115actr.sbk` | 363667 | 48 | `TB115` | `11.50.21` | 12 | 228079 | 380 | 0 |
| `tb115aicc.sbk` | 96015 | 21 | `TB115` | `11.50.12` | 3 | 30974 | 59 | 0 |
| `tb115anm.sbk` | 76941 | 16 | `TB115` | `11.50.12` | 1 | 32733 | 47 | 0 |
| `tb115ftp.sbk` | 300269 | 40 | `TB115` | `11.50.12` | 15 | 107144 | 147 | refused |
| `tb115hyp.sbk` | 123049 | 25 | `TB115` | `11.50.12` | 3 | 51557 | 116 | 2 |
| `tb115r.sbk` | 1251439 | 156 | `TB115` | `11.50.30` | 63 | 644574 | 1022 | refused |

Type 10 is the number of scripts `resource_scripts` returned. Chars is the sum of those script lengths. Handlers is the number of handlers `book_handlers` listed in that type 10 text. Type 19 is the number of scripts `shared_scripts` returned, or `refused` when it raised.

`tb90hyp.sbk` and `tb115hyp.sbk` each returned two type 19 scripts, resource ids 100 and 102, 856 characters together. `book_handlers` listed two handlers in that text: `handle closeWindow`, and `handle setDefButton` with argument `btn`.

The object store sits at offset 16384 in the five `tb90` books and at offset 16438 in the six `tb115` books.

### What `shared_scripts` refused

Three files raised. The first 16 bytes of each are `4d5a90000300000004000000ffff0000`. The type 10 scripts of the same files had already been returned, and `book_handlers` listed the handlers in that type 10 text.

| File | Exception |
|---|---|
| `tb90r.sbk` | `ValueError: type 19 resource 103 has no handler` |
| `tb115ftp.sbk` | `ValueError: type 19 resource 104 has no handler` |
| `tb115r.sbk` | `ValueError: type 19 resource 103 has no handler` |

### Names from Dedmore's runtime notes

`tb115r.sbk` is the runtime system book in this tree (1251439 bytes, product version `11.50.30`). `book_handlers` listed these handlers in its type 10 book script:

- `get ASYM_StandardFolderPath`, argument `f`
- `get ASYM_GetSystemColor`, argument `nm`
- `get ASYM_ProductDirectory`
- `get ASYM_PathOfFile`, argument `pth`

The same four handlers are in the type 10 book script of `tb90r.sbk`. That file's version resource says internal name `TB90`, product version `9.01.526`.

The expanded type 10 text of `tb115r.sbk` also uses the name `sysToolBookDirectory`. One line is `fN = ASYM_FindPathFile(sysToolBookDirectory & whatFile,"")`. `book_handlers` did not list `sysToolBookDirectory` as a handler. `tb115anm.sbk` sets `runtimeName = "tb115r.sbk"` and builds a path with `sysToolBookDirectory & runtimeName`. `tb115aicc.sbk` contains the line `if "tb115r.sbk" is not in sysbooks`. `tb115ftp.sbk` uses the same `runtimeName = "tb115r.sbk"` line.

The ASCII names `getConfigVar` and `setConfigVar` are absent from every `.sbk` in these archives. A byte search found those names in `TB90CMP.DLL`, `TB115CMP.DLL`, and `TB115UTL.DLL`. Those three are core files. The search matched the name and copied nothing around it.

The expanded type 10 text of `tb115ftp.sbk` does not contain `ASYM_GetSystemColor`. The file's own bytes do contain that ASCII name. `shared_scripts` refused type 19 resource 104 in that file, so that resource is not part of the expanded text.

The 68 stub names, including `tb105hyp.sbk`, `tb80anm.sbk`, `tb80hyp.sbk`, `tb80r.sbk`, and `tb110hyp.sbk`, returned no type 10 script and no type 19 script. `book_handlers` had no text to list.

## Handlers listed from the books that returned book script

Each line is one handler `book_handlers` listed in the type 10 book script: kind, name, then the argument text when the header line has any. This is the text the ToolBook 8 reader already expands. It is not a call.

### `tb90actr.sbk`

371 handlers (89 handle, 251 get, 31 set) from 12 type 10 scripts, resource ids 1314, 1316, 1318, 1320, 1322, 1324, 1326, 1328, 1330, 1332, 1334, 1336.

- `handle enterBook`
- `handle enterApplication`
- `handle leaveBook`
- `handle ASYM_LoadBook`
- `handle ASYM_UnloadBook`
- `handle linkSysbook`
- `handle author`
- `handle reader`
- `get ASYM_EA_GetParameterList` — `objectRef, event`
- `get ASYM_EA_ParameterList` — `event, obRef`
- `set ASYM_EA_ParameterList` — `event to value`
- `handle ASYM_EA_InitParameterList`
- `get ASYM_EA_GetLocalVariableList` — `objectRef, event`
- `get ASYM_EA_GetGlobalVariableList` — `OBJECT objectRef`
- `get ASYM_EA_LocalVariableInitialValue` — `variableName, objectRef, event`
- `set ASYM_EA_LocalVariableInitialValue` — `variableName, objectRef, event to value`
- `get ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event to value`
- `get ASYM_EA_GlobalVariableInitialValue` — `variableName, objectRef`
- `set ASYM_EA_GlobalVariableInitialValue` — `variableName, objectRef to value`
- `get ASYM_EA_GlobalVariable` — `variableName`
- `get ASYM_EA_FindLocalVariable` — `targetRef, event, varName`
- `get ASYM_EA_FindGlobalVariable` — `targetRef, varName`
- `handle ASYM_EA_RemoveParameter` — `parameterName, objectRef, actionBlockName`
- `handle ASYM_EA_RemoveLocalVariable` — `variableName, objectRef, event`
- `handle ASYM_EA_RemoveGlobalVariable` — `variableName, objectRef`
- `get ASYM_EA_LocalVariableName` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableName` — `varID, targetRef, event to value`
- `get ASYM_EA_GlobalVariableName` — `varID, targetRef`
- `set ASYM_EA_GlobalVariableName` — `varID, targetRef to value`
- `get ASYM_EA_CreateVarInfo` — `varName, varScope, targetRef, event, varID, indexExpression`
- `get ASYM_EA_VariableIsArray` — `varID, varScope, targetRef, event`
- `get ASYM_EA_LocalVariableIsArray` — `varID, targetRef, event`
- `get ASYM_EA_GlobalVariableIsArray` — `varName, targetRef`
- `get ASYM_EA_ParameterIsArray` — `paramNum, targetRef, event`
- `get ASYM_EA_GetNewVariableID` — `varScope, targetRef, event`
- `get ASYM_EA_ExtractVariableName` — `varInfo, targetRef, event`
- `get ASYM_EA_VariableNameFromID` — `varID, varScope, targetRef, event`
- `get ASYM_EA_ExtractVariableScope` — `varInfo, targetRef, event`
- `handle ASYM_EA_InitGlobalVariables` — `bkRef`
- `get ASYM_EA_GetTokenList`
- `get ASYM_EA_GetTokenDataType` — `token`
- `get ASYM_EA_IsVariableReference` — `varInfo, selfRef, event`
- `get ASYM_EA_IsPropertyReference` — `propInfo`
- `get ASYM_EA_Get` — `STACK dataStructure, STRING key`
- `get ASYM_EA_Set` — `STACK dataStructure, STRING key, STACK value`
- `get ASYM_EA_GetActionArray` — `event, obRef`
- `get ASYM_EA_GetActionBlockArray` — `actionBlockName, bkRef`
- `get ASYM_EA_GetActionMethodArray` — `actionMethodName, obRef`
- `get ASYM_EA_GetActionCount` — `actionArray[]`
- `get ASYM_EA_GetActionInfo` — `actionArray[], actionNum`
- `get ASYM_EA_GetActionKey` — `actionInfo, validate`
- `get ASYM_EA_FindNextClause` — `actionArray[] by reference, actionNumber`
- `get ASYM_EA_FindStructureEnd` — `actionArray[] by reference, actionNumber`
- `get ASYM_EA_FindStructureTypeEnd` — `actionArray[] by reference, actionNumber, structureType`
- `get ASYM_EA_FindStructureStart` — `actionArray[] by reference, actionNum`
- `get ASYM_EA_ExpressionDisplayStringFromExpressionInfo` — `expression, objectRef, event, editing`
- `get ASYM_EA_ExpressionOperatorArray`
- `set ASYM_EA_ExpressionOperatorArray` — `to operatorArray[][]`
- `get ASYM_EA_ExpressionDataRuleArray`
- `set ASYM_EA_ExpressionDataRuleArray` — `to dataRuleArray[][]`
- `handle ASYM_EA_ExpressionInitializeOperatorArrays`
- `get ASYM_EA_ResolveObject` — `objectInfo, obRef, targetRef, validate`
- `get ASYM_EA_ResolveBookName` — `bookName, obRef`
- `get ASYM_EA_FindPage` — `pageName, pageID, bookRef, obRef`
- `get ASYM_EA_FindBackground` — `bgName, bgID, bookRef, obRef`
- `get ASYM_EA_FindObject` — `objectType, objectName, objectID, layerRef, obRef`
- `get ASYM_EA_ConstructObjectIdentifier` — `targetRef, objectRef, noSelf, thisPage, layerRef`
- `get ASYM_EA_ObjectDescriptionFromObjectInfo` — `obInfo, selfRef, event, initCaps, obRef`
- `get ASYM_EA_RelativeObjectDescription` — `targetRef, sourceRef, initCaps, event`
- `get ASYM_EA_PopupPage` — `pageRef, closeOnClick`
- `get ASYM_EA_ResetPages` — `firstPage, lastPage`
- `get ASYM_EA_PlayAnimation` — `obRef, num`
- `handle doneAnimatingNotify` — `status, obRef`
- `get ASYM_EA_MessageBox` — `msg, cptn, icn, btns, helpTopicID, helpFile`
- `handle ASYM_EA_SendWindowsMessage` — `msgName`
- `handle ASYM_EA_CheckSysError` — `obRef, event, actionNum, bs`
- `get ASYM_EA_ObjectCache` — `obCache, obInfo, objectRef, targetRef`
- `get ASYM_EA_ObjectFromExpression` — `obType, obName, selfRef`
- `get ASYM_EA_ShellExecute` — `source, bkRef`
- `get ASYM_EA_ScoreQuestion` — `obRef, showFB, showScore, scoreFormat, lockQn, resetQn`
- `get ASYM_EA_ScorePages` — `startPgNum, endPgNum, showScore, scoreFormat, lockQn, resetQn, ignoreSkip`
- `get ASYM_EA_ScorePage` — `pgRef, showScore, scoreFormat, lockQn, resetQn, returnMaxScore`
- `handle ASYM_EA_ShowScore` — `score, mode`
- `get ASYM_SetFocus`
- `get ASYM_RemoveFocus`
- `get ASYM_EA_PropertyDataType` — `obRef, propName`
- `get ASYM_EA_MethodList` — `obRef`
- `get ASYM_EA_MethodInfo` — `obRef, method`
- `get ASYM_EA_PropertyEnumInt` — `obRef, propName`
- `get ASYM_EA_PropertyEnumString` — `obRef, propName`
- `get ASYM_ReverseStack` — `STACK stk`
- `handle ASYM_EA_RuntimeError` — `errorTxt, objectRef, event, actionNumber`
- `get ASYM_EA_ActionName` — `actionKey`
- `get ASYM_EA_IsActionValid` — `actionInfo, targetObject, event`
- `get ASYM_EA_ActionErrors` — `actionInfo, targetObject, event, noRecurse`
- `get ASYM_EA_EventString` — `event`
- `get ASYM_EA_GetMethodType` — `obRef, methodName`
- `get ASYM_EA_InternalMethodList` — `obType`
- `set ASYM_EA_InternalMethodList` — `obType to value`
- `get ASYM_EA_InternalMethodListFromObjectRef` — `obRef`
- `handle ASYM_EA_InitInternalMethodList`
- `get ASYM_EA_ObjectTypesFromObjectRef` — `obRef`
- `get ASYM_EA_GetsFocus` — `targetRef`
- `get isNumber` — `value`
- `get ASYM_EA_EQ` — `a, b`
- `get ASYM_EA_NE` — `a, b`
- `get ASYM_EA_GT` — `a, b, asText`
- `get ASYM_EA_LT` — `a, b, asText`
- `get ASYM_EA_GE` — `a, b, asText`
- `get ASYM_EA_LE` — `a, b, asText`
- `get left`
- `set left` — `to value`
- `get top`
- `set top` — `to value`
- `get width`
- `set width` — `to value`
- `get height`
- `set height` — `to value`
- `get selectedItemText`
- `set selectedItemText` — `to value`
- `get ASYM_CleanCaption`
- `get ASYM_ItemText`
- `set ASYM_ItemText` — `to value`
- `get ASYM_ItemSelected`
- `set ASYM_ItemSelected` — `to value`
- `get lastScore`
- `get minimumScore`
- `get maximumScore`
- `get locked`
- `get tryCount`
- `get tryLimit`
- `get mediaPosition`
- `set mediaPosition` — `to value`
- `get mediaPlaying`
- `get ASYM_EA_GetClipRef` — `obRef`
- `get visited`
- `get title`
- `get description`
- `get studentName`
- `handle selectChange` — `choice`
- `handle ASYM_Select`
- `handle buttonDown`
- `handle mouseEnter`
- `handle mouseLeave` — `pos`
- `handle buttonUp`
- `handle keyDown` — `key, isShift, isCtrl`
- `get ASYM_EA_IsListBox` — `targetRef`
- `handle ASYM_Trigger`
- `handle stopAllMedia` — `recurse`
- `handle enterField`
- `handle leaveField`
- `handle clearOldText` — `targetRef`
- `handle ASYM_StartSimulation`
- `handle ASYM_EndSimulation`
- `handle ASYM_StartStep`
- `handle ASYM_EndStep`
- `handle ASYM_AttemptStep`
- `handle ASYM_Changed`
- `handle ASYM_Complete`
- `handle ASYM_User`
- `handle ASYM_EA_Make`
- `get ASYM_DuplicateChar` — `txt, chr`
- `get ASYM_SIM_IsEvaluationObject` — `obRef`
- `get ASYM_SIM_IsTriggerObject` — `obRef`
- `get ASYM_SIM_isObjectClickable` — `obRef`
- `get ASYM_SIM_ObjectGetsFocus` — `obRef`
- `get ASYM_SIM_ObjectHasSelectableItems` — `obRef`
- `get ASYM_SIM_ObjectType` — `obRef`
- `get ASYM_SIM_ObjectDescription` — `obRef, initCaps`
- `get ASYM_SIM_ObjectTypeDescription` — `obType, obRef, initCaps`
- `get ASYM_SIM_TriggerObjectDescription` — `obRef`
- `get ASYM_SIM_KeyString` — `key, caps, useThe`
- `get ASYM_SIM_ObjectState` — `obRef, obType`
- `set ASYM_SIM_ObjectState` — `obRef, obType to value`
- `get ASYM_SIM_DefaultTextEditState` — `obState`
- `get ASYM_SIM_StateMatches` — `obRef, requiredState, actualState`
- `get ASYM_SIM_EditFieldStateMatches` — `requiredState, actualState`
- `get ASYM_SIM_MaxFeedbackAttempts`
- `get ASYM_SIM_GetAutoInstructionText` — `selfRef, stepInfo, allEvalObjects[][] by reference`
- `get ASYM_SIM_GetAutoTriggerFeedback` — `selfRef, triggerEvents`
- `get ASYM_SIM_GetAutoObjectFeedback` — `obRef, actualState, requiredState, previousState, isPopup, objDescTemplate`
- `get ASYM_SIM_GetFeedbackText` — `feedbackInfo, simMode, currentTry, maxTries, forceLastAttempt`
- `set ASYM_SIM_ItemProperty` — `propName, itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemProperty` — `propName, itemType, stepNum, itemNum`
- `set ASYM_SIM_ItemData` — `itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemData` — `itemType, stepNum, itemNum`
- `get ASYM_SIM_GetIncludedObjectsArray`
- `get ASYM_SIM_CurrentStepID`
- `get ASYM_SIM_CurrentStepName`
- `get ASYM_SIM_CurrentStepInfo`
- `get ASYM_SIM_StepInfo` — `stepNum`
- `get ASYM_SIM_StartingMode`
- `get ASYM_SIM_GetBookMode`
- `handle ASYM_SIM_DisplayInstructions` — `simMode, stepInfo, includedObjects[][] by reference`
- `handle ASYM_SIM_ShowFeedback` — `stepInfo, stepNum, triggerEvents, matchingTriggerInfo, simMode, initialFeedbackText, forceLastAttempt`
- `get ASYM_SIM_GetObjectDescriptionString` — `obRef, obInfo, obType`
- `get ASYM_SIM_GetDefaultObjectDescriptionString` — `obRef, obType`
- `get ASYM_SIM_GetErrorObjectInfo` — `stepInfo, needFeedback, needRequiredState, forceLastAttempt`
- `get ASYM_SIM_RememberListboxState` — `pRef`
- `get ASYM_SIM_RestoreListboxState` — `pRef, stateInfo`
- `handle ASYM_SIM_HidePointer` — `animateMouse`
- `handle ASYM_SIM_NavigatePointerTo` — `mousePointer, pos, targetViewer, notifyObject, timeFactor, nextAction`
- `get ASYM_SIM_PauseMousePointer` — `animateMouse`
- `get ASYM_SIM_ResumeMousePointer` — `animateMouse, details`
- `handle ASYM_SIM_ShowMousePointer` — `animateMouse, targetViewer, pos, isPixels`
- `handle ASYM_SIM_ShowMousePointerClick` — `animateMouse, clickType`
- `handle ASYM_SIM_HideMousePointerClick` — `animateMouse`
- `handle ASYM_SIM_SetPointerTimeFactor` — `animateMouse, timeFactor`
- `handle ASYM_SIM_ShowComboPopup` — `comboRef, targetViewer`
- `get ASYM_SIM_GetComboScrollDir` — `itemNum`
- `get ASYM_SIM_GetComboItemPosition` — `itemNum`
- `get ASYM_SIM_GetComboScrollPosition` — `dir`
- `get ASYM_SIM_ScrollPopup` — `itemNum`
- `handle ASYM_SIM_SelectComboboxItem` — `obState`
- `handle ASYM_SIM_CloseComboPopup`
- `get ASYM_SIM_GetComboPopupState`
- `get ASYM_SIM_RestoreComboPopupState` — `popupState`
- `handle buttonClick` — `pos, isShift, isCtrl`
- `handle rightButtonDown` — `pos, isShift, isCtrl`
- `handle buttonDoubleClick` — `pos, isShift, isCtrl`
- `get ASYM_EA_GetActionArray` — `eventName, obRef`
- `get ASYM_EA_GetActionBlockArray` — `actionBlockName, bkRef`
- `get ASYM_EA_GetActionMethodArray` — `actionMethodName, obRef`
- `get ASYM_EA_PopupPage` — `pageRef, closeOnClick`
- `get ASYM_EA_ResetPages` — `firstPage, lastPage`
- `get ASYM_EA_PlayAnimation` — `obRef, num`
- `get ASYM_EA_ShellExecute` — `source, bkRef`
- `get ASYM_EA_ScoreQuestion` — `obRef, showFB, showScore, scoreFormat, lockQn, resetQn`
- `get ASYM_EA_ScorePages` — `startPgNum, endPgNum, showScore, scoreFormat, lockQn, resetQn, ignoreSkip`
- `get ASYM_EA_ScorePage` — `pgRef, showScore, scoreFormat, lockQn, resetQn, returnMaxScore`
- `handle ASYM_EA_ShowScore` — `score, mode`
- `get ASYM_EA_ConvertDataType` — `value, dataType`
- `get ASYM_EA_ExpressionOperatorArray`
- `get ASYM_EA_ExpressionDataRuleArray`
- `set ASYM_EA_ExpressionOperatorArray` — `to operatorArray[][]`
- `set ASYM_EA_ExpressionDataRuleArray` — `to dataRuleArray[][]`
- `handle ASYM_EA_ExpressionInitializeOperatorArrays`
- `get ASYM_EA_ExpressionDisplayStringFromExpressionInfo` — `STACK expression, targetRef, event, editing, parentHasBrackets, parentOperatorPrecedence, parentAssociative`
- `get ASYM_EA_GetGlobalVariableList` — `targetRef`
- `get ASYM_EA_GetLocalVariableList` — `targetRef, event`
- `get ASYM_EA_GetParameterList` — `targetRef, event`
- `get ASYM_EA_LocalVariableInitialValue` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableInitialValue` — `varID, targetRef, event to value`
- `get ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event to value`
- `get ASYM_EA_GlobalVariableInitialValue` — `varName, targetRef`
- `set ASYM_EA_GlobalVariableInitialValue` — `varName, targetRef to value`
- `get ASYM_EA_VariableIsArray` — `varID, varScope, targetRef, event`
- `get ASYM_EA_LocalVariableIsArray` — `varID, targetRef, event`
- `get ASYM_EA_GlobalVariableIsArray` — `varName, targetRef`
- `get ASYM_EA_ParameterIsArray` — `paramNum, targetRef, event`
- `handle ASYM_EA_RemoveParameter` — `parameterName, targetRef, actionBlockName`
- `handle ASYM_EA_RemoveLocalVariable` — `varID, targetRef, event`
- `handle ASYM_EA_RemoveGlobalVariable` — `varName, targetRef, event`
- `get ASYM_EA_LocateVariable` — `STACK varList, varName`
- `get ASYM_EA_LocalVariableName` — `varID, targetRef, event`
- `get ASYM_EA_GlobalVariableName` — `varID, targetRef`
- `set ASYM_EA_LocalVariableName` — `varID, targetRef, event to value`
- `set ASYM_EA_GlobalVariableName` — `varID, targetRef to value`
- `get ASYM_EA_ExtractVariableName` — `varInfo, targetRef, event`
- `get ASYM_EA_VariableNameFromID` — `varID, varScope, targetRef, event`
- `get ASYM_EA_ExtractVariableScope` — `varInfo, targetRef, event`
- `get ASYM_EA_CreateVarInfo` — `varName, varScope, targetRef, event, varID, indexExpression`
- `get ASYM_EA_GetNewVariableID` — `varScope, targetRef, event`
- `handle ASYM_EA_InitGlobalVariables` — `bkRef`
- `handle initVar` — `_varName, _varInitValue`
- `handle initArray` — `_varName`
- `get ASYM_EA_GlobalVariable` — `_ASYM_EA_VarName`
- `get ASYM_EA_FindLocalVariable` — `targetRef, event, varName`
- `get ASYM_EA_FindGlobalVariable` — `targetRef, varName`
- `get ASYM_EA_ParameterList` — `event, obRef, showArrays`
- `set ASYM_EA_ParameterList` — `event to value`
- `handle ASYM_EA_InitParameterList`
- `get ASYM_EA_ActionName` — `actionKey`
- `get ASYM_EA_IsActionValid` — `actionInfo, targetObject, event, forceReevaluate`
- `get ASYM_EA_ActionErrors` — `actionInfo, selfRef, event`
- `get objectTypesFromObjectRef` — `obRef`
- `get getsFocus` — `targetRef`
- `handle initInternalMethodList`
- `get internalMethodListFromObjectRef` — `obRef`
- `get getMethodType` — `obRef, methodName`
- `handle ASYM_SIM_ProcessEvent` — `simRef, event, targetRef, mod1, mod2`
- `get isTriggerTargetIncluded` — `simRef, obRef, event`
- `get ASYM_SIM_GetErrorObjectInfo` — `simRef, stepInfo, needFeedback, needRequiredState, forceLastAttempt`
- `get ASYM_SIM_StateMatches` — `obRef, requiredState, actualState`
- `get ASYM_SIM_EditFieldStateMatches` — `requiredState, actualState`
- `handle ASYM_SIM_ShowFeedback` — `simRef, stepInfo, stepNum, triggerEvents, matchingTriggerInfo, simMode, initialFeedbackText, forceLastAttempt`
- `handle ASYM_SIM_DisplayInstructions` — `simRef, simMode, stepInfo, includedObjects[][] by reference`
- `get ASYM_SIM_IsEvaluationObject` — `obRef`
- `get ASYM_SIM_IsTriggerObject` — `obRef`
- `get ASYM_SIM_IsMenuObject` — `obRef`
- `get ASYM_SIM_IsObjectClickable` — `obRef`
- `get ASYM_SIM_ObjectGetsFocus` — `obRef`
- `get ASYM_SIM_ObjectHasSelectableItems` — `obRef`
- `get ASYM_SIM_ObjectType` — `obRef`
- `get ASYM_SIM_ObjectDescription` — `obRef, initCaps`
- `get ASYM_SIM_ObjectTypeDescription` — `obType, obRef, initCaps`
- `get ASYM_SIM_TriggerObjectDescription` — `obRef`
- `get ASYM_SIM_KeyString` — `key, caps, useThe`
- `get ASYM_SIM_ObjectState` — `obRef, obType`
- `set ASYM_SIM_ObjectState` — `obRef, obType to value`
- `get ASYM_SIM_DefaultTextEditState` — `obState`
- `get ASYM_SIM_MaxFeedbackAttempts`
- `get ASYM_SIM_GetAutoInstructionText` — `selfRef, stepInfo, includedObjects[][] by reference`
- `get ASYM_SIM_GetAutoTriggerFeedback` — `selfRef, triggerEvents`
- `get ASYM_SIM_GetAutoObjectFeedback` — `obRef, actualState, requiredState, previousState, isPopup, objDescTemplate`
- `get ASYM_SIM_GetFeedbackText` — `feedbackInfo, simMode, currentTry, maxTries, forceLastAttempt`
- `get buildItemString` — `itms, txt`
- `get ASYM_SIM_StartingMode` — `simRef`
- `get ASYM_SIM_GetBookMode` — `simRef`
- `set ASYM_SIM_ItemProperty` — `simRef, propName, itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemProperty` — `simRef, propName, itemType, stepNum, itemNum`
- `get validateState` — `stateval, obRef`
- `get convertToFeedbackTypeName` — `propName`
- `get convertToFeedbackValName` — `propName`
- `set ASYM_SIM_ItemData` — `simRef, itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemData` — `simRef, itemType, stepNum, itemNum`
- `get ASYM_SIM_GetObjectDescriptionString` — `obRef, obInfo, obType`
- `get ASYM_SIM_GetDefaultObjectDescriptionString` — `obRef, obType`
- `get objectDescriptionFromTemplate` — `objDescTemplate, obRef, value`
- `get getObjectDescriptionTemplate` — `simRef, obRef, includedObjects[][] by reference`
- `get ASYM_SIM_RememberListboxState` — `pRef`
- `get ASYM_SIM_RestoreListboxState` — `pRef, listInfo`
- `get tlEscape` — `t`
- `get tlUnescape` — `t`
- `handle showPointer` — `animateMouse, ownerViewer, pos, isPixels`
- `get initMousePointer` — `ownerViewer`
- `handle setRegion`
- `get createRegion` — `obRef, vRef`
- `handle showClick` — `animateMouse, clickType`
- `handle hideClick` — `animateMouse`
- `get pausePointer` — `animateMouse`
- `get resumePointer` — `animateMouse, details`
- `handle hidePointer` — `animateMouse`
- `handle navigateTo` — `mousePointer, p3, targetViewer, notifyObject, timeFactor, nextAction`
- `handle animatePointer` — `ax, ay, bx, by, cx, cy, dx, dy`
- `get getControlPoints` — `x0, y0, x3, y3`
- `get getControlPointAngles` — `dx, dy`
- `get getAngle` — `dx, dy`
- `get roundToPageUnitsX` — `value`
- `get roundToPageUnitsY` — `value`
- `handle setPosition` — `vRef, viewerPos, forceMove`
- `handle showViewer` — `vRef`
- `handle closeViewer` — `vRef`
- `get windowMoved` — `hWnd, dwMsg, wParam, lParam`
- `handle setTimeFactor` — `animateMouse, timeFactor`
- `handle ASYM_Reset`
- `get getTotalTime` — `hyp, timeFactor`
- `get adjustStartTime` — `startTime, currentTime`
- `handle showComboPopup` — `comboRef, targetViewer, forceSelectedTextline, forceScroll`
- `handle closeComboPopup`
- `get getComboPopupState`
- `get restoreComboPopupState` — `popupState`
- `get getScrollDir` — `itemNum`
- `get getItemPosition` — `itemNum`
- `get getScrollPosition` — `dir`
- `get scrollPopup` — `itemNum`
- `handle selectItem` — `obState`
- `get roundToPageUnitsX` — `value`
- `get roundToPageUnitsY` — `value`
- `get convertToSourceUnits` — `x, y`
- `get getScrollButtonWidth`
- `get getScrollButtonHeight`
- `handle setPosition` — `vRef, viewerPos, forceSet`
- `handle showViewer` — `vRef`
- `handle closeViewer` — `vRef`
- `get windowMoved` — `hWnd, dwMsg, wParam, lParam`
- `handle author`
- `handle reader`
- `handle buttonClick`

### `tb90aicc.sbk`

59 handlers (8 handle, 51 get, 0 set) from 3 type 10 scripts, resource ids 1035, 1037, 1039.

- `handle Init_AICC_Standards`
- `get ASYM_AICC_Init`
- `get ASYM_AICC_ExtractFromCmdLine` — `commandLn`
- `get ASYM_AICC_GetMultipleParameters` — `paramList, _text, storeInVars`
- `get paramName_VarEquivalent` — `paramName`
- `get ASYM_AICC_GetSingleParameter` — `paramName, _text`
- `get ASYM_OLX`
- `handle enterSystem`
- `handle linkSysbook`
- `handle unlinkSelf`
- `handle unlinkSysbook`
- `handle exit`
- `get ASYM_CMS_CollectTotalScore` — `includeSkip`
- `get ASYM_AICC_CorrectWidgetAnswers` — `ansArray[][]`
- `get ASYM_ACIEndLesson` — `status`
- `get ASYM_CMS_AccessRights`
- `get ASYM_CMS_UserID`
- `get ASYM_CMS_UserName`
- `get ASYM_CMS_BookName`
- `get ASYM_CMS_RuntimeLinked`
- `get ASYM_CMS_CMSApplicationName`
- `get ASYM_CMS_AskToContinue`
- `get ASYM_CMS_BookmarkFileName`
- `get ASYM_CMS_DataDir`
- `get ASYM_CMS_dbError`
- `get ASYM_CMS_dbErrorString`
- `get ASYM_CMS_dbOK`
- `get ASYM_CMS_EnterApplication`
- `get ASYM_CMS_GetRecordedScore` — `arg`
- `get ASYM_CMS_GoToModule`
- `get ASYM_CMS_IniFile`
- `get ASYM_CMS_IsCourseCompleted`
- `get ASYM_CMS_LeaveApplication`
- `get ASYM_CMS_LogDir`
- `get ASYM_CMS_LogFileName`
- `get ASYM_CMS_LogType`
- `get ASYM_CMS_MarkAsCompleted`
- `get ASYM_CMS_ModuleFileName`
- `get ASYM_CMS_RecordScore`
- `get ASYM_CMS_ReturnToCMS`
- `get ASYM_CMS_SetBookmarkFileName`
- `get ASYM_CMS_SetLogDir`
- `get ASYM_CMS_SetLogFileName`
- `get ASYM_CMS_SetLogType`
- `get ASYM_CMS_SetNextModule`
- `get asym_CMS_sysBookName`
- `get AICC_ExitAU`
- `get ASYM_INET_DLL_Link`
- `get urlEncode` — `str`
- `get ASYM_AICC_SpecialCharsContract` — `s`
- `get formatTimetoSec` — `whatTime`
- `get formatTimetoHHMinSEC` — `whattime,No_00_flag`
- `get ASYM_AICC_ProcessForError` — `returnString`
- `handle ASYM_AICC_ImmediateExit`
- `get ASYM_AICC_CleanupResponse` — `txt`
- `handle AICC_Set_Score` — `status`
- `get ASYM_AICC_BuildPostStr_PutParam` — `status, score, _time`
- `get ASYM_ConvertToAICCPercent` — `totalScore`
- `get _AICC_ExitAU`

### `tb90anm.sbk`

47 handlers (18 handle, 19 get, 10 set) from 1 type 10 scripts, resource ids 267.

- `handle linkSysbook`
- `handle moved`
- `handle playAnimation` — `animation, notifyObject, waitTillDone, options`
- `handle ASYM_Reset`
- `handle pauseAnimation` — `status`
- `handle stopAnimation` — `status, options`
- `handle ASYM_CleanupAnimations`
- `handle jumpToStep` — `whichStep, whichAnimation`
- `handle jumpToPercent` — `percentComplete, whichAnimation`
- `handle playStep` — `currentAnim`
- `handle updateCel` — `theTarget, StepsPerCel, stepNumber,previousstepNumber`
- `handle doneAnimatingNotify` — `status,whatObject`
- `handle restoreAnimation` — `objectList, animationList`
- `get ASYM_CloseAllAnimations`
- `handle closeAllAnimations`
- `get closeAllAnimations_WinMsg` — `-- process after call to system`
- `get objectAnimation` — `rowNum`
- `set objectAnimation` — `to animationSettings[]`
- `get animationCacheEntry` — `theTarget`
- `get anim_Offset`
- `set anim_Offset` — `to value`
- `get anim_CurrentStep`
- `set anim_CurrentStep` — `to value`
- `get anim_NumRepetitions`
- `set anim_NumRepetitions` — `to value`
- `get anim_CelAnimation` — `whichAnimation`
- `set anim_CelAnimation` — `to value`
- `get anim_ShowAllSteps` — `whichAnimation`
- `set anim_ShowAllSteps` — `whichAnimation to value`
- `get anim_Duration` — `whichAnimation`
- `set anim_Duration` — `whichAnimation to value`
- `get anim_NumSteps` — `whichAnimation`
- `set anim_NumSteps` — `whichAnimation to value`
- `get anim_StepsPerCell` — `whichAnimation`
- `set anim_StepsPerCell` — `whichAnimation to value`
- `get anim_StartPosition` — `whichAnimation`
- `set anim_StartPosition` — `whichAnimation to value`
- `get anim_StartSize` — `whichAnimation`
- `get anim_EndSize` — `whichAnimation`
- `get anim_StartTime`
- `get anim_elapsedTime`
- `get anim_currentTime`
- `handle updateAnimations`
- `get animTimer` — `whatHandle, whatMsg, wparam`
- `handle startAnimTimer`
- `handle stopAnimTimer`
- `handle author`

### `tb90hyp.sbk`

116 handlers (20 handle, 93 get, 3 set) from 3 type 10 scripts, resource ids 634, 636, 638.

- `handle linkSysBook`
- `get ASYM_URLSpecialCharsExpand` — `s`
- `get ASYM_URLSpecialCharsContract` — `s`
- `get _ASYM_AddAnswerArrayHyperlink` — `fixed ansArray[][] by reference, int iRow, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddAnswerHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddHyperlinkToArray` — `hyperlinks[][] by reference,linkName, pgRef,  transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddLinkToArray` — `hyperlinks[][] by reference, int iRow, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_requestRemoveAmpersand` — `txt`
- `get _ASYM_BadLinksList` — `fixed hyperlinks[][] by reference`
- `get _ASYM_ClearAnsArrayHyperlink` — `fixed ansArray[][] by reference, int iRow`
- `get _ASYM_ClearAnswerHyperlink` — `obj, linkName`
- `get _ASYM_ClearHyperlink` — `obj, linkName`
- `get _ASYM_ClearHyperlinkFromArray` — `hyperlinks[][] by reference, linkName`
- `get _ASYM_ExecHyperLink` — `fixed hyperlinks[][] by reference, linkName`
- `get _ASYM_HyperlinkCandidates` — `obj, candidates[] by reference`
- `get _ASYM_HyperlinkLinkInfo` — `hyperlinks[][] by reference, linkName, resolv`
- `get _ASYM_HyperlinkIRow` — `STRING linkName, hyperlinks[][] by reference`
- `get _ASYM_SysCursor`
- `handle _AutoCloseCheck` — `loc`
- `handle _SetHyperPath` — `bk, what`
- `get _tbk_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _tbk_AddHyperlinktoArray` — `hyperlinks[][] by reference,linkName, pgRef,  transFx, linkType, curs, isURL, vRef`
- `get _tbk_AddLinkToArray` — `hyperlinks[][] by reference, int iRow, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _tbk_BadLinksList` — `fixed hyperlinks[][] by reference`
- `get _tbk_ClearHyperlink` — `obj, linkName`
- `get _tbk_ClearHyperlinkFromArray` — `hyperlinks[][] by reference, linkName`
- `get _tbk_ExecHyperLink` — `fixed hyperlinks[][] by reference, linkName`
- `get _tbk_HyperlinkCandidates` — `obj, candidates[] by reference`
- `get _tbk_HyperlinkLinkInfo` — `hyperlinks[][] by reference, linkName, resolv`
- `get _tbk_HyperlinkIRow` — `STRING linkName, hyperlinks[][] by reference`
- `get _tbk_PopupPage` — `object pgRef, popStyle, pos, captn, curs`
- `get _tbk_SysCursor`
- `get ASYM_AddAnswerHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get ASYM_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get ASYM_AltPgName` — `page obj`
- `get ASYM_ChooseWebBrowser`
- `get ASYM_ClearAnswerHyperlink` — `obj, linkName`
- `get ASYM_ClearHyperlink` — `obj, linkName`
- `get ASYM_CurrentDirectory`
- `get ASYM_CurrentPath`
- `handle ASYM_DisplayURL` — `exeName, url, mode`
- `get ASYM_DoAnswerHyperlink` — `object obj, answerName, IsSpecific`
- `get ASYM_DoHyperlink` — `object obj, triggerName`
- `get ASYM_FindHyperPage` — `pgName, altPgName, bk, isURL, vSymbol`
- `get ASYM_FindHyperWindow` — `vSymbol`
- `get ASYM_FindPage` — `pgN`
- `get ASYM_FindPathFile` — `fName, path, bkPath`
- `get ASYM_GetAnswerHyperlinks` — `obj, linkName`
- `get ASYM_GetHyperlinks` — `obj, linkName`
- `get ASYM_GoToPage` — `pgRef, transfx, curs, isURL`
- `get ASYM_HasHyperlinks` — `obj`
- `get ASYM_HyperPath` — `bk`
- `set ASYM_HyperPath` — `to what`
- `get ASYM_IsFile` — `fName`
- `get ASYM_MakeIntoRelPath` — `rootPath,longPath`
- `get ASYM_MTBVersion` — `dotFlag, options`
- `get ASYM_ProductVersion` — `dotFlag, options`
- `get ASYM_NameOrID` — `obj`
- `get ASYM_ProductPrefix` — `capFlag`
- `get ASYM_RelativePath` — `path, bkName`
- `handle ASYM_ResetCursor`
- `get ASYM_Trim` — `s`
- `handle buttonClick` — `loc`
- `handle extClick` — `loc`
- `handle leaveBook`
- `get tbk_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get tbk_AltPgName` — `page obj`
- `get tbk_ChooseWebBrowser`
- `get tbk_CurrentDirectory`
- `get tbk_CurrentPath`
- `handle tbk_DisplayURL` — `exeName, url, mode`
- `get tbk_DoHyperlink` — `object obj, triggerName`
- `get tbk_FindHyperPage` — `pgName, altPgName, bk, isURL, vSymbol`
- `get tbk_FindPage` — `pgN`
- `get tbk_FindPathFile` — `fName, path`
- `get tbk_GetHyperlinks` — `obj, linkName`
- `get tbk_GoToPage` — `pgRef, transfx, curs, isURL`
- `get tbk_HasHyperlinks` — `obj`
- `get tbk_HyperPath` — `bk`
- `set tbk_HyperPath` — `to what`
- `get tbk_IsFile` — `fName`
- `get tbk_MakeIntoRelPath` — `rootPath,longPath`
- `get tbk_NameOrID` — `obj`
- `get tbk_PopupPage` — `object pgRef, popStyle, pos, captn, curs`
- `get tbk_RelativePath` — `path, bkName`
- `get tbk_trim` — `s`
- `get ASYM_NewRelativePath` — `otherPath, rootPath`
- `get ASYM_ResolvePath` — `filePath`
- `get ASYM_ExpandRelPath` — `otherPath, rootPath`
- `get ASYM_ConvertPathToList` — `path`
- `get ASYM_ConvertListToPath` — `pathList`
- `get tbk_Container` — `obj, objType`
- `handle save`
- `handle saveAs`
- `get ASYM_IsHyperlinkSysBookAdded`
- `get ChooseWebBrowser`
- `handle WriteBrowserIniEntry` — `exeName, sectn, key`
- `get ddeServerName` — `exeName, ddeAppName`
- `handle DisplayURL` — `exeName, url, popup`
- `handle showError` — `errorKey, fn`
- `get ASYM_FindExecutableFile` — `fn`
- `get revOffset` — `s1, s2`
- `get URLSpecialCharsContract` — `s`
- `get URLSpecialCharsExpand` — `s`
- `get FileNameToURL` — `fn`
- `get ASYM_GetTempFile` — `pExt`
- `get ASYM_TempDir`
- `get _ASYM_ChooseFromTextLinesDlg` — `dlgCaption, prompt, txtLines, deflt`
- `handle enterPage`
- `handle Cancel`
- `handle closeThisWindow`
- `handle firstIdle`
- `handle idle`
- `handle OK`
- `set customSize` — `to what`

### `tb90r.sbk`

923 handlers (193 handle, 719 get, 11 set) from 61 type 10 scripts, resource ids 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292.

- `get ASYM_MTBVersion` — `dotFlag, opts`
- `get ASYM_CBTVersion` — `dotFlag, opts`
- `get ASYM_ProductPrefix` — `caps`
- `get ASYM_ProductVersion` — `dotFlag, opts`
- `get ASYM_DisplayableVersion` — `opts`
- `get ASYM_ProductName`
- `get ASYM_RunSysBookName`
- `get ASYMR`
- `handle author`
- `handle buttonClick` — `loc`
- `handle buttonDown` — `loc`
- `handle clear`
- `handle closeWindow`
- `handle destroy`
- `handle enterApplication`
- `handle enterBook`
- `handle enterPage`
- `handle enterSystem`
- `handle enterWindow` — `vRef`
- `handle openWindow`
- `handle keyDown` — `key`
- `handle keyChar` — `x`
- `handle leaveApplication`
- `handle leaveBook`
- `handle leavePage`
- `handle leaveSystem`
- `handle leaveWindow`
- `handle linkSysBook`
- `handle unlinkSysBook`
- `handle mouseEnter`
- `handle mouseLeave`
- `handle newBackground`
- `handle newPage`
- `handle reader`
- `handle rightButtonDown` — `loc, sh, ct`
- `handle rightButtonUp` — `loc`
- `handle sized`
- `handle menuItemSelected`
- `handle ASYM_ResetCursor`
- `get ASYM_IsNumber` — `x`
- `get isNumber` — `x`
- `get ASYM_TextlineOffset` — `x, txt, pos`
- `get onLine`
- `set onLine` — `to val`
- `get ASYM_ItemInList` — `itm,lst`
- `get ASYM_TextlineInText` — `tl, txt`
- `get ASYM_BlockSuspend` — `stckFull`
- `get ASYM_RestoreSuspend` — `opts`
- `get ASYM_CollectWidgets` — `pg`
- `get INFO_CreatedBy`
- `handle ASYM_IAmWidget`
- `get ASYM_Container` — `STRING srcOb, obTypes`
- `handle ASYM_Trigger`
- `handle ASYM_Reset` — `mode, pRef`
- `get ASYM_IniCompanyName`
- `get ASYM_IniUserName`
- `handle ASYM_Idle;` — `end`
- `handle ASYM_BackgroundRightButtonDown;` — `end`
- `handle ASYM_BeginDrag;` — `end`
- `handle ASYM_ObjectDropped;` — `end`
- `handle ASYM_SummonWidgets;` — `end`
- `handle ASYM_PageEntered;` — `end`
- `handle ASYM_Scored;` — `end`
- `handle ASYM_Answered;` — `end`
- `handle ASYM_Changed;` — `end`
- `get ASYM_CMS_GetNextModule`
- `get ASYM_CMS_GotoModule`
- `get ASYM_CMS_IniFile`
- `get ASYM_CMS_MarkAsCompleted`
- `get ASYM_CMS_ModuleFileName`
- `get ASYM_CMS_RecordDetailInfo`
- `get ASYM_CMS_RecordedScore`
- `get ASYM_CMS_RecordScore`
- `get ASYM_CMS_SetNextModule`
- `get sliderMax`
- `set sliderMax` — `to value`
- `get sliderMin`
- `set sliderMin` — `to value`
- `handle sliderMove`
- `get sliderPos`
- `get sliderRatio`
- `set sliderRatio` — `to value`
- `get thumbPosition`
- `set thumbPosition` — `to val`
- `get thumbWidth`
- `set thumbWidth` — `to value`
- `get trackPosition`
- `set trackPosition` — `to v`
- `handle ASYM_SizeButtonToGraphic` — `a`
- `get ASYM_tbdosErrorString` — `a,b`
- `get ASYM_tbfile32ErrorString` — `a`
- `get ASYM_TBDLLErrorString` — `a,b,c`
- `get ASYM_ColorPaletteDlg` — `r,g,b`
- `get ASYM_ChooseColorDlg` — `r,g,b`
- `get ASYM_ChooseFontDlg` — `a,b`
- `get ASYM_OpenFileDlg` — `a,b,c,d,e`
- `get ASYM_OpenFileDlgLFN` — `a,b,c,d,e`
- `get ASYM_SaveAsDlg` — `a,b,c,d,e`
- `get ASYM_ChooseDirectoryDlg` — `a,b`
- `get ASYM_ChooseDirectoryDlgLFN` — `a,b`
- `get ASYM_SaveAsDlgLFN` — `a,b,c,d,e`
- `get ASYM_DuplicateClip` — `clipRef`
- `get ASYM_IsClip` — `STRING nm,bkRef`
- `get _ASYM_SysCursor`
- `get ASYM_WorkingCursor` — `pShow`
- `handle ASYM_ElapsedCursor` — `nmax,n,nm`
- `get ASYM_CursorInResizeHandle`
- `get ASYM_GetResizeTarget` — `pos`
- `get ASYM_CursorSelectionHandle` — `pos, obRef`
- `get ASYM_ClearClipboard`
- `get ASYM_CopyTextToClipboard` — `txt`
- `get ASYM_checkHyperSysBook`
- `get ASYM_EnableHyperlinks`
- `get ASYM_GlossaryPage` — `term,bk`
- `get ASYM_CheckObjectHyperlinks` — `ob`
- `get ASYM_EllipsizeFilenameInText` — `txt, fRef`
- `get ASYM_GetAvailableTextWidth` — `fRef`
- `get ASYM_NumberToRoman` — `num,case,stle`
- `get ASYM_RomanToNumber` — `rom`
- `get ASYM_CompareByCase` — `str1,str2`
- `get revOffset` — `s1,s2`
- `get ASYM_trim` — `s`
- `get trim` — `s`
- `get wordContains` — `x,txt`
- `get wordOffset` — `x,txt`
- `get ASYMA_FindWordStart` — `txt,chr,ln`
- `get ASYM_FindWordStart` — `txt,chr,ln`
- `get ASYM_Offset` — `str,src,pos`
- `get ASYM_ReverseStack` — `STACK stk`
- `get ASYM_StringOf` — `str,cnt`
- `get ASYM_TextlineFromPos` — `pos,txt`
- `get ASYM_SplitWordsOnCaps` — `txt`
- `get ASYM_ExpandEnvironmentStrings` — `str`
- `get ASYM_PathOfFile` — `pth`
- `get ASYM_ShortFileName` — `pth`
- `get ASYM_IsDirectoryWriteable` — `dir`
- `get ASYM_IsDriveReady` — `drv`
- `get ASYM_IsFileAvailable` — `fN`
- `get ASYM_CurrentDirectory`
- `get ASYM_CurrentPath`
- `get ASYM_FindPathFile` — `nm,path,bkPath`
- `get ASYM_FreeDiskSpace` — `dr`
- `get ASYM_GetPath` — `nm`
- `get ASYM_IsDirectory` — `dir`
- `get ASYM_DirectoryExists` — `dir`
- `get ASYM_IsFile` — `fn`
- `get ASYM_RelativePath` — `path,nm`
- `get ASYM_WindowsDirectory`
- `get ASYM_MakeIntoRelPath` — `subPath,bigPath`
- `get ASYM_SetCurrentDirectory` — `path`
- `get ASYM_SetCurrentPath` — `path`
- `get ASYM_SetPath` — `nm,path`
- `get ASYM_TempDir`
- `get ASYM_FindExecutableFile` — `fn`
- `get ASYM_IsAbsoluteFilePath` — `fn`
- `get ASYM_RecurseCreateDirectory` — `dir`
- `get ASYM_ParentDirectory` — `dir`
- `get ASYM_ParsePath` — `path,op`
- `get ASYM_AppendFileToPath` — `dir,fn`
- `get ASYM_ExpandRelPath` — `a,b`
- `get ASYM_ResolvePath` — `filePath`
- `get ASYM_ConvertPathToList` — `path`
- `get ASYM_ConvertListToPath` — `pathList`
- `get ASYM_RecurseRemoveDirectory` — `dir,opts`
- `get ASYM_FindMediaFile` — `fn,bk,srchHD,srchCD,srchHypPath`
- `get ASYM_ExpandMediaPath` — `paths,bk`
- `get ASYM_FileRelativeToMedia` — `fn,bk,srchHD,srchCD,srchHypPath`
- `get ASYM_PromptForCDROM` — `fn,pMessage,cptn`
- `get ASYM_FindFileOnCDROM` — `fn`
- `get ASYM_StandardFolderPath` — `f`
- `get ASYM_FindAnswerIndex` — `itm,col,all`
- `handle ASYM_QLocked` — `ob,resp`
- `handle ASYM_QResponded` — `ob,resp`
- `handle ASYM_TypeInCompleted` — `txt,stat,fld`
- `handle ASYM_CheckDropObj` — `ob,loc`
- `get ASYM_CheckPoint` — `ob,loc,_target`
- `handle ASYM_CheckTries` — `_target`
- `get ASYM_RegisterAttempt` — `_target,mode,showFB,scr`
- `get ASYM_CondensePhonetic` — `s`
- `get ASYM_StripPunctuation` — `txt`
- `handle ASYM_GetTypeInData`
- `get ASYM_MatchString` — `testStr,refStr,byCase,jumbledOK,wildcard,trimText`
- `get ASYM_WID_Responses`
- `get ASYM_BeginResponse` — `ob,nm`
- `handle ASYM_RegisterResponse` — `ob,nm`
- `handle ASYM_WID_Chosen`
- `get ASYM_QuestionStatus` — `ob,_score,mode,noUpdate,showFB`
- `get _ASYM_FindString` — `fixed strgs[][] by reference,nm`
- `get ASYM_GetStandardString` — `nm,dflt`
- `get ASYM_GetString` — `nm,dflt`
- `get ASYMA_GetStringList`
- `get ASYM_AddString` — `nm,s`
- `get ASYM_ClearString` — `nm`
- `get ASYM_ObjectExists` — `STRING ob`
- `get ASYM_FindField` — `fldName,pg`
- `get ASYM_FindPage` — `pgN`
- `get ASYM_GetObjectListByName` — `ob,otype,hasScript,nm`
- `get ASYM_NameOrID` — `ob`
- `get ASYM_ObjectCenter` — `ob`
- `set ASYM_ObjectCenter` — `to loc`
- `get ASYM_OppositePos` — `pos`
- `handle ASYM_ScrollListBoxToSelection`
- `get ASYM_WordFromPoint` — `loc`
- `handle ASYMA_CopyUserProperties` — `obj1,obj2`
- `handle ASYM_FixFieldScrollBar` — `fld`
- `get ASYM_CopyProperty` — `srcRef,destRef,srcProp,destProp`
- `get ASYM_ObjectParentList` — `ob,cutOff`
- `get ASYM_ObjectsWhere` — `ob,objTypes,express`
- `get ASYM_ResolveObject` — `obInfo,ob,srcRef,validate`
- `get ASYM_ResolveBookName` — `bkNm,ob`
- `get ASYM_ResolvePage` — `pgNm,pgID,bkRef,ob`
- `get ASYM_ResolveBackground` — `bgName,bgID,bkRef,ob`
- `get ASYM_FindObject` — `objectType,objectName,objectID,layerRef,ob`
- `get ASYM_ConstructObjectIdentifier` — `ob, srcRef, noSelf, thisPage, layerRef`
- `get ASYM_ObjectDescriptionFromObjectInfo` — `obInfo, srcRef, event, initCaps, ob`
- `get ASYM_RelativeObjectDescription` — `ob, srcRef, initCaps, event`
- `handle ASYM_RegisterPath` — `path, ob`
- `get ASYM_FirstNavigablePage`
- `get ASYM_LastNavigablePage`
- `get ASYM_NextNavigablePage`
- `get ASYM_PreviousNavigablePage`
- `get ASYM_CBTIniVar` — `sxn, key, dflt`
- `handle ASYM_FlushMsgQ`
- `get ASYM_GetSystemVar` — `nm`
- `get ASYM_RandomList` — `cnt, inList`
- `get ASYM_ProductDirectory`
- `get ASYM_LongProductDirectory`
- `get ASYM_SystemDirectory`
- `get ASYM_DrawFocusRect` — `bnds, vRef`
- `get ASYM_DeleteHandler` — `ob, nm`
- `get ASYM_Is32Bit`
- `get ASYM_ScreenInfo`
- `get ASYM_MonitorContaining` — `loc, dflt`
- `get ASYM_MonitorWorkAreaBounds` — `loc, dflt`
- `get ASYM_MonitorBounds` — `loc, dflt, workArea`
- `get ASYM_ScreenBounds` — `loc, dflt, workArea`
- `get ASYM_MonitorHandleList`
- `get ASYM_GetSystemColor` — `nm`
- `get ASYM_GetColorBrightness` — `rgb`
- `get ASYM_PrimaryMouseButton`
- `get ASYM_SetIniCompanyName` — `what`
- `get ASYM_SetIniUserName` — `nm`
- `get ASYM_TicksToTime` — `ms`
- `get ASYM_MouseScreenPos` — `units`
- `get ASYM_FontHeight` — `nm, sz, stle, units`
- `get ASYM_FontWidth` — `nm, sz, stle, units, what, data`
- `get ASYM_CalculateRequiredFieldHeight` — `fRef, lns, htPU`
- `get ASYM_GetScrollInfo` — `hWnd, which`
- `get ASYM_SetScrollInfo` — `hWnd, min, max, pgSize, value, which`
- `get ASYM_SpawnProcess` — `commandLine, showWindow, wait`
- `get ASYM_Copyright`
- `get ASYM_LogSetOptions` — `hdr, pgs, tms, ans, lck, stats`
- `get ASYM_LogStatus`
- `get ASYM_AskStudentName` — `prompt`
- `get ASYM_LogStart` — `bk, fn, appnd, enc, dest, typ`
- `get ASYM_LogStop`
- `get ASYM_LogTypeComboValues`
- `get ASYM_LogWriteEntry` — `txt`
- `get ASYM_LogDispatchComboValues`
- `handle ASYM_MailLogFile` — `fn,a,b,c`
- `handle _ASYM_ResetPgWidgets` — `msg`
- `handle _ASYM_ResetResponseData` — `_target`
- `handle ASYM_Locked`
- `get ASYM_ShortReference` — `ob`
- `get ASYM_ShowDialog` — `vRef, pRef, cptn, mode`
- `handle ASYM_ShowYourScore` — `ob, scr, mode, playFB`
- `get ASYM_WID_Score` — `mode, noUpdate, showFB`
- `get ASYM_CollectTotalScore` — `skp`
- `get ASYM_WID_Correctness` — `ob`
- `handle ASYM_PlayFeedback` — `ind, ob, mode, try`
- `get ASYM_CheckAnswerHyperlinks` — `ob`
- `handle ASYM_DoFeedback` — `ob, num, actualOb`
- `get ASYM_DoGenericTextFeedback` — `ob, tag, pos, option`
- `get ASYM_PlaySoundEffect` — `snd,sync`
- `handle ASYM_PlaySummaryFeedback` — `ob, try`
- `get ASYM_IniFile`
- `get ASYM_GetRuntimeIniVar` — `sxn, nm`
- `get ASYM_SetRuntimeIniVar` — `sxn, nm, val`
- `get ASYM_GetGlobalIniVar` — `sxn, nm`
- `get ASYM_SetGlobalIniVar` — `sxn, nm, val`
- `get ASYM_SetWorkWindow` — `object v`
- `get ASYM_WorkWindow`
- `get ASYM_DisableWindows`
- `get ASYM_EnableWindows` — `val`
- `get ASYM_ViewerContainer` — `ob`
- `handle killUserTooltipTimers`
- `get ASYM_LibrarianUniqueName` — `ob`
- `get ASYM_LibrarianUniqueNameInfo` — `ob, trunc`
- `get ASYM_LibrarianDisplayName` — `ob`
- `get ASYM_LMS_QuestionType`
- `get ASYM_LMS_GetAICCCompatibility` — `ob`
- `get ASYM_LMS_GetAICCSpec20` — `ob`
- `get ASYM_LMS_GetAICCPinnacleCompatibility` — `ob`
- `get ASYM_LMS_GetSCORM_ReportRawScore` — `ob`
- `get ASYM_GetFileDate` — `fn,frmt`
- `get ASYM_AddFileExtension` — `fn, ext`
- `get ASYM_ReplaceFileExtension` — `fn, ext`
- `get ASYM_GetTempFile` — `ext`
- `get ASYM_GetFileVersion` — `fn`
- `get ASYM_GetProductVersion` — `fn`
- `get ASYM_GetShortFileName` — `fn, opt`
- `get ASYM_GetLongFileName` — `fn, opt`
- `get ASYM_ExtensionName` — `ob`
- `get ASYM_FileFromCLSID` — `clsid`
- `get _ASYM_TBKFileVersion` — `fn`
- `get ASYM_FileToPrinter` — `fn, opts, hWnd, showAbort`
- `get ASYM_TextToPrinter` — `txt, opts, hWnd, showAbort`
- `handle ASYM_PrintWindow` — `hWnd, area, opts, xScl, yScl, jobNm, toTop, update, statusB`
- `handle ASYM_SaveWindowToFile` — `hWnd, area, fn, bits, compress, toTop, update, statusB`
- `get ASYM_PopGlossary` — `term, bk, styl, pos, captn, curs`
- `handle ASYM_PopGlossary` — `term`
- `get ASYM_PopupPage` — `object pgRef, popStyle, pos, captn, curs`
- `get ASYM_PopupWinComboValues`
- `handle ASYM_ShowPopupText` — `txt, pos`
- `handle ASYM_HidePopupText`
- `get ASYM_CompareDates` — `d1, d2, fmt`
- `get ASYM_DateToSeconds` — `d, fmt`
- `get ASYM_MillisecondsToTime` — `ms`
- `get millisecondsToTime` — `ms`
- `handle ASYM_PostMsg` — `msg, tgt`
- `handle ASYM_DoPostedMsg` — `msg, tgt`
- `get ASYM_IsMsgPosted` — `msg, tgt`
- `get ASYM_SetPostMsgBlock` — `pNewValue`
- `get ASYM_FlushPostMsgQueue`
- `get ASYM_Ellipsize` — `s, len, side`
- `get ASYM_EllipsizeFileToField` — `fld, file, fileOpt, dirOpt`
- `handle ASYM_LinkDLLs`
- `get ASYM_AskForPath` — `startPath, dbCaption`
- `get ASYM_WinHelp` — `cn, file`
- `get ASYM_IsWin31`
- `get ASYM_PopRTFHelp` — `fN, captn`
- `get ASYM_Wait` — `ms, breakKeys, yield`
- `get ASYM_Sleep` — `pMs`
- `get ASYM_UpdateTargetObject` — `ob`
- `get ASYM_DoProgressSingle` — `a,b,c,d,e,f`
- `get ASYM_DoProgressDouble` — `a,b,c,d,e,f,g,h,i`
- `handle ASYM_ShowProgress` — `n, maxN, captn`
- `handle ASYM_ShowProgressWithText` — `txt, n, maxN, captn`
- `handle ASYM_OpenEndedProgress` — `txt`
- `handle ASYM_ShowError` — `txt, winCaption, helpTag, helpFile`
- `get ASYM_ModalDialog` — `whatPage, whatCaption`
- `set ASYM_ModalState` — `to what`
- `get ASYM_MessageBox` — `txt,captn,icn,btns,hlpTag,hlpFile`
- `get asym_ask` — `cptn,txt,icn,btns,defTxt,width,pos,frm,chk,rdio,hlp`
- `get asym_request` — `cptn,txt,icn,btns,width,pos,frm,chk,rdio,hlp`
- `get ASYM_PopMenu` — `menuItemList, pos, rect`
- `get ASYM_INET_linkDLL`
- `get ASYM_GetFile_URL` — `rmtFn, locFn, overwrite, secSock`
- `get ASYM_GetFile_FTP` — `rmtSrv,rmtPrt,rmtDir,rmtFn,rmtUsr,rmtPW,locFn,overwrite,transType`
- `get ASYM_ActionsRuntimeLinked`
- `get ASYM_Media_PlayerTable`
- `get ASYM_Media_PlayerIndexFromKey` — `key, val`
- `get ASYM_Media_FileIndexFromKey` — `key, val`
- `get ASYM_Media_PlayerInfo` — `idx, key`
- `get ASYM_Media_FileInfo` — `idx, key`
- `get ASYM_Media_MediaFilterList`
- `get ASYM_Media_PlayerIndex` — `fName, desc`
- `get ASYM_Media_FileIndex` — `fName`
- `get ASYM_Media_PlayerName` — `fName, desc`
- `get ASYM_Media_TimeFormat` — `fName`
- `get ASYM_Media_VideoSupport` — `fName, desc`
- `get ASYM_Media_ControlSupport` — `fName, desc`
- `get ASYM_GetDataElement` — `STACK data, STRING key, STRING dflt, validate`
- `get ASYM_SetDataElement` — `STACK data, STRING key, STACK val, validate`
- `get ASYM_GetStructureName` — `STACK data, validate`
- `get ASYM_GetElementList` — `STACK data`
- `get ASYM_SetStructureName` — `STACK data, val`
- `get ASYM_ForEachInit` — `STACK data, validate`
- `get ASYM_ForEachNext` — `structureID`
- `get ASYM_ForEachRelease` — `structureID`
- `get ASYM_NewDataStructure` — `nm`
- `get ASYM_IsDataStructure` — `STACK data`
- `get ASYM_ListToStack` — `STRING pList`
- `get ASYM_ArrayPropertyDataType` — `ob,prop`
- `get ASYM_InternationalFile` — `fn, validate`
- `get ASYM_QuickSortList` — `lst, asText`
- `get ASYM_QuickSortArray` — `lst[] by reference, txt`
- `get ASYM_QuickSortTable` — `lst[][] by reference, srtOrder, srtType`
- `handle ASYM_SyncTextValueWithList` — `ob, STRING txt, exact`
- `handle ASYM_SyncNumericValueWithList` — `ob, txt, exact`
- `handle ASYM_EnsureTextlineVisible` — `ob, ln`
- `get puToInches` — `pu`
- `get inchesToPU` — `inches`
- `get ASYM_PageUnitsToStandardUnits`
- `get ASYM_StandardUnitsToPageUnits` — `val, noRound`
- `get ASYM_GreatestCommonDivisor`
- `get ASYM_GreatestCommonDivisorArray` — `n[] by reference`
- `get ASYM_SelectObjectTarget` — `a,b,c,d,e,f,g,h,i`
- `get ASYM_SelectObjectFromList` — `obList, selType, cptn`
- `get ASYM_ObjectBitmapGroup` — `thisObj`
- `handle _ASYM_ReaderExit`
- `get ASYM_AltPgName` — `page ob`
- `get ASYM_ChooseFromTextLinesDlg` — `a,b,c,d,e`
- `get ASYM_decode` — `src, pw, ver`
- `get ASYM_HasAnsArray` — `ob`
- `get ASYM_HasFBArray` — `ob`
- `get ASYM_IsPointClose` — `a,b,c`
- `get ASYM_SuperEncode` — `txt, pwd`
- `get ASYM_GetDeploymentMethod` — `ob`
- `get ASYM_GetParameter` — `nm`
- `get getParameter` — `nm`
- `get ASYM_SetHTTPPostParameter` — `nm, val`
- `get ASYM_HTTPPost` — `url`
- `get httpPost` — `url`
- `get ASYM_IsObjectDirty` — `ob, bit`
- `get ASYM_IsObjectClean` — `ob, bit`
- `get ASYM_SetObjectClean` — `ob, bit`
- `get ASYM_IsPageDirty` — `whichPg, bit, bk`
- `get ASYM_IsPageClean` — `whichPg, bit, bk`
- `get ASYM_ReturnCleanPages` — `pgList, bit, bk`
- `get ASYM_ReturnDirtyPages` — `pgList, bit, bk`
- `get ASYM_SetPageClean` — `whichPg, bit, bk`
- `get ASYM_DisableBackup`
- `get ASYM_RestoreBackup`
- `handle ASYM_TimeMarker`
- `get ASYM_IsInstanceActive`
- `get TBK_Assert` — `cond, fatal, loc, str, r1, r2, r3, r4`
- `get ASYM_ItemOffset` — `itm, lst`
- `get ASYM_ItemContains` — `itm, lst`
- `get ASYM_ModalPopText` — `ttl, txt, pt`
- `get ASYM_CreateEncryptedFile` — `a,b`
- `get ASYM_CreateEncryptedFileEX` — `a,b,c`
- `get ASYM_WriteEncryptedFile` — `a,b,c`
- `get ASYM_GetMemBlock` — `a`
- `get ASYM_FreeMemBlock` — `a`
- `get ASYM_DecodeEX` — `a,b,c`
- `get ASYM_Encode` — `a,b`
- `get ASYM_EncodeEX` — `a,b,c`
- `handle _linkDLLs`
- `handle _linkSysBook`
- `handle _doNeuronCheck`
- `handle _unLinkSysBook`
- `handle initSysBooks`
- `get SetSysBooksInOrder` — `bkFnList`
- `get shortFileName` — `fName`
- `get _ASYM_Ellipsize` — `s, len, side`
- `get _ASYM_EllipsizeFileToField` — `pField, pFileName, pFileOpt, pDirOpt`
- `handle cleanupDuplicateSysbooks`
- `handle _enterApplication` — `targetRef`
- `handle _leaveApplication`
- `handle _CMS_EnterApplication` — `bk, bookmarkFn`
- `get blockSuspend` — `stckFull`
- `get restoreSuspend` — `opts`
- `get _ASYM_TBDLLErrorString` — `pDLL, pFunctionName, pErrorCode`
- `get _ASYM_PopupPage` — `object pgRef, popStyle, pos, captn, curs, fx`
- `get _ASYM_PopupWinComboValues`
- `handle _AutoCloseCheck` — `loc`
- `get viewerScript`
- `get _FindExecutableFile` — `fn`
- `get _ASYM_IsDirectoryWriteable` — `dirSpec`
- `get _ASYM_IsDriveReady` — `drv`
- `get _ASYM_IsFileAvailable` — `fN`
- `get _ASYM_MakeIntoRelPath` — `rootPath,longPath`
- `get _ASYM_SetCurrentDirectory` — `pathStr`
- `get _ASYM_SetPath` — `pathName, path`
- `get _ASYM_IsValidDrive` — `path, retry, prompt`
- `get _ASYM_CurrentDirectory`
- `get _ASYM_FindPathFile` — `fName, path, bkPath`
- `get _ASYM_FreeDiskSpace` — `drspec`
- `get _ASYM_GetPath` — `pathName`
- `get _ASYM_IsDirectory` — `dirspec`
- `get _ASYM_RelativePath` — `path, bkName`
- `get _ASYM_WindowsDirectory`
- `get _ASYM_IsAbsoluteFilePath` — `pFileName`
- `get _ASYM_RecurseCreateDirectory` — `dir`
- `get _ASYM_ParentDirectory` — `dir`
- `get _ASYM_ParsePath` — `path, op`
- `get ASYM_FileDotPosition` — `fileName`
- `get _ASYM_AppendFileToPath` — `dir, fn`
- `get _ASYM_ExpandRelPath` — `otherPath, rootPath`
- `get _ASYM_ResolvePath` — `filePath`
- `get _ASYM_ConvertPathToList` — `path`
- `get _ASYM_ConvertListToPath` — `pathList`
- `get _ASYM_RecurseRemoveDirectory` — `dir, options`
- `get _ASYM_FindMediaFile` — `pFilename, pBook, pSearchHD, pSearchCD, pSearchHyperPath`
- `get _ASYM_ExpandMediaPath` — `pPaths, pBook`
- `get _ASYM_FileRelativeToMedia` — `pFilename, pBook, pSearchHD, pSearchCD, pSearchHyperPath`
- `get _ASYM_PromptForCDROM` — `pFilename, pMessage, pCaption`
- `get _ASYM_FindFileOnCDROM` — `pFilename`
- `get _ASYM_PathOfFile` — `pPath`
- `get _ASYM_ShortFileName` — `pPath`
- `get _ASYM_TempDir`
- `get _ASYM_ExpandEnvironmentStrings` — `str`
- `get standardFolder` — `folderName`
- `get playerKeyList`
- `get fileKeyList`
- `get playerTable`
- `get fileTable`
- `handle addArrayItem` — `itemArray[][] by reference`
- `get playerIndexFromKey` — `pInfoKey, pValue`
- `get fileIndexFromKey` — `pInfoKey, pValue`
- `get indexFromKey` — `pInfoKey, pValue, mediaTable[][] by reference, nameKeys`
- `get playerInfo` — `pIndex, pInfoKey`
- `get fileInfo` — `pIndex, pInfoKey`
- `get mediaInfo` — `pIndex, pInfoKey, mediaTable[][] by reference, nameKeys`
- `get mediaFilterList`
- `get playerIndex` — `fName, playerDesc, targetRef`
- `get fileIndex` — `fName, targetRef`
- `get playerName` — `fName, playerDesc, targetRef`
- `get timeFormat` — `fName, targetRef`
- `get videoSupport` — `fName, playerDesc, targetRef`
- `get controlSupport` — `fName, playerDesc, targetRef`
- `handle disableTaskSwitching` — `how`
- `handle _WM_SYSCOMMAND` — `hWnd, wMsg, wp, lp`
- `handle _sized` — `sizedObj, tbk_wid_type`
- `handle _ASYM_SizeButtonToGraphic` — `pTarget, pObj`
- `get isPointClose` — `p1,p2, dist`
- `get _ASYM_MakeBookmarkFileName`
- `get _readBookmarks` — `bookmarkFn`
- `get _writeBookmarks` — `bookmarkFn`
- `get readNextLine` — `fN`
- `get _AskStudentName` — `prompt`
- `handle _ASYM_CollectLogResponseData` — `sep`
- `get _ASYM_LogDispatchDirectory` — `LogDest`
- `get _ASYM_LogStart` — `bk, fName, logAppend, encryptIt, dest, typ, CMSLogFileName, CMSLogFileType`
- `get _ASYM_LogStop`
- `get _ASYM_LogTypeComboValues`
- `get _ASYM_MakeLogFileName` — `dest, logFn`
- `get IsRoomOnDisk` — `d`
- `get _ASYM_LogWriteEntry` — `txt`
- `get _ASYM_LogSetOptions` — `heading, logPages, logTimes, logAnswers, logOnLock, logStats`
- `get _ASYM_LogStatus`
- `get _ASYM_decode` — `source, password, ver`
- `handle _ASYM_LogDispatch` — `LogFileName, LogDest,\`
- `get _ASYM_LogDispatchComboValues`
- `handle _ASYM_MailLogFile` — `LogFileName, EmailLogRecipients,\`
- `get getMAPIErrorString` — `nErrorNumber`
- `get IsMAPIAvailable`
- `handle linkMAPI`
- `get logPrintDefaults`
- `handle mailDriverError` — `fName, EmailLogRecipients`
- `handle mailSendError` — `fName, EmailLogRecipients`
- `handle RequestDeleteTempFile` — `fN, titl`
- `handle ConfirmLogMailedOK` — `fN, titl, bConfirm`
- `get sendFile` — `fileName`
- `get SessionLogOff`
- `get SessionLogOn`
- `handle showLogMailError` — `fName, EmailLogRecipients`
- `get str_OK`
- `get ASYM_MAPISendMessage` — `recips,subject,msgText,attachments`
- `get _ASYM_FindFaxDriver`
- `get SendLogAsFax` — `fN, printdefaults, faxDevice`
- `handle AutoGlossary` — `hotWrd`
- `handle autoHotword` — `fld, loc`
- `get _asym_IsWin31`
- `get _ASYM_WinHelp` — `what, whatFile`
- `get _ASYM_AddString` — `strgName, s, tgt`
- `get _ASYM_ClearString` — `strgName, tgt`
- `get __ASYM_FindString` — `fixed strgs[][] by reference, strgName`
- `get _ASYM_GetStandardString` — `pTarget, strgName, strgDflt`
- `get _ASYM_GetString` — `pTarget, strgName, strgDflt`
- `get _ASYMA_GetStringList` — `pTarget`
- `get GetStringTargetBook` — `pTarget`
- `get _ASYM_Wait` — `ms, breakKeys, yield`
- `get _ASYM_Sleep` — `pMs`
- `get _ASYM_CompareDates` — `d1, d2, fmt`
- `get _ASYM_DateToSeconds` — `d, fmt`
- `get _ASYM_MillisecondsToTime` — `ms`
- `get _ASYM_FileToPrinter` — `fn, options, hParentWnd, showAbortDlg`
- `get _ASYM_TextToPrinter` — `txt, options, hParentWnd, showAbortDlg`
- `get cleanUpText` — `pText`
- `get PrintBand` — `hDC, lpRectOut, lpRectClip, lpDIBHdr, lpDIBBits`
- `get PrintDIB` — `hDib, fPrintOpt, wXScale, wYScale, szJobName`
- `handle printWindow` — `hWnd, wPrintArea, wPrintOpt, wXScale, wYScale, szJobName, toTop, update, statusB`
- `get doPrintWindow` — `hWnd, wPrintArea, wPrintOpt, wXScale, wYScale, szJobName`
- `get CalculatePrintRect` — `hDC, lpPrintRect, fPrintOpt, cxDIB, cyDIB`
- `get CopyWindowToDIB` — `hWnd, fPrintArea, bitCount, Compress`
- `get CopyScreenToDIB` — `lpRect, bitCount, Compress`
- `get CopyScreenToBitmap` — `lpRect`
- `get BitmapToDIB` — `hBitmap, hPal, bitCount, Compress`
- `get FindDIBBits` — `lpDIB`
- `get DIBNumColors` — `lpDIB`
- `get GetSystemPalette`
- `get PalEntriesOnDevice` — `hDC`
- `get PaletteSize` — `lpDIB`
- `get SaveDIBToFile` — `hDib, lpFileName`
- `get DIBError` — `ErrNo`
- `get getViewerName` — `whatViewer`
- `handle linkDlls`
- `handle saveWindowToFile` — `hWnd, wPrintArea, FileName, bitCount, compress, toTop, update, statusB`
- `get doSaveWindow` — `hWnd, printArea, fileName, bitCount, compress`
- `get GetPrinterDC` — `forPrinter   --32`
- `get _ASYM_IsObjectDirty` — `obRef, whichBit`
- `get _ASYM_IsObjectClean` — `obRef, whichBit`
- `get _ASYM_IsPageDirty` — `whichPg,whichBit,whichBk`
- `get _ASYM_IsPageClean` — `whichPg,whichBit,whichBk`
- `get _ASYM_ReturnCleanPages` — `pgList,whichBit,whichBk`
- `get _ASYM_ReturnDirtyPages` — `pgList,whichBit,whichBk`
- `get _ASYM_SetObjectClean` — `obRef, whichBit`
- `get _ASYM_SetPageClean` — `whichPg,whichBit,whichBk`
- `get modBit` — `whichBit`
- `get getDirtyBitsObject` — `obRef`
- `get _ASYM_GetParameter` — `paramName`
- `get replaceEscapeChars` — `txt`
- `get _ASYM_SetHTTPPostParameter` — `paramName, paramValue`
- `get _ASYM_HTTPPost` — `url`
- `get escapeChars` — `txt`
- `handle _ASYM_PostMsg` — `msg, tgt`
- `handle _ASYM_DoNextPostedMsg`
- `handle _ASYM_DoPostedMsg` — `hWnd, msgID`
- `get _ASYM_IsMsgPosted` — `msg, tgt`
- `get _ASYM_SetPostMsgBlock` — `pNewValue`
- `get _ASYM_FlushPostMsgQueue`
- `handle _ASYM_FlushMsgQ`
- `handle _ASYM_Reset` — `targetRef, mode, pResetTargetPage`
- `handle _ASYM_ResetPgWidgets` — `msg, setBeenHere`
- `handle sizeButtonToGraphic` — `obj`
- `handle _ASYM_Locked` — `_target`
- `handle _ASYM_ResetRespData` — `_target`
- `handle _ASYM_ResetTestItem` — `QType, mode, _target`
- `get _ASYM_ShortReference` — `obj`
- `get _ASYM_ShowDialog` — `whatViewer, whatPage, whatCaption, whatMode`
- `handle _fixAnsArray` — `obj`
- `handle ASYM_QuestionLoad` — `mode, index, _target`
- `get ASYM_CleanState` — `pageRef`
- `set ASYM_CleanState` — `pageRef to cleanState`
- `get _ASYM_WID_Responses` — `obj`
- `get _ASYM_BeginResponse` — `actualObj, respName, _target, resetToOld`
- `get _ASYM_CheckPoint` — `obj, loc, _target`
- `handle _ASYM_GetTypeInData` — `_target`
- `handle _ASYM_RegisterResponse` — `actualObj, respName, _target`
- `handle _moveObj` — `obj, _target`
- `get testExpressionWithX` — `expr, x`
- `get ASYM_cepr` — `s`
- `get ASYM_matchString` — `STRING testString, STRING refString, \`
- `get ASYM_SoundsLike` — `s1, s2`
- `get ASYM_stripPunctuation` — `whatText`
- `get defaultPhRules`
- `get defaultPhVowels`
- `handle LockAndAdjustTestItem` — `_target, actualObj, respName, QType`
- `get matchJumbledWords` — `STRING testString, ARRAY wrdList[],LOGICAL byCase`
- `get SetElapsedTime` — `_target, newTimeChosen`
- `get _cleanUp` — `txt`
- `handle _ASYM_CheckDropObj` — `pTarget, obj, loc`
- `get _ASYM_RegisterAttempt` — `pTarget, _target, mode, showFeedback, correctness, score`
- `handle _ASYM_CheckTries` — `pTarget, _target`
- `get _ASYM_FindAnswerIndex` — `pTarget, whatItem, col, all`
- `handle _ASYM_QLocked` — `obj, response`
- `handle _ASYM_QResponded` — `obj, response`
- `handle _ASYM_TypeInCompleted` — `pTarget, txt, stat, entryField`
- `get _ASYM_QuestionStatus` — `pTarget, obj, _score, mode, noUpdate, showFeedback`
- `handle handleButtonDown` — `loc, targetRef`
- `get _ASYM_DoGenericTextFeedback` — `obj, tag, pos, option`
- `get _ASYM_PlayAnswerFeedback` — `answerIndex, obj, actualObj`
- `get _ASYM_PlaySummaryFeedback` — `obj, actualObj, registerTry`
- `get _PlayFeedbackItem` — `fbArray[][] by reference, num, obj, actualObj, notSummary`
- `get _upgrade3SummaryFeedback` — `obj`
- `handle mmnotify` — `clipRef, cmd, result`
- `get _SmartPlaySound` — `snd, sync`
- `get _ASYM_CheckAnswerHyperlinks` — `obj`
- `handle _ASYM_PlayFeedback` — `pTarget, index, actualObj, mode, pRegisterTry`
- `handle ASYM_ShowYourScore` — `obj, score, mode, playFB, _target`
- `handle _ASYM_ShowYourScore` — `obj, score, mode, playFeedback, _target`
- `get _ASYM_WID_Correctness` — `_target`
- `get _ASYM_WID_Score` — `_target, mode`
- `get _ASYM_CollectTotalScore` — `includeSkip`
- `handle DoDragObject` — `tgt, obj, loc, whatButton`
- `handle DoMatchItemDrag` — `tgt, obj, loc, whatButton`
- `get _UpdateTargetObject` — `obj`
- `get _ASYM_Is32Bit`
- `get monitorContaining` — `where, defaultMonitor`
- `get monitorBounds` — `where, defaultMonitor, workArea`
- `get getPrimaryMonitorBounds` — `workArea`
- `get ScreenInfo`
- `get getSystemColor` — `sysColor`
- `get getColorBrightness` — `rgbColor`
- `get primaryMouseButton`
- `get setIniCompanyName` — `what`
- `get setIniUserName` — `what`
- `get ticksToTime` — `ms`
- `get mouseScreenPos` — `pReturnType`
- `get calculateRequiredFieldHeight` — `fRef, numLines, fontHeightTwips`
- `get fontHeight` — `fontName, fontHeightPoints, fontInfo, units`
- `get guessFontHeight` — `fontHeightPoints`
- `get fontWidth` — `fontName, fontHeightPoints, fontInfo, units, what, data`
- `get getScrollInfo` — `hWnd, which`
- `get setScrollInfo` — `hWnd, min, max, pgSize, value, which`
- `get monitorHandleList` — `pos, monitorList`
- `get SpawnProcess` — `commandLine, showWindow, wait`
- `get SpawnProcessAsynch` — `commandLine, showWindow`
- `get _ASYM_CBTIniVar` — `section, key, deflt`
- `get _ASYM_GetSystemVar` — `varName`
- `get _ASYM_RandomList` — `numItems, inList`
- `get _ASYM_ProductDirectory`
- `get _ASYM_LongProductDirectory`
- `get _ASYM_SystemDirectory`
- `get _ASYM_DrawFocusRect` — `pBounds, pViewer`
- `get _ASYM_DeleteHandler` — `obRef, handlerName`
- `get _ASYM_DisableBackup`
- `get _ASYM_RestoreBackup`
- `get _ASYM_GetDeploymentMethod` — `ob`
- `get _ASYM_MessageBox` — `txt, titl, icn, btns, hlpTag, hlpFile`
- `handle F1Pressed`
- `get _ASYM_ColorPaletteDlg` — `r, g, b`
- `get _ASYM_chooseColorDlg` — `r, g, b`
- `get _ASYM_ChooseFontDlg` — `a, b`
- `get _ASYM_OpenFileDlg` — `a, b, c, d, e`
- `get _ASYM_OpenFileDlgLFN` — `a, b, c, d, e`
- `get _ASYM_SaveAsDlg` — `a, b, c, d, e`
- `get _ASYM_ChooseDirectoryDlg` — `a, b`
- `get _ASYM_ChooseDirectoryDlgLFN` — `a, b`
- `get _ASYM_SaveAsDlgLFN` — `a, b, c, d, e`
- `get _ASYM_LockWindows`
- `get _ASYM_UnlockWindows` — `winDetails`
- `get __ASYM_SysCursor`
- `get _ASYM_WorkingCursor` — `pShow`
- `get _ASYM_CursorInResizeHandle`
- `handle _ASYM_ElapsedCursor` — `nmax, n, curName`
- `get getResizeTarget` — `pos`
- `get cursorSelectionHandle` — `pos, obRef`
- `get midPoint` — `p1, p2, px`
- `get selectionHandleRect` — `x, y`
- `get pointInRect` — `pt, rect`
- `get ASYM_DuplicateClip` — `clipRef`
- `get ASYM_IsClip` — `STRING pClip, pTargetBook`
- `get _ASYM_ViewerContainer` — `pObjRef`
- `get _ASYM_SetWorkWindow` — `object v`
- `get _ASYM_WorkWindow`
- `get _ASYM_DisableWindows`
- `get _ASYM_EnableWindows` — `val`
- `handle showToolbar`
- `handle showColorTray`
- `get _ASYM_ClearClipboard`
- `get _ASYM_CopyTextToClipboard` — `clipText`
- `get _ASYM_checkHyperSysBook`
- `get _ASYM_EnableHyperlinks`
- `get _ASYM_GlossaryPage` — `term, bkName`
- `get _ASYM_NumberToRoman` — `num, case, formatStyle`
- `get _ASYM_RomanToNumber` — `rom`
- `get _ASYM_CompareByCase` — `string1, string2`
- `get _revOffset` — `s1, s2`
- `get _ASYM_Trim` — `s`
- `get _wordContains` — `x, txt`
- `get _wordOffset` — `x, txt`
- `get _ASYM_FindWordStart` — `whatText, whatChar, whatLine`
- `get _ASYM_Offset` — `str, src, pos`
- `get _ASYM_ReverseStack` — `STACK stk`
- `get _ASYM_StringOf` — `str, cnt`
- `get _ASYM_TextlineFromPos` — `pPos, pText`
- `get _ASYM_SplitWordsOnCaps` — `txt`
- `get ASYM_EllipsizeFilenameInText` — `txt, fRef`
- `get ASYM_GetAvailableTextWidth` — `fRef`
- `get _ASYM_FindField` — `fldName, pg`
- `get _ASYM_FindPage` — `pgN`
- `get _ASYM_GetObjectListByName` — `oContainer, otype, hasScript, nam`
- `get _ASYM_NameOrID` — `obj`
- `get _ASYM_ObjectCenter` — `pTarget, obj`
- `handle _ASYM_SetObjectCenter` — `pTarget, loc`
- `get _ASYM_OppositePos` — `pos`
- `handle _ASYM_ScrollListBoxToSelection` — `pTarget`
- `get _ASYM_WordFromPoint` — `loc`
- `handle _ASYMA_CopyUserProperties` — `obj1, obj2`
- `handle _ASYM_FixFieldScrollBar` — `pTarget, fld`
- `get _ASYM_CopyProperty` — `pSourceObj, pDestObj, pSourceProp, pDestProp`
- `get _ASYM_ObjectParentList` — `pObj, pCutOffLevel`
- `get ASYM_ConstructObjectIdentifier` — `objectRef, targetRef, noSelf, thisPage, layerRef`
- `get ASYM_ObjectDescriptionFromObjectInfo` — `obInfo, selfRef, event, initCaps, obRef`
- `get ASYM_ResolveObject` — `objectInfo, selfRef, targetRef, validate`
- `get ASYM_ResolveBookName` — `bookName, targetRef`
- `get ASYM_ResolvePage` — `pageName, pageID, bookRef, targetRef`
- `get ASYM_ResolveViewer` — `viewerName, viewerID, bookRef, targetRef`
- `get ASYM_ResolveBackground` — `bgName, bgID, bookRef, targetRef`
- `get ASYM_FindObject` — `objectType, objectName, objectID, layerRef, targetRef`
- `get ASYM_RelativeObjectDescription` — `targetRef, selfRef, initCaps, event`
- `handle ASYM_RegisterPath` — `path, targetRef`
- `get _ASYM_ObjectsWhere` — `ownerObj, objTypes, express`
- `get _ASYM_LMS_UniqueName` — `obRef`
- `get _ASYM_LMS_UniqueNameInfo` — `obRef, truncateFlag`
- `get _ASYM_LMS_DisplayName` — `obRef`
- `get _ASYM_LMS_QuestionType` — `obj`
- `get getAICCCompatibility` — `ob`
- `get getAICCSpec20` — `ob`
- `get getAICCPinnacleCompatibility` — `ob`
- `get getSCORM_ReportRawScore` — `ob`
- `get _ASYM_GetFileDate` — `fName, formatString`
- `get _ASYM_AddFileExtension` — `fn, ext`
- `get _ASYM_ReplaceFileExtension` — `fn, ext`
- `get _ASYM_GetFileVersion` — `fName, productFlag`
- `get _ASYM_GetTempFile` — `pExt`
- `get _ASYM_GetShortFileName` — `fName, opt`
- `get _ASYM_GetLongFileName` — `fName, opt`
- `get _ASYM_ExtensionName` — `ob`
- `get _ASYM_FileFromCLSID` — `pCLSID`
- `get _ASYM_PopMenu` — `menuItemList, pos, rect`
- `get buildMenu` — `menuItemList, vRef, hMenu, pMenuItemInfo, pMenuText, delimitByCRLF, parentItem`
- `get _ASYM_INET_linkDLL`
- `get _ASYM_GetFile_URL` — `pRemoteFile, pLocalFile, pOverWrite, pSecureSocket`
- `get _ASYM_GetFile_FTP` — `pRemoteServer, pRemotePort, pRemoteDir, \`
- `get INetNotifyResolvingName` — `pAlias, pName`
- `get INetNotifyNameResolved` — `pAlias, pName`
- `get INetNotifyConnecting` — `pAlias`
- `get INetNotifyConnected` — `pAlias`
- `get INetNotifySending` — `pAlias, pRequestHeaders`
- `get INetNotifySent` — `pAlias`
- `get INetNotifyReceivingResponse` — `pAlias`
- `get INetNotifyReceivedResponse` — `pAlias, pResponseHeaders, DWORD pBytesReceived`
- `get INetNotifyClosingConnection` — `pAlias`
- `get INetNotifyClosedConnection` — `pAlias`
- `get INetNotifyRequestComplete` — `pAlias`
- `get INetNotifyCopyProgress` — `pAlias, DWORD pBytesCopied, DWORD pTotalBytesToCopy`
- `get INetNotifyCopyComplete` — `pAlias, DWORD pBytesCopied`
- `get ASYM_SetDataElement` — `stack dataStructure, string elementName, stack elementValue, validate`
- `get ASYM_GetDataElement` — `stack dataStructure, string elementName, defaultValue, validate`
- `get ASYM_GetElementList` — `STACK dataStructure`
- `get ASYM_GetStructureName` — `STACK dataStructure, validate`
- `get ASYM_IsDataStructure` — `STACK dataStructure`
- `get ASYM_GetDataElement_Old` — `STACK dataStructure, STRING key, STRING default`
- `get ASYM_SetDataElement_Old` — `STACK dataStructure, STRING key, STRING value`
- `get ASYM_GetStructureName_Old` — `STACK dataStructure`
- `get ASYM_SetStructureName` — `STACK dataStructure, value`
- `get ASYM_SetStructureName_Old` — `STACK dataStructure, value`
- `get ASYM_GetElementList_Old` — `STACK dataStructure`
- `get ASYM_ExpandSpecialChars` — `STRING txt`
- `get ASYM_ReplaceSpecialChars` — `STRING txt`
- `get ASYM_Offset` — `str, src, pos`
- `get ASYM_ForEachInit` — `STACK dataStructure, validate`
- `get ASYM_ForEachNext` — `structureID`
- `get ASYM_ForEachRelease` — `structureID`
- `get ASYM_ListToStack` — `STRING pList`
- `get _asym_ArrayPropertyDataType` — `obj, prop`
- `get typeDataCheck` — `obj, prop, curType, dims`
- `get _ASYM_InternationalFile` — `pFileName, pValidateFile`
- `get ASYM_QuickSortArray` — `lst[] by reference, asText`
- `get ASYM_QuickSortTable` — `lst[][] by reference, sortOrder, sortType`
- `get compare` — `val1, val2, datatype`
- `get ASYM_QuickSortList` — `lst, asText`
- `get quickSort` — `data[] by reference, STACK lStack, STACK rStack`
- `get quickSortText` — `data[] by reference, STACK lStack, STACK rStack`
- `handle _ASYM_SyncTextValueWithList` — `FIELD fRef, STRING testText, exactFit`
- `handle _ASYM_SyncNumericValueWithList` — `FIELD fRef, testText, exactFit`
- `handle _ASYM_EnsureTextlineVisible` — `FIELD fRef, currentLine`
- `get _ASYM_PageUnitsToStandardUnits`
- `get _ASYM_StandardUnitsToPageUnits` — `value, noRounding`
- `get gcd` — `nums[] by reference`
- `get tooltip` — `targetRef`
- `handle doToolTip` — `targetRef`
- `handle timerNotify` — `timerID`
- `handle showTooltip`
- `get getTooltipInfo`
- `handle hideTooltip` — `targetRef`
- `handle _killTooltipTimers`
- `handle ASYM_ShowPopupText` — `txt, pos`
- `handle buttonClick`
- `handle ASYM_HidePopupText`
- `handle resizeField` — `obj, fixedWidth, minWidth, maxWidth, textRightMargin`
- `get repairFieldWidth` — `obj, min, max`
- `get repairFieldHeight` — `obj, maxHeight`
- `handle ASYM_Reset`
- `get htmlToRichText` — `txt`
- `handle setRichText` — `obRef, txt`
- `get doProgress` — `mainCaption, progressCaption, progressValue, progressMax, viewerCaption, noCancel`
- `get checkCancel` — `vRef`
- `handle ASYM_Reset`
- `get doProgress` — `mainCaption, progress1Caption, progress1Value, progress1Max, progress2Caption, progress2Value, progress2Max, viewerCaption, noCancel`
- `get checkCancel` — `vRef, cancelRef`
- `get _ASYM_ChooseFromTextLinesDlg` — `dlgCaption, prompt, txtLines, deflt, helpTopicOrID`
- `handle enterPage`
- `handle Cancel`
- `handle closeThisWindow`
- `handle firstIdle`
- `handle idle`
- `handle OK`
- `set customSize` — `to what`
- `handle ASYM_Reset`
- `get _asym_ask_request` — `_caption, _text, _icon, _buttons, _type, _defText, _width, _position, _frame, _check, _radio, _help`
- `get stripSpecial` — `str, lst`
- `get findSpecial` — `str, lst`
- `handle resizeButtons`
- `get XpixelToPU` — `val`
- `get YpixelToPU` — `val`
- `handle resizeField` — `obj, fixedWidth, minWidth, maxWidth, textRightMargin`
- `get repairFieldWidth` — `obj, min, max`
- `get repairFieldHeight` — `obj, maxHeight`
- `get myPage`
- `get parseButtons` — `_buttons`
- `get screenWidth`
- `get screenHeight`
- `handle Paste`
- `get mnemonicChar` — `str`
- `handle keyChar` — `key`
- `handle buttonClick`
- `handle keyDown` — `key`
- `get moveDefRect` — `object defRect, object obj`
- `get hideDefRect`
- `get resetRect` — `object oldObj`
- `get createDefRect` — `logical isBG`
- `get defaultRect` — `logical isBackground`
- `get pushButtonList`
- `get defPushButton`
- `get escPushButton`
- `get isBackground` — `obj`
- `get showDefRect`
- `get showRect` — `obj`
- `get _ASYM_PopRTFHelp` — `fN, captn`
- `handle ASYM_Reset`
- `handle cancel`
- `handle copy`
- `handle fixScroll` — `fld`
- `handle fixSize`
- `handle keyUp` — `x, iss, isc`
- `handle leavePage`
- `handle windowSized`
- `get _ASYM_SelectObjectTarget` — `pReturnType, pFullReference, pTargetWindow, pObjectTypes, pNamedOnly, \`
- `get processGroupStuff` — `thisObj, topLevelOnly, allowGroups, exportableOnly`
- `get includeThisObj` — `pObj, pObjectsToInclude`
- `get ignoreThisObj` — `pObj, pObjectsToIgnore`
- `get validateObject` — `thisObj, objectsToInclude, objectsToIgnore, validObjectTypes, returnNamedOnly, objectsWhere`
- `get findValidObjectType` — `thisObj, validObjectTypes`
- `get findNamedObject` — `thisObj, returnNamedOnly`
- `get findObjectWhere` — `thisObj, objectsWhere`
- `get ASYM_SelectObjectFromList` — `pObjList, selectType, pDialogTitle`
- `handle init` — `pObjList`
- `handle OK`
- `handle cancel`
- `get ASYM_ObjectBitmapGroup` — `thisObj`
- `handle enterBackground`
- `get actualMediaSize` — `STACK pFrameSizeInPageUnits`
- `get nonMediaAreaStageSizes`
- `get windowCaptionHeight`
- `get windowBorderHeight`
- `get windowBorderWidth`
- `handle buttonDown`
- `handle updateMedia` — `frame`

### `tb115actr.sbk`

380 handlers (89 handle, 260 get, 31 set) from 12 type 10 scripts, resource ids 1414, 1416, 1418, 1420, 1422, 1424, 1426, 1428, 1430, 1432, 1434, 1436.

- `handle enterBook`
- `handle enterApplication`
- `handle leaveBook`
- `handle ASYM_LoadBook`
- `handle ASYM_UnloadBook`
- `handle linkSysbook`
- `handle author`
- `handle reader`
- `get ASYM_EA_GetParameterList` — `objectRef, event`
- `get ASYM_EA_ParameterList` — `event, obRef`
- `set ASYM_EA_ParameterList` — `event to value`
- `handle ASYM_EA_InitParameterList`
- `get ASYM_EA_GetLocalVariableList` — `objectRef, event`
- `get ASYM_EA_GetGlobalVariableList` — `OBJECT objectRef`
- `get ASYM_EA_LocalVariableInitialValue` — `variableName, objectRef, event`
- `set ASYM_EA_LocalVariableInitialValue` — `variableName, objectRef, event to value`
- `get ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event to value`
- `get ASYM_EA_GlobalVariableInitialValue` — `variableName, objectRef`
- `set ASYM_EA_GlobalVariableInitialValue` — `variableName, objectRef to value`
- `get ASYM_EA_GlobalVariable` — `variableName`
- `get ASYM_EA_FindLocalVariable` — `targetRef, event, varName`
- `get ASYM_EA_FindGlobalVariable` — `targetRef, varName`
- `handle ASYM_EA_RemoveParameter` — `parameterName, objectRef, actionBlockName`
- `handle ASYM_EA_RemoveLocalVariable` — `variableName, objectRef, event`
- `handle ASYM_EA_RemoveGlobalVariable` — `variableName, objectRef`
- `get ASYM_EA_LocalVariableName` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableName` — `varID, targetRef, event to value`
- `get ASYM_EA_GlobalVariableName` — `varID, targetRef`
- `set ASYM_EA_GlobalVariableName` — `varID, targetRef to value`
- `get ASYM_EA_CreateVarInfo` — `varName, varScope, targetRef, event, varID, indexExpression`
- `get ASYM_EA_VariableIsArray` — `varID, varScope, targetRef, event`
- `get ASYM_EA_LocalVariableIsArray` — `varID, targetRef, event`
- `get ASYM_EA_GlobalVariableIsArray` — `varName, targetRef`
- `get ASYM_EA_ParameterIsArray` — `paramNum, targetRef, event`
- `get ASYM_EA_GetNewVariableID` — `varScope, targetRef, event`
- `get ASYM_EA_ExtractVariableName` — `varInfo, targetRef, event`
- `get ASYM_EA_VariableNameFromID` — `varID, varScope, targetRef, event`
- `get ASYM_EA_ExtractVariableScope` — `varInfo, targetRef, event`
- `handle ASYM_EA_InitGlobalVariables` — `bkRef`
- `get ASYM_EA_GetTokenList`
- `get ASYM_EA_GetTokenDataType` — `token`
- `get ASYM_EA_IsVariableReference` — `varInfo, selfRef, event`
- `get ASYM_EA_IsPropertyReference` — `propInfo`
- `get ASYM_EA_Get` — `STACK dataStructure, STRING key`
- `get ASYM_EA_Set` — `STACK dataStructure, STRING key, STACK value`
- `get ASYM_EA_GetActionArray` — `event, obRef`
- `get ASYM_EA_GetActionBlockArray` — `actionBlockName, bkRef`
- `get ASYM_EA_GetActionMethodArray` — `actionMethodName, obRef`
- `get ASYM_EA_GetActionCount` — `actionArray[]`
- `get ASYM_EA_GetActionInfo` — `actionArray[], actionNum`
- `get ASYM_EA_GetActionKey` — `actionInfo, validate`
- `get ASYM_EA_FindNextClause` — `actionArray[] by reference, actionNumber`
- `get ASYM_EA_FindStructureEnd` — `actionArray[] by reference, actionNumber`
- `get ASYM_EA_FindStructureTypeEnd` — `actionArray[] by reference, actionNumber, structureType`
- `get ASYM_EA_FindStructureStart` — `actionArray[] by reference, actionNum`
- `get ASYM_EA_ExpressionDisplayStringFromExpressionInfo` — `expression, objectRef, event, editing`
- `get ASYM_EA_ExpressionOperatorArray`
- `set ASYM_EA_ExpressionOperatorArray` — `to operatorArray[][]`
- `get ASYM_EA_ExpressionDataRuleArray`
- `set ASYM_EA_ExpressionDataRuleArray` — `to dataRuleArray[][]`
- `handle ASYM_EA_ExpressionInitializeOperatorArrays`
- `get ASYM_EA_ResolveObject` — `objectInfo, obRef, targetRef, validate`
- `get ASYM_EA_ResolveBookName` — `bookName, obRef`
- `get ASYM_EA_FindPage` — `pageName, pageID, bookRef, obRef`
- `get ASYM_EA_FindBackground` — `bgName, bgID, bookRef, obRef`
- `get ASYM_EA_FindObject` — `objectType, objectName, objectID, layerRef, obRef`
- `get ASYM_EA_ConstructObjectIdentifier` — `targetRef, objectRef, noSelf, thisPage, layerRef`
- `get ASYM_EA_ObjectDescriptionFromObjectInfo` — `obInfo, selfRef, event, initCaps, obRef`
- `get ASYM_EA_RelativeObjectDescription` — `targetRef, sourceRef, initCaps, event`
- `get ASYM_EA_PopupPage` — `pageRef, closeOnClick`
- `get ASYM_EA_ResetPages` — `firstPage, lastPage`
- `get ASYM_EA_PlayAnimation` — `obRef, num`
- `handle doneAnimatingNotify` — `status, obRef`
- `get ASYM_EA_MessageBox` — `msg, cptn, icn, btns, helpTopicID, helpFile`
- `handle ASYM_EA_SendWindowsMessage` — `msgName`
- `handle ASYM_EA_CheckSysError` — `obRef, event, actionNum, bs`
- `get ASYM_EA_ObjectCache` — `obCache, obInfo, objectRef, targetRef`
- `get ASYM_EA_ObjectFromExpression` — `obType, obName, selfRef`
- `get ASYM_EA_ShellExecute` — `source, bkRef`
- `get ASYM_EA_ScoreQuestion` — `obRef, showFB, showScore, scoreFormat, lockQn, resetQn`
- `get ASYM_EA_ScorePages` — `startPgNum, endPgNum, showScore, scoreFormat, lockQn, resetQn, ignoreSkip`
- `get ASYM_EA_ScorePage` — `pgRef, showScore, scoreFormat, lockQn, resetQn, returnMaxScore`
- `handle ASYM_EA_ShowScore` — `score, mode`
- `get getGeolocationDistance` — `lat1, lon1, lat2, long2`
- `get ASYM_SetFocus`
- `get ASYM_RemoveFocus`
- `get ASYM_EA_PropertyDataType` — `obRef, propName`
- `get ASYM_EA_MethodList` — `obRef`
- `get ASYM_EA_MethodInfo` — `obRef, method`
- `get ASYM_EA_PropertyEnumInt` — `obRef, propName`
- `get ASYM_EA_PropertyEnumString` — `obRef, propName`
- `get ASYM_ReverseStack` — `STACK stk`
- `handle ASYM_EA_RuntimeError` — `errorTxt, objectRef, event, actionNumber`
- `get ASYM_EA_ActionName` — `actionKey`
- `get ASYM_EA_IsActionValid` — `actionInfo, targetObject, event`
- `get ASYM_EA_ActionErrors` — `actionInfo, targetObject, event, noRecurse`
- `get ASYM_EA_EventString` — `event`
- `get ASYM_EA_GetMethodType` — `obRef, methodName`
- `get ASYM_EA_InternalMethodList` — `obType`
- `set ASYM_EA_InternalMethodList` — `obType to value`
- `get ASYM_EA_InternalMethodListFromObjectRef` — `obRef`
- `handle ASYM_EA_InitInternalMethodList`
- `get ASYM_EA_ObjectTypesFromObjectRef` — `obRef`
- `get ASYM_EA_GetsFocus` — `targetRef`
- `get isNumber` — `value`
- `get ASYM_EA_EQ` — `a, b`
- `get ASYM_EA_NE` — `a, b`
- `get ASYM_EA_GT` — `a, b, asText`
- `get ASYM_EA_LT` — `a, b, asText`
- `get ASYM_EA_GE` — `a, b, asText`
- `get ASYM_EA_LE` — `a, b, asText`
- `get left`
- `set left` — `to value`
- `get top`
- `set top` — `to value`
- `get width`
- `set width` — `to value`
- `get height`
- `set height` — `to value`
- `get selectedItemText`
- `set selectedItemText` — `to value`
- `get ASYM_CleanCaption`
- `get ASYM_ItemText`
- `set ASYM_ItemText` — `to value`
- `get ASYM_ItemSelected`
- `set ASYM_ItemSelected` — `to value`
- `get lastScore`
- `get minimumScore`
- `get maximumScore`
- `get locked`
- `get tryCount`
- `get tryLimit`
- `get mediaPosition`
- `set mediaPosition` — `to value`
- `get mediaPlaying`
- `get ASYM_EA_GetClipRef` — `obRef`
- `get visited`
- `get title`
- `get description`
- `get studentName`
- `get isGeolocationSupported`
- `get isGeolocationReady`
- `get currentLatitude`
- `get currentLongitude`
- `get currentGeolocationAccuracy`
- `handle selectChange` — `choice`
- `handle ASYM_Select`
- `handle buttonDown`
- `handle mouseEnter`
- `handle mouseLeave` — `pos`
- `handle buttonUp`
- `handle keyDown` — `key, isShift, isCtrl`
- `get ASYM_EA_IsListBox` — `targetRef`
- `handle ASYM_Trigger`
- `handle stopAllMedia` — `recurse`
- `handle enterField`
- `handle leaveField`
- `handle clearOldText` — `targetRef`
- `handle ASYM_StartSimulation`
- `handle ASYM_EndSimulation`
- `handle ASYM_StartStep`
- `handle ASYM_EndStep`
- `handle ASYM_AttemptStep`
- `handle ASYM_Changed`
- `handle ASYM_Complete`
- `handle ASYM_User`
- `handle ASYM_EA_Make`
- `get ASYM_DuplicateChar` — `txt, chr`
- `get ASYM_SIM_IsEvaluationObject` — `obRef`
- `get ASYM_SIM_IsTriggerObject` — `obRef`
- `get ASYM_SIM_isObjectClickable` — `obRef`
- `get ASYM_SIM_ObjectGetsFocus` — `obRef`
- `get ASYM_SIM_ObjectHasSelectableItems` — `obRef`
- `get ASYM_SIM_ObjectType` — `obRef`
- `get ASYM_SIM_ObjectDescription` — `obRef, initCaps`
- `get ASYM_SIM_ObjectTypeDescription` — `obType, obRef, initCaps`
- `get ASYM_SIM_TriggerObjectDescription` — `obRef`
- `get ASYM_SIM_KeyString` — `key, caps, useThe`
- `get ASYM_SIM_ObjectState` — `obRef, obType`
- `set ASYM_SIM_ObjectState` — `obRef, obType to value`
- `get ASYM_SIM_DefaultTextEditState` — `obState`
- `get ASYM_SIM_StateMatches` — `obRef, requiredState, actualState`
- `get ASYM_SIM_EditFieldStateMatches` — `requiredState, actualState`
- `get ASYM_SIM_MaxFeedbackAttempts`
- `get ASYM_SIM_GetAutoInstructionText` — `selfRef, stepInfo, allEvalObjects[][] by reference`
- `get ASYM_SIM_GetAutoTriggerFeedback` — `selfRef, triggerEvents`
- `get ASYM_SIM_GetAutoObjectFeedback` — `obRef, actualState, requiredState, previousState, isPopup, objDescTemplate`
- `get ASYM_SIM_GetFeedbackText` — `feedbackInfo, simMode, currentTry, maxTries, forceLastAttempt`
- `set ASYM_SIM_ItemProperty` — `propName, itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemProperty` — `propName, itemType, stepNum, itemNum`
- `set ASYM_SIM_ItemData` — `itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemData` — `itemType, stepNum, itemNum`
- `get ASYM_SIM_GetIncludedObjectsArray`
- `get ASYM_SIM_CurrentStepID`
- `get ASYM_SIM_CurrentStepName`
- `get ASYM_SIM_CurrentStepInfo`
- `get ASYM_SIM_StepInfo` — `stepNum`
- `get ASYM_SIM_StartingMode`
- `get ASYM_SIM_GetBookMode`
- `handle ASYM_SIM_DisplayInstructions` — `simMode, stepInfo, includedObjects[][] by reference`
- `handle ASYM_SIM_ShowFeedback` — `stepInfo, stepNum, triggerEvents, matchingTriggerInfo, simMode, initialFeedbackText, forceLastAttempt`
- `get ASYM_SIM_GetObjectDescriptionString` — `obRef, obInfo, obType`
- `get ASYM_SIM_GetDefaultObjectDescriptionString` — `obRef, obType`
- `get ASYM_SIM_GetErrorObjectInfo` — `stepInfo, needFeedback, needRequiredState, forceLastAttempt`
- `get ASYM_SIM_RememberListboxState` — `pRef`
- `get ASYM_SIM_RestoreListboxState` — `pRef, stateInfo`
- `handle ASYM_SIM_HidePointer` — `animateMouse`
- `handle ASYM_SIM_NavigatePointerTo` — `mousePointer, pos, targetViewer, notifyObject, timeFactor, nextAction`
- `get ASYM_SIM_PauseMousePointer` — `animateMouse`
- `get ASYM_SIM_ResumeMousePointer` — `animateMouse, details`
- `handle ASYM_SIM_ShowMousePointer` — `animateMouse, targetViewer, pos, isPixels`
- `handle ASYM_SIM_ShowMousePointerClick` — `animateMouse, clickType`
- `handle ASYM_SIM_HideMousePointerClick` — `animateMouse`
- `handle ASYM_SIM_SetPointerTimeFactor` — `animateMouse, timeFactor`
- `handle ASYM_SIM_ShowComboPopup` — `comboRef, targetViewer`
- `get ASYM_SIM_GetComboScrollDir` — `itemNum`
- `get ASYM_SIM_GetComboItemPosition` — `itemNum`
- `get ASYM_SIM_GetComboScrollPosition` — `dir`
- `get ASYM_SIM_ScrollPopup` — `itemNum`
- `handle ASYM_SIM_SelectComboboxItem` — `obState`
- `handle ASYM_SIM_CloseComboPopup`
- `get ASYM_SIM_GetComboPopupState`
- `get ASYM_SIM_RestoreComboPopupState` — `popupState`
- `handle buttonClick` — `pos, isShift, isCtrl`
- `handle rightButtonDown` — `pos, isShift, isCtrl`
- `handle buttonDoubleClick` — `pos, isShift, isCtrl`
- `get ASYM_EA_GetActionArray` — `eventName, obRef`
- `get ASYM_EA_GetActionBlockArray` — `actionBlockName, bkRef`
- `get ASYM_EA_GetActionMethodArray` — `actionMethodName, obRef`
- `get ASYM_EA_ObjectFromExpression` — `obType, obName, selfRef`
- `get ASYM_EA_PopupPage` — `pageRef, closeOnClick`
- `get ASYM_EA_ResetPages` — `firstPage, lastPage`
- `get ASYM_EA_PlayAnimation` — `obRef, num`
- `get ASYM_EA_ShellExecute` — `source, bkRef`
- `get ASYM_EA_ScoreQuestion` — `obRef, showFB, showScore, scoreFormat, lockQn, resetQn`
- `get ASYM_EA_ScorePages` — `startPgNum, endPgNum, showScore, scoreFormat, lockQn, resetQn, ignoreSkip`
- `get ASYM_EA_ScorePage` — `pgRef, showScore, scoreFormat, lockQn, resetQn, returnMaxScore`
- `handle ASYM_EA_ShowScore` — `score, mode`
- `get getGeolocationDistance` — `latitude1, longitude1, latitude2, longitude2`
- `get toRadians` — `degrees`
- `get ASYM_EA_ConvertDataType` — `value, dataType`
- `get ASYM_EA_ExpressionOperatorArray`
- `get ASYM_EA_ExpressionDataRuleArray`
- `set ASYM_EA_ExpressionOperatorArray` — `to operatorArray[][]`
- `set ASYM_EA_ExpressionDataRuleArray` — `to dataRuleArray[][]`
- `handle ASYM_EA_ExpressionInitializeOperatorArrays`
- `get ASYM_EA_ExpressionDisplayStringFromExpressionInfo` — `STACK expression, targetRef, event, editing, parentHasBrackets, parentOperatorPrecedence, parentAssociative`
- `get ASYM_EA_GetGlobalVariableList` — `targetRef`
- `get ASYM_EA_GetLocalVariableList` — `targetRef, event`
- `get ASYM_EA_GetParameterList` — `targetRef, event`
- `get ASYM_EA_LocalVariableInitialValue` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableInitialValue` — `varID, targetRef, event to value`
- `get ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event`
- `set ASYM_EA_LocalVariableIsStatic` — `varID, targetRef, event to value`
- `get ASYM_EA_GlobalVariableInitialValue` — `varName, targetRef`
- `set ASYM_EA_GlobalVariableInitialValue` — `varName, targetRef to value`
- `get ASYM_EA_VariableIsArray` — `varID, varScope, targetRef, event`
- `get ASYM_EA_LocalVariableIsArray` — `varID, targetRef, event`
- `get ASYM_EA_GlobalVariableIsArray` — `varName, targetRef`
- `get ASYM_EA_ParameterIsArray` — `paramNum, targetRef, event`
- `handle ASYM_EA_RemoveParameter` — `parameterName, targetRef, actionBlockName`
- `handle ASYM_EA_RemoveLocalVariable` — `varID, targetRef, event`
- `handle ASYM_EA_RemoveGlobalVariable` — `varName, targetRef, event`
- `get ASYM_EA_LocateVariable` — `STACK varList, varName`
- `get ASYM_EA_LocalVariableName` — `varID, targetRef, event`
- `get ASYM_EA_GlobalVariableName` — `varID, targetRef`
- `set ASYM_EA_LocalVariableName` — `varID, targetRef, event to value`
- `set ASYM_EA_GlobalVariableName` — `varID, targetRef to value`
- `get ASYM_EA_ExtractVariableName` — `varInfo, targetRef, event`
- `get ASYM_EA_VariableNameFromID` — `varID, varScope, targetRef, event`
- `get ASYM_EA_ExtractVariableScope` — `varInfo, targetRef, event`
- `get ASYM_EA_CreateVarInfo` — `varName, varScope, targetRef, event, varID, indexExpression`
- `get ASYM_EA_GetNewVariableID` — `varScope, targetRef, event`
- `handle ASYM_EA_InitGlobalVariables` — `bkRef`
- `handle initVar` — `_varName, _varInitValue`
- `handle initArray` — `_varName`
- `get ASYM_EA_GlobalVariable` — `_ASYM_EA_VarName`
- `get ASYM_EA_FindLocalVariable` — `targetRef, event, varName`
- `get ASYM_EA_FindGlobalVariable` — `targetRef, varName`
- `get ASYM_EA_ParameterList` — `event, obRef, showArrays`
- `set ASYM_EA_ParameterList` — `event to value`
- `handle ASYM_EA_InitParameterList`
- `get ASYM_EA_ActionName` — `actionKey`
- `get ASYM_EA_IsActionValid` — `actionInfo, targetObject, event, forceReevaluate`
- `get ASYM_EA_ActionErrors` — `actionInfo, selfRef, event`
- `get objectTypesFromObjectRef` — `obRef`
- `get getsFocus` — `targetRef`
- `handle initInternalMethodList`
- `get internalMethodListFromObjectRef` — `obRef`
- `get getMethodType` — `obRef, methodName`
- `handle ASYM_SIM_ProcessEvent` — `simRef, event, targetRef, mod1, mod2`
- `get isTriggerTargetIncluded` — `simRef, obRef, event`
- `get ASYM_SIM_GetErrorObjectInfo` — `simRef, stepInfo, needFeedback, needRequiredState, forceLastAttempt`
- `get ASYM_SIM_StateMatches` — `obRef, requiredState, actualState`
- `get ASYM_SIM_EditFieldStateMatches` — `requiredState, actualState`
- `handle ASYM_SIM_ShowFeedback` — `simRef, stepInfo, stepNum, triggerEvents, matchingTriggerInfo, simMode, initialFeedbackText, forceLastAttempt`
- `handle ASYM_SIM_DisplayInstructions` — `simRef, simMode, stepInfo, includedObjects[][] by reference`
- `get ASYM_SIM_IsEvaluationObject` — `obRef`
- `get ASYM_SIM_IsTriggerObject` — `obRef`
- `get ASYM_SIM_IsMenuObject` — `obRef`
- `get ASYM_SIM_IsObjectClickable` — `obRef`
- `get ASYM_SIM_ObjectGetsFocus` — `obRef`
- `get ASYM_SIM_ObjectHasSelectableItems` — `obRef`
- `get ASYM_SIM_ObjectType` — `obRef`
- `get ASYM_SIM_ObjectDescription` — `obRef, initCaps`
- `get ASYM_SIM_ObjectTypeDescription` — `obType, obRef, initCaps`
- `get ASYM_SIM_TriggerObjectDescription` — `obRef`
- `get ASYM_SIM_KeyString` — `key, caps, useThe`
- `get ASYM_SIM_ObjectState` — `obRef, obType`
- `set ASYM_SIM_ObjectState` — `obRef, obType to value`
- `get ASYM_SIM_DefaultTextEditState` — `obState`
- `get ASYM_SIM_MaxFeedbackAttempts`
- `get ASYM_SIM_GetAutoInstructionText` — `selfRef, stepInfo, includedObjects[][] by reference`
- `get ASYM_SIM_GetAutoTriggerFeedback` — `selfRef, triggerEvents`
- `get ASYM_SIM_GetAutoObjectFeedback` — `obRef, actualState, requiredState, previousState, isPopup, objDescTemplate`
- `get ASYM_SIM_GetFeedbackText` — `feedbackInfo, simMode, currentTry, maxTries, forceLastAttempt`
- `get buildItemString` — `itms, txt`
- `get ASYM_SIM_StartingMode` — `simRef`
- `get ASYM_SIM_GetBookMode` — `simRef`
- `set ASYM_SIM_ItemProperty` — `simRef, propName, itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemProperty` — `simRef, propName, itemType, stepNum, itemNum`
- `get validateState` — `stateval, obRef`
- `get convertToFeedbackTypeName` — `propName`
- `get convertToFeedbackValName` — `propName`
- `set ASYM_SIM_ItemData` — `simRef, itemType, stepNum, itemNum to value`
- `get ASYM_SIM_ItemData` — `simRef, itemType, stepNum, itemNum`
- `get ASYM_SIM_GetObjectDescriptionString` — `obRef, obInfo, obType`
- `get ASYM_SIM_GetDefaultObjectDescriptionString` — `obRef, obType`
- `get objectDescriptionFromTemplate` — `objDescTemplate, obRef, value`
- `get getObjectDescriptionTemplate` — `simRef, obRef, includedObjects[][] by reference`
- `get ASYM_SIM_RememberListboxState` — `pRef`
- `get ASYM_SIM_RestoreListboxState` — `pRef, listInfo`
- `get tlEscape` — `t`
- `get tlUnescape` — `t`
- `handle showPointer` — `animateMouse, ownerViewer, pos, isPixels`
- `get initMousePointer` — `ownerViewer`
- `handle setRegion`
- `get createRegion` — `obRef, vRef`
- `handle showClick` — `animateMouse, clickType`
- `handle hideClick` — `animateMouse`
- `get pausePointer` — `animateMouse`
- `get resumePointer` — `animateMouse, details`
- `handle hidePointer` — `animateMouse`
- `handle navigateTo` — `mousePointer, p3, targetViewer, notifyObject, timeFactor, nextAction`
- `handle animatePointer` — `ax, ay, bx, by, cx, cy, dx, dy`
- `get getControlPoints` — `x0, y0, x3, y3`
- `get getControlPointAngles` — `dx, dy`
- `get getAngle` — `dx, dy`
- `get roundToPageUnitsX` — `value`
- `get roundToPageUnitsY` — `value`
- `handle setPosition` — `vRef, viewerPos, forceMove`
- `handle showViewer` — `vRef`
- `handle closeViewer` — `vRef`
- `get windowMoved` — `hWnd, dwMsg, wParam, lParam`
- `handle setTimeFactor` — `animateMouse, timeFactor`
- `handle ASYM_Reset`
- `get getTotalTime` — `hyp, timeFactor`
- `get adjustStartTime` — `startTime, currentTime`
- `handle showComboPopup` — `comboRef, targetViewer, forceSelectedTextline, forceScroll`
- `handle closeComboPopup`
- `get getComboPopupState`
- `get restoreComboPopupState` — `popupState`
- `get getScrollDir` — `itemNum`
- `get getItemPosition` — `itemNum`
- `get getScrollPosition` — `dir`
- `get scrollPopup` — `itemNum`
- `handle selectItem` — `obState`
- `get roundToPageUnitsX` — `value`
- `get roundToPageUnitsY` — `value`
- `get convertToSourceUnits` — `x, y`
- `get getScrollButtonWidth`
- `get getScrollButtonHeight`
- `handle setPosition` — `vRef, viewerPos, forceSet`
- `handle showViewer` — `vRef`
- `handle closeViewer` — `vRef`
- `get windowMoved` — `hWnd, dwMsg, wParam, lParam`
- `handle author`
- `handle reader`
- `handle buttonClick`

### `tb115aicc.sbk`

59 handlers (8 handle, 51 get, 0 set) from 3 type 10 scripts, resource ids 1050, 1052, 1054.

- `handle Init_AICC_Standards`
- `get ASYM_AICC_Init`
- `get ASYM_AICC_ExtractFromCmdLine` — `commandLn`
- `get ASYM_AICC_GetMultipleParameters` — `paramList, _text, storeInVars`
- `get paramName_VarEquivalent` — `paramName`
- `get ASYM_AICC_GetSingleParameter` — `paramName, _text`
- `get ASYM_OLX`
- `handle enterSystem`
- `handle linkSysbook`
- `handle unlinkSelf`
- `handle unlinkSysbook`
- `handle exit`
- `get ASYM_CMS_CollectTotalScore` — `includeSkip`
- `get ASYM_AICC_CorrectWidgetAnswers` — `ansArray[][]`
- `get ASYM_ACIEndLesson` — `status`
- `get ASYM_CMS_AccessRights`
- `get ASYM_CMS_UserID`
- `get ASYM_CMS_UserName`
- `get ASYM_CMS_BookName`
- `get ASYM_CMS_RuntimeLinked`
- `get ASYM_CMS_CMSApplicationName`
- `get ASYM_CMS_AskToContinue`
- `get ASYM_CMS_BookmarkFileName`
- `get ASYM_CMS_DataDir`
- `get ASYM_CMS_dbError`
- `get ASYM_CMS_dbErrorString`
- `get ASYM_CMS_dbOK`
- `get ASYM_CMS_EnterApplication`
- `get ASYM_CMS_GetRecordedScore` — `arg`
- `get ASYM_CMS_GoToModule`
- `get ASYM_CMS_IniFile`
- `get ASYM_CMS_IsCourseCompleted`
- `get ASYM_CMS_LeaveApplication`
- `get ASYM_CMS_LogDir`
- `get ASYM_CMS_LogFileName`
- `get ASYM_CMS_LogType`
- `get ASYM_CMS_MarkAsCompleted`
- `get ASYM_CMS_ModuleFileName`
- `get ASYM_CMS_RecordScore`
- `get ASYM_CMS_ReturnToCMS`
- `get ASYM_CMS_SetBookmarkFileName`
- `get ASYM_CMS_SetLogDir`
- `get ASYM_CMS_SetLogFileName`
- `get ASYM_CMS_SetLogType`
- `get ASYM_CMS_SetNextModule`
- `get asym_CMS_sysBookName`
- `get AICC_ExitAU`
- `get ASYM_INET_DLL_Link`
- `get urlEncode` — `str`
- `get ASYM_AICC_SpecialCharsContract` — `s`
- `get formatTimetoSec` — `whatTime`
- `get formatTimetoHHMinSEC` — `whattime,No_00_flag`
- `get ASYM_AICC_ProcessForError` — `returnString`
- `handle ASYM_AICC_ImmediateExit`
- `get ASYM_AICC_CleanupResponse` — `txt`
- `handle AICC_Set_Score` — `status`
- `get ASYM_AICC_BuildPostStr_PutParam` — `status, score, _time`
- `get ASYM_ConvertToAICCPercent` — `totalScore`
- `get _AICC_ExitAU`

### `tb115anm.sbk`

47 handlers (18 handle, 19 get, 10 set) from 1 type 10 scripts, resource ids 272.

- `handle linkSysbook`
- `handle moved`
- `handle playAnimation` — `animation, notifyObject, waitTillDone, options`
- `handle ASYM_Reset`
- `handle pauseAnimation` — `status`
- `handle stopAnimation` — `status, options`
- `handle ASYM_CleanupAnimations`
- `handle jumpToStep` — `whichStep, whichAnimation`
- `handle jumpToPercent` — `percentComplete, whichAnimation`
- `handle playStep` — `currentAnim`
- `handle updateCel` — `theTarget, StepsPerCel, stepNumber,previousstepNumber`
- `handle doneAnimatingNotify` — `status,whatObject`
- `handle restoreAnimation` — `objectList, animationList`
- `get ASYM_CloseAllAnimations`
- `handle closeAllAnimations`
- `get closeAllAnimations_WinMsg` — `-- process after call to system`
- `get objectAnimation` — `rowNum`
- `set objectAnimation` — `to animationSettings[]`
- `get animationCacheEntry` — `theTarget`
- `get anim_Offset`
- `set anim_Offset` — `to value`
- `get anim_CurrentStep`
- `set anim_CurrentStep` — `to value`
- `get anim_NumRepetitions`
- `set anim_NumRepetitions` — `to value`
- `get anim_CelAnimation` — `whichAnimation`
- `set anim_CelAnimation` — `to value`
- `get anim_ShowAllSteps` — `whichAnimation`
- `set anim_ShowAllSteps` — `whichAnimation to value`
- `get anim_Duration` — `whichAnimation`
- `set anim_Duration` — `whichAnimation to value`
- `get anim_NumSteps` — `whichAnimation`
- `set anim_NumSteps` — `whichAnimation to value`
- `get anim_StepsPerCell` — `whichAnimation`
- `set anim_StepsPerCell` — `whichAnimation to value`
- `get anim_StartPosition` — `whichAnimation`
- `set anim_StartPosition` — `whichAnimation to value`
- `get anim_StartSize` — `whichAnimation`
- `get anim_EndSize` — `whichAnimation`
- `get anim_StartTime`
- `get anim_elapsedTime`
- `get anim_currentTime`
- `handle updateAnimations`
- `get animTimer` — `whatHandle, whatMsg, wparam`
- `handle startAnimTimer`
- `handle stopAnimTimer`
- `handle author`

### `tb115ftp.sbk`

147 handlers (54 handle, 86 get, 7 set) from 15 type 10 scripts, resource ids 1599, 1602, 1604, 1606, 1608, 1610, 1612, 1614, 1616, 1618, 1620, 1622, 1624, 1626, 1628.

- `handle enterApplication`
- `handle linkSysbook`
- `handle linkRuntimeSystemBook`
- `get _ftp_SearchDirForFile` — `dir, fn, recurse`
- `get _ftp_AllowOverwriteDB` — `destFn, destFnLocation, destFnSize, destFnDate, srcFn, srcFnLocation, srcFnSize, srcFnDate, IsBatch`
- `get ASYM_ftpBatchPutDirectory` — `szHost, szUser, szPassword, szAccount, szLocalDir, szRemoteDir, \`
- `get ASYM_ftpPutDirectory` — `p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,p11,p12`
- `get ASYM_ftpBatchPutFilesFromList` — `szHost, szUser, szPassword, \`
- `get ASYM_ftpGetErrorString` — `errNo`
- `get ASYM_ftpGetFile` — `szHost, szUser, szPassword, \`
- `get ASYM_ftpPutFile` — `szHost, szUser, szPassword, \`
- `handle unlinkSysBook`
- `handle leaveApplication`
- `handle leaveSystem`
- `get ASYM_ftpMakeTempFile` — `szStub`
- `get ASYM_ftpDeleteLocalFile` — `szFn`
- `get ASYM_ftpGetTotalFileSize` — `dirName, bRecurse`
- `get ASYM_CopyTree` — `sourceDir, destDir, bRecurse, bPromptOverwrite, boolOnlyIfNewer, bShowProgress, szShowResult`
- `get ASYM_ftpLocalCopyFiles` — `sourceDir, destDir, bRecurse, bPromptOverwrite,  boolOnlyIfNewer, bShowProgress, szShowResult`
- `get ASYM_ftpDelFileTree` — `szHost, szUser, szPassword, szAccount, szRemoteDir, bConfirm, szShowResult`
- `get ASYM_ftpDelDirTree` — `szHost, szUser, szPassword, szAccount, szRemoteDir, bConfirm, szShowResult`
- `get _ftp_PutFileList`
- `get _ftp_PutDirectory` — `p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11`
- `get _ftpputDirDB` — `szHost, szUser, szPassword, szAccount,\`
- `handle author`
- `handle reader`
- `handle asym_reset`
- `handle save`
- `handle enterField`
- `handle firstIdle`
- `handle idle`
- `handle enterPage`
- `handle remoteSet` — `what, toWhat`
- `get setLocalDirAndFileList` — `what`
- `handle initDefaults`
- `handle OK`
- `get ASYM_Enabled`
- `handle SaveIniSettings`
- `handle cancel`
- `get checkDirForFiles` — `path`
- `get mungePassword` — `s`
- `get isNumber` — `x`
- `get SearchFileForString` — `file, str`
- `get appendPath` — `p1, p2`
- `handle buttonClick`
- `get propValue`
- `set propValue` — `to what`
- `handle enterField` — `--1793`
- `handle keyChar` — `--1793`
- `handle leaveField`
- `handle fixMyPrompt`
- `handle updateLocalDir` — `--1793`
- `get propValue`
- `set propValue` — `to what`
- `handle ASYM_ButtonClick`
- `handle fixMyPrompt`
- `handle ASYM_ButtonClick`
- `set propValue` — `to what`
- `get propValue`
- `get propValue`
- `set propValue` — `to what`
- `handle leaveField`
- `get propValue`
- `set propValue` — `to what`
- `handle leaveField`
- `handle fixMyPrompt`
- `get propValue`
- `set propValue` — `to what`
- `handle leaveField`
- `handle validateValue` — `txt`
- `get ftpLoginDB` — `szHost, szUser, szPassword, szAccount`
- `handle enterField`
- `handle firstIdle`
- `handle enterPage`
- `handle OK`
- `handle cancel`
- `get trim` — `s`
- `handle idle`
- `handle FTPShowStatus` — `msg, progress1`
- `handle showMyViewer`
- `handle hideMyViewer`
- `handle cancel`
- `handle buttonDown`
- `handle reset`
- `set progress` — `to n`
- `get _ASYM_ftpGetTotalFileSize` — `dirName, boolRecurse, boolShowProgress`
- `get GetLocalDirMap` — `LocalDirMap[][] by reference, szLocalDir, dirDepth, boolTallyFileSize, boolShowProgress, ftpkey`
- `get _ASYM_ftpLocalCopyFiles` — `sourceDir, destDir, bRecurse, bPromptOverwrite, bOnlyIfNewer, bShowProgress, szShowResult`
- `handle showStatus` — `msg, prgrs`
- `get copyDirFilesOnly` — `srcDir, destDir, bPromptOverwrite, bOnlyIfNewer, bShowProgress, szShowResult`
- `get IsFileMoreRecent` — `newF, oldF`
- `get _ftp_SearchDirForFile` — `dir, fn, recurse`
- `get SearchDirForFile` — `dir, fn, recurse`
- `get _ASYM_ftpBatchPutDirectory` — `szHost, szUser, szPassword, szAccount, szLocalDir, szRemoteDir, \`
- `handle showStatus` — `msg, progress`
- `get _ASYM_ftpBatchPutFilesFromList` — `szHost, szUser, szPassword, szAccount, szLocalDir, szRemoteDir, \`
- `handle setFTPDLLOptions` — `ftpHandle, bProgressMessage, bLowerCase, bBinary`
- `get checkFTPResult` — `ftpHandle, result`
- `get _ASYM_ftpGetFile` — `szHost, szUser, szPassword, szAccount, szRemoteFileName, szLocalFileName, \`
- `get _ASYM_ftpPutFile` — `szHost, szUser, szPassword, szAccount, szLocalFileName, szRemoteFileName, \`
- `get asym_ftpLinkDLL`
- `get CountFiles` — `fileNameMask`
- `get CreateOrVerifyRemoteDir` — `ftpHandle,\`
- `get ftp_GetLastError`
- `get ftp_Goodbye`
- `get ftp_pwd` — `hndl`
- `get ftp_quote` — `hndl, cmd`
- `get ftp_replyString` — `hndl`
- `get FTPErrNoFromErrString` — `s`
- `get getDirSeparator` — `ftpHandle`
- `handle idle`
- `get InitFTPLink` — `szHost, szUser, szPassword, szAccount, boolShowProgress`
- `get MoveToRemoteDirectory` — `ftpHandle, szRemoteDir, createIfNecessary`
- `get ParseDirs` — `dirspec, dirs[] by reference, sep`
- `get PutSubDirFiles` — `ftpHandle, szLocalDir,\`
- `get PutDirFiles` — `ftpHandle, fileNameMask, lc, boolPromptOverwrite, bOnlyIfNewer, bShowProgress`
- `get getRemoteFileList` — `ftpHandle`
- `get isRemoteFileOlder` — `ftpHandle, localFn, remoteFn`
- `get isLocalFileOlder` — `ftpHandle, localFn, remoteFn`
- `get remoteFileInfo` — `ftpHandle, fn`
- `get allowOverwrite` — `ftpHandle, destFn, destFileLocation, srcFile, IsBatch`
- `get FindFileInRemDirList` — `fn`
- `get rightMatch` — `substrng, strng`
- `handle ShowOptionalDone` — `szDoneMessage, result`
- `get _ASYM_ftpMakeTempFile` — `szStub`
- `get _ASYM_ftpDeleteLocalFile` — `szFn`
- `get isNumber` — `x`
- `get _ftp_delFileTree` — `p1,p2,p3,p4,p5,p6,p7`
- `get _ftp_delDirTree` — `p1,p2,p3,p4,p5,p6,p7`
- `get zapDirFiles` — `boolDelTheDir, szHost, szUser, szPassword, szAccount, szRemoteDir, boolConfirm, szShowResult`
- `get deleteFilesInCurrentRemoteDir` — `ftpHandle`
- `get localFileDateInSeconds` — `fN`
- `get remoteFileDateInSeconds` — `ftpHandle, fN`
- `get ftp_put` — `p1,p2,p3`
- `get ftp_get` — `p1,p2,p3`
- `get ftp_mput` — `p1,p2,p3`
- `handle ReEnableViewers`
- `handle DisableViewers`
- `get ConfirmAbortTransfer`
- `get inDir` — `childSpec, parentDir`
- `get errString32` — `pErrorCode`
- `get AllowOverwriteDB` — `destFn, destFnLocation, destFnSize, destFnDate, srcFn, srcFnLocation, srcFnSize, srcFnDate, IsBatch`
- `get getFileNameString` — `fileLocation, fileName`
- `get getStandardFileSizeString` — `fileSizeBytes`
- `get standardFileTimeStringFromSeconds` — `fileTime`
- `handle buttonClick`
- `handle close`

### `tb115hyp.sbk`

116 handlers (20 handle, 93 get, 3 set) from 3 type 10 scripts, resource ids 651, 653, 655.

- `handle linkSysBook`
- `get ASYM_URLSpecialCharsExpand` — `s`
- `get ASYM_URLSpecialCharsContract` — `s`
- `get _ASYM_AddAnswerArrayHyperlink` — `fixed ansArray[][] by reference, int iRow, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddAnswerHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddHyperlinkToArray` — `hyperlinks[][] by reference,linkName, pgRef,  transFx, linkType, curs, isURL, vRef`
- `get _ASYM_AddLinkToArray` — `hyperlinks[][] by reference, int iRow, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _ASYM_requestRemoveAmpersand` — `txt`
- `get _ASYM_BadLinksList` — `fixed hyperlinks[][] by reference`
- `get _ASYM_ClearAnsArrayHyperlink` — `fixed ansArray[][] by reference, int iRow`
- `get _ASYM_ClearAnswerHyperlink` — `obj, linkName`
- `get _ASYM_ClearHyperlink` — `obj, linkName`
- `get _ASYM_ClearHyperlinkFromArray` — `hyperlinks[][] by reference, linkName`
- `get _ASYM_ExecHyperLink` — `fixed hyperlinks[][] by reference, linkName`
- `get _ASYM_HyperlinkCandidates` — `obj, candidates[] by reference`
- `get _ASYM_HyperlinkLinkInfo` — `hyperlinks[][] by reference, linkName, resolv`
- `get _ASYM_HyperlinkIRow` — `STRING linkName, hyperlinks[][] by reference`
- `get _ASYM_SysCursor`
- `handle _AutoCloseCheck` — `loc`
- `handle _SetHyperPath` — `bk, what`
- `get _tbk_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _tbk_AddHyperlinktoArray` — `hyperlinks[][] by reference,linkName, pgRef,  transFx, linkType, curs, isURL, vRef`
- `get _tbk_AddLinkToArray` — `hyperlinks[][] by reference, int iRow, pgRef, transFx, linkType, curs, isURL, vRef`
- `get _tbk_BadLinksList` — `fixed hyperlinks[][] by reference`
- `get _tbk_ClearHyperlink` — `obj, linkName`
- `get _tbk_ClearHyperlinkFromArray` — `hyperlinks[][] by reference, linkName`
- `get _tbk_ExecHyperLink` — `fixed hyperlinks[][] by reference, linkName`
- `get _tbk_HyperlinkCandidates` — `obj, candidates[] by reference`
- `get _tbk_HyperlinkLinkInfo` — `hyperlinks[][] by reference, linkName, resolv`
- `get _tbk_HyperlinkIRow` — `STRING linkName, hyperlinks[][] by reference`
- `get _tbk_PopupPage` — `object pgRef, popStyle, pos, captn, curs`
- `get _tbk_SysCursor`
- `get ASYM_AddAnswerHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get ASYM_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get ASYM_AltPgName` — `page obj`
- `get ASYM_ChooseWebBrowser`
- `get ASYM_ClearAnswerHyperlink` — `obj, linkName`
- `get ASYM_ClearHyperlink` — `obj, linkName`
- `get ASYM_CurrentDirectory`
- `get ASYM_CurrentPath`
- `handle ASYM_DisplayURL` — `exeName, url, mode`
- `get ASYM_DoAnswerHyperlink` — `object obj, answerName, IsSpecific`
- `get ASYM_DoHyperlink` — `object obj, triggerName`
- `get ASYM_FindHyperPage` — `pgName, altPgName, bk, isURL, vSymbol`
- `get ASYM_FindHyperWindow` — `vSymbol`
- `get ASYM_FindPage` — `pgN`
- `get ASYM_FindPathFile` — `fName, path, bkPath`
- `get ASYM_GetAnswerHyperlinks` — `obj, linkName`
- `get ASYM_GetHyperlinks` — `obj, linkName`
- `get ASYM_GoToPage` — `pgRef, transfx, curs, isURL`
- `get ASYM_HasHyperlinks` — `obj`
- `get ASYM_HyperPath` — `bk`
- `set ASYM_HyperPath` — `to what`
- `get ASYM_IsFile` — `fName`
- `get ASYM_MakeIntoRelPath` — `rootPath,longPath`
- `get ASYM_MTBVersion` — `dotFlag, options`
- `get ASYM_ProductVersion` — `dotFlag, options`
- `get ASYM_NameOrID` — `obj`
- `get ASYM_ProductPrefix` — `capFlag`
- `get ASYM_RelativePath` — `path, bkName`
- `handle ASYM_ResetCursor`
- `get ASYM_Trim` — `s`
- `handle buttonClick` — `loc`
- `handle extClick` — `loc`
- `handle leaveBook`
- `get tbk_AddHyperlink` — `obj, linkName, pgRef, transFx, linkType, curs, isURL, vRef`
- `get tbk_AltPgName` — `page obj`
- `get tbk_ChooseWebBrowser`
- `get tbk_CurrentDirectory`
- `get tbk_CurrentPath`
- `handle tbk_DisplayURL` — `exeName, url, mode`
- `get tbk_DoHyperlink` — `object obj, triggerName`
- `get tbk_FindHyperPage` — `pgName, altPgName, bk, isURL, vSymbol`
- `get tbk_FindPage` — `pgN`
- `get tbk_FindPathFile` — `fName, path`
- `get tbk_GetHyperlinks` — `obj, linkName`
- `get tbk_GoToPage` — `pgRef, transfx, curs, isURL`
- `get tbk_HasHyperlinks` — `obj`
- `get tbk_HyperPath` — `bk`
- `set tbk_HyperPath` — `to what`
- `get tbk_IsFile` — `fName`
- `get tbk_MakeIntoRelPath` — `rootPath,longPath`
- `get tbk_NameOrID` — `obj`
- `get tbk_PopupPage` — `object pgRef, popStyle, pos, captn, curs`
- `get tbk_RelativePath` — `path, bkName`
- `get tbk_trim` — `s`
- `get ASYM_NewRelativePath` — `otherPath, rootPath`
- `get ASYM_ResolvePath` — `filePath`
- `get ASYM_ExpandRelPath` — `otherPath, rootPath`
- `get ASYM_ConvertPathToList` — `path`
- `get ASYM_ConvertListToPath` — `pathList`
- `get tbk_Container` — `obj, objType`
- `handle save`
- `handle saveAs`
- `get ASYM_IsHyperlinkSysBookAdded`
- `get ChooseWebBrowser`
- `handle WriteBrowserIniEntry` — `exeName, sectn, key`
- `get ddeServerName` — `exeName, ddeAppName`
- `handle DisplayURL` — `exeName, url, popup`
- `handle showError` — `errorKey, fn`
- `get ASYM_FindExecutableFile` — `fn`
- `get revOffset` — `s1, s2`
- `get URLSpecialCharsContract` — `s`
- `get URLSpecialCharsExpand` — `s`
- `get FileNameToURL` — `fn`
- `get ASYM_GetTempFile` — `pExt`
- `get ASYM_TempDir`
- `get _ASYM_ChooseFromTextLinesDlg` — `dlgCaption, prompt, txtLines, deflt`
- `handle enterPage`
- `handle Cancel`
- `handle closeThisWindow`
- `handle firstIdle`
- `handle idle`
- `handle OK`
- `set customSize` — `to what`

### `tb115r.sbk`

1022 handlers (207 handle, 804 get, 11 set) from 63 type 10 scripts, resource ids 872, 874, 876, 878, 880, 882, 884, 886, 888, 890, 892, 894, 896, 898, 900, 902, 904, 906, 908, 910, 912, 914, 916, 918, 920, 922, 924, 926, 928, 930, 932, 934, 936, 938, 940, 942, 944, 946, 948, 950, 952, 954, 956, 958, 960, 962, 964, 966, 968, 970, 972, 974, 976, 978, 980, 982, 984, 986, 988, 990, 992, 994, 996.

- `get ASYM_MTBVersion` — `dot, opts`
- `get ASYM_CBTVersion` — `dot, opts`
- `get ASYM_ProductPrefix` — `caps`
- `get ASYM_ProductVersion` — `dot, opts`
- `get ASYM_DisplayableVersion` — `opts`
- `get ASYM_ProductName`
- `get ASYM_ProductDesc`
- `get ASYM_RunSysBookName`
- `get ASYMR`
- `handle author`
- `handle buttonClick` — `loc`
- `handle buttonDown` — `loc`
- `handle clear`
- `handle closeWindow`
- `handle destroy`
- `handle enterApplication`
- `handle enterBook`
- `handle enterPage`
- `handle enterSystem`
- `handle enterWindow` — `vRef`
- `handle openWindow`
- `handle keyDown` — `key`
- `handle keyChar` — `x`
- `handle leaveApplication`
- `handle leaveBook`
- `handle leavePage`
- `handle leaveSystem`
- `handle leaveWindow`
- `handle linkSysBook`
- `handle unlinkSysBook`
- `handle mouseEnter`
- `handle mouseLeave`
- `handle newBackground`
- `handle newPage`
- `handle reader`
- `handle rightButtonDown` — `loc, sh, ct`
- `handle rightButtonUp` — `loc`
- `handle sized`
- `handle menuItemSelected`
- `handle ASYM_ResetCursor`
- `get ASYM_IsNumber` — `x`
- `get isNumber` — `x`
- `get ASYM_TextlineOffset` — `x, txt, pos`
- `get onLine`
- `set onLine` — `to val`
- `get ASYM_ItemInList` — `itm,lst`
- `get ASYM_TextlineInText` — `tl, txt`
- `get ASYM_BlockSuspend` — `stckFull`
- `get ASYM_RestoreSuspend` — `opts`
- `get ASYM_CollectWidgets` — `pg`
- `get INFO_CreatedBy`
- `handle ASYM_IAmWidget`
- `get ASYM_Container` — `STRING srcOb, obTypes`
- `handle ASYM_Trigger`
- `handle ASYM_Reset` — `mode, pRef`
- `get ASYM_IniCompanyName`
- `get ASYM_IniUserName`
- `handle ASYM_Idle;` — `end`
- `handle ASYM_BackgroundRightButtonDown;` — `end`
- `handle ASYM_BeginDrag;` — `end`
- `handle ASYM_ObjectDropped;` — `end`
- `handle ASYM_SummonWidgets;` — `end`
- `handle ASYM_PageEntered;` — `end`
- `handle ASYM_Scored;` — `end`
- `handle ASYM_Answered;` — `end`
- `handle ASYM_Changed;` — `end`
- `get ASYM_CMS_GetNextModule`
- `get ASYM_CMS_GotoModule`
- `get ASYM_CMS_IniFile`
- `get ASYM_CMS_MarkAsCompleted`
- `get ASYM_CMS_ModuleFileName`
- `get ASYM_CMS_RecordDetailInfo`
- `get ASYM_CMS_RecordedScore`
- `get ASYM_CMS_RecordScore`
- `get ASYM_CMS_SetNextModule`
- `get sliderMax`
- `set sliderMax` — `to value`
- `get sliderMin`
- `set sliderMin` — `to value`
- `handle sliderMove`
- `get sliderPos`
- `get sliderRatio`
- `set sliderRatio` — `to value`
- `get thumbPosition`
- `set thumbPosition` — `to val`
- `get thumbWidth`
- `set thumbWidth` — `to value`
- `get trackPosition`
- `set trackPosition` — `to v`
- `handle ASYM_SizeButtonToGraphic` — `a`
- `get ASYM_tbdosErrorString` — `a,b`
- `get ASYM_tbfile32ErrorString` — `a`
- `get ASYM_TBDLLErrorString` — `a,b,c`
- `get ASYM_ColorPaletteDlg` — `r,g,b`
- `get ASYM_ChooseColorDlg` — `r,g,b`
- `get ASYM_ChooseFontDlg` — `a,b`
- `get ASYM_OpenFileDlg` — `a,b,c,d,e`
- `get ASYM_OpenFileDlgLFN` — `a,b,c,d,e`
- `get ASYM_SaveAsDlg` — `a,b,c,d,e`
- `get ASYM_ChooseDirectoryDlg` — `a,b`
- `get ASYM_ChooseDirectoryDlgLFN` — `a,b`
- `get ASYM_SaveAsDlgLFN` — `a,b,c,d,e`
- `get ASYM_DuplicateClip` — `clipRef`
- `get ASYM_IsClip` — `STRING nm,bkRef`
- `get _ASYM_SysCursor`
- `get ASYM_WorkingCursor` — `pShow`
- `handle ASYM_ElapsedCursor` — `nmax,n,nm`
- `get ASYM_CursorInResizeHandle`
- `get ASYM_GetResizeTarget` — `pos`
- `get ASYM_CursorSelectionHandle` — `pos, obRef`
- `get ASYM_ClearClipboard`
- `get ASYM_CopyTextToClipboard` — `txt`
- `get ASYM_checkHyperSysBook`
- `get ASYM_EnableHyperlinks`
- `get ASYM_GlossaryPage` — `term,bk`
- `get ASYM_CheckObjectHyperlinks` — `ob`
- `get getLongDate`
- `get ASYM_EllipsizeFilenameInText` — `txt, fRef`
- `get ASYM_GetAvailableTextWidth` — `fRef`
- `get ASYM_NumberToRoman` — `num,case,stle`
- `get ASYM_RomanToNumber` — `rom`
- `get ASYM_CompareByCase` — `str1,str2`
- `get revOffset` — `s1,s2`
- `get ASYM_trim` — `s`
- `get trim` — `s`
- `get wordContains` — `x,txt`
- `get wordOffset` — `x,txt`
- `get ASYMA_FindWordStart` — `txt,chr,ln`
- `get ASYM_FindWordStart` — `txt,chr,ln`
- `get ASYM_Offset` — `str,src,pos`
- `get ASYM_ReverseStack` — `STACK stk`
- `get ASYM_StringOf` — `str,cnt`
- `get ASYM_TextlineFromPos` — `pos,txt`
- `get ASYM_SplitWordsOnCaps` — `txt`
- `get ASYM_ExpandEnvironmentStrings` — `str`
- `get ASYM_PathOfFile` — `pth`
- `get ASYM_ShortFileName` — `pth`
- `get ASYM_IsDirectoryWriteable` — `dir`
- `get ASYM_IsDriveReady` — `drv`
- `get ASYM_IsFileAvailable` — `fN`
- `get ASYM_CurrentDirectory`
- `get ASYM_CurrentPath`
- `get ASYM_FindPathFile` — `nm,path,bkPath`
- `get ASYM_FreeDiskSpace` — `dr`
- `get ASYM_GetPath` — `nm`
- `get ASYM_IsDirectory` — `dir`
- `get ASYM_DirectoryExists` — `dir`
- `get ASYM_IsFile` — `fn`
- `get ASYM_RelativePath` — `path,nm`
- `get ASYM_WindowsDirectory`
- `get ASYM_MakeIntoRelPath` — `subPath,bigPath`
- `get ASYM_SetCurrentDirectory` — `path`
- `get ASYM_SetCurrentPath` — `path`
- `get ASYM_SetPath` — `nm,path`
- `get ASYM_TempDir`
- `get ASYM_FindExecutableFile` — `fn`
- `get TBK_openAcrobatFile` — `a, b`
- `get ASYM_IsAbsoluteFilePath` — `fn`
- `get ASYM_RecurseCreateDirectory` — `dir`
- `get ASYM_ParentDirectory` — `dir`
- `get ASYM_ParsePath` — `path,op`
- `get ASYM_AppendFileToPath` — `dir,fn`
- `get ASYM_ExpandRelPath` — `a,b`
- `get ASYM_ResolvePath` — `filePath`
- `get ASYM_ConvertPathToList` — `path`
- `get ASYM_ConvertListToPath` — `pathList`
- `get ASYM_RecurseRemoveDirectory` — `dir,opts`
- `get ASYM_FindMediaFile` — `fn,bk,srchHD,srchCD,srchHypPath`
- `get ASYM_ExpandMediaPath` — `paths,bk`
- `get ASYM_FileRelativeToMedia` — `fn,bk,srchHD,srchCD,srchHypPath`
- `get ASYM_PromptForCDROM` — `fn,pMessage,cptn`
- `get ASYM_FindFileOnCDROM` — `fn`
- `get ASYM_StandardFolderPath` — `f`
- `get ASYM_FindAnswerIndex` — `itm,col,all`
- `handle ASYM_QLocked` — `ob,resp`
- `handle ASYM_QResponded` — `ob,resp`
- `handle ASYM_TypeInCompleted` — `txt,stat,fld`
- `handle ASYM_CheckDropObj` — `ob,loc`
- `get ASYM_CheckPoint` — `ob,loc,_target`
- `handle ASYM_CheckTries` — `_target`
- `get ASYM_RegisterAttempt` — `_target,mode,showFB,scr`
- `get ASYM_CondensePhonetic` — `s`
- `get ASYM_StripPunctuation` — `txt`
- `handle ASYM_GetTypeInData`
- `get ASYM_MatchString` — `testStr,refStr,byCase,jumbledOK,wildcard,trimText`
- `get ASYM_WID_Responses`
- `get ASYM_BeginResponse` — `ob,nm`
- `handle ASYM_RegisterResponse` — `ob,nm`
- `handle ASYM_WID_Chosen`
- `get ASYM_QuestionStatus` — `ob,_score,mode,noUpdate,showFB`
- `get _ASYM_FindString` — `fixed strgs[][] by reference,nm`
- `get ASYM_GetStandardString` — `nm,dflt`
- `get ASYM_GetString` — `nm,dflt`
- `get ASYMA_GetStringList`
- `get ASYM_AddString` — `nm,s`
- `get ASYM_ClearString` — `nm`
- `get ASYM_ObjectExists` — `STRING ob`
- `get ASYM_QuestionText` — `tgt,opt,txt,fld`
- `get ASYM_GetQuestionTextField` — `tgt,fld`
- `get ASYM_GetQuestionTextAutoFields` — `tgt`
- `get ASYM_FindField` — `fldName,pg`
- `get ASYM_FindPage` — `pgN`
- `get ASYM_GetObjectListByName` — `ob,otype,hasScript,nm`
- `get ASYM_NameOrID` — `ob`
- `get ASYM_ObjectCenter` — `ob`
- `set ASYM_ObjectCenter` — `to loc`
- `get ASYM_OppositePos` — `pos`
- `handle ASYM_ScrollListBoxToSelection`
- `get ASYM_WordFromPoint` — `loc`
- `handle ASYMA_CopyUserProperties` — `obj1,obj2`
- `handle ASYM_FixFieldScrollBar` — `fld`
- `get ASYM_CopyProperty` — `srcRef,destRef,srcProp,destProp`
- `get ASYM_ObjectParentList` — `ob,cutOff`
- `get ASYM_ObjectsWhere` — `ob,objTypes,express`
- `get ASYM_ResolveObject` — `obInfo,ob,srcRef,validate`
- `get ASYM_ResolveBookName` — `bkNm,ob`
- `get ASYM_ResolvePage` — `pgNm,pgID,bkRef,ob`
- `get ASYM_ResolveBackground` — `bgName,bgID,bkRef,ob`
- `get ASYM_FindObject` — `objectType,objectName,objectID,layerRef,ob`
- `get ASYM_ConstructObjectIdentifier` — `ob, srcRef, noSelf, thisPage, layerRef`
- `get ASYM_ObjectDescriptionFromObjectInfo` — `obInfo, srcRef, event, initCaps, ob`
- `get ASYM_RelativeObjectDescription` — `ob, srcRef, initCaps, event`
- `handle ASYM_RegisterPath` — `path, ob`
- `get ASYM_FirstNavigablePage`
- `get ASYM_LastNavigablePage`
- `get ASYM_NextNavigablePage`
- `get ASYM_PreviousNavigablePage`
- `get ASYM_CBTIniVar` — `sxn, key, dflt`
- `handle ASYM_FlushMsgQ`
- `get ASYM_GetSystemVar` — `nm`
- `get ASYM_RandomList` — `cnt, inList`
- `get ASYM_ProductDirectory`
- `get ASYM_LongProductDirectory`
- `get ASYM_SystemDirectory`
- `get ASYM_DrawFocusRect` — `bnds, vRef`
- `get ASYM_DeleteHandler` — `ob, nm`
- `get ASYM_Is32Bit`
- `get ASYM_ScreenInfo`
- `get ASYM_MonitorContaining` — `loc, dflt`
- `get ASYM_MonitorWorkAreaBounds` — `loc, dflt`
- `get ASYM_MonitorBounds` — `loc, dflt, workArea`
- `get ASYM_ScreenBounds` — `loc, dflt, workArea`
- `get ASYM_MonitorHandleList`
- `get ASYM_GetSystemColor` — `nm`
- `get ASYM_GetColorBrightness` — `rgb,n`
- `get ASYM_PrimaryMouseButton`
- `get ASYM_SetIniCompanyName` — `what`
- `get ASYM_SetIniUserName` — `nm`
- `get ASYM_TicksToTime` — `ms`
- `get ASYM_MouseScreenPos` — `units`
- `get ASYM_FontHeight` — `nm, sz, stle, units`
- `get ASYM_FontWidth` — `nm, sz, stle, units, what, data`
- `get ASYM_CalculateRequiredFieldHeight` — `fRef, lns, htPU`
- `get ASYM_GetScrollInfo` — `hWnd, which`
- `get ASYM_SetScrollInfo` — `hWnd, min, max, pgSize, value, which`
- `get ASYM_SpawnProcess` — `commandLine, showWindow, wait`
- `get ASYM_Copyright`
- `get ASYM_LogSetOptions` — `hdr, pgs, tms, ans, lck, stats`
- `get ASYM_LogStatus`
- `get ASYM_AskStudentName` — `prompt`
- `get ASYM_LogStart` — `bk, fn, appnd, enc, dest, typ`
- `get ASYM_LogStop`
- `get ASYM_LogTypeComboValues`
- `get ASYM_LogWriteEntry` — `txt`
- `get ASYM_LogDispatchComboValues`
- `handle ASYM_MailLogFile` — `fn,a,b,c`
- `handle _ASYM_ResetPgWidgets` — `msg`
- `handle _ASYM_ResetResponseData` — `_target`
- `handle ASYM_Locked`
- `get ASYM_ShortReference` — `ob`
- `get ASYM_ShowDialog` — `vRef, pRef, cptn, mode`
- `handle ASYM_ShowYourScore` — `ob, scr, mode, playFB`
- `get ASYM_WID_Score` — `mode, noUpdate, showFB`
- `get ASYM_CollectTotalScore` — `skp`
- `get ASYM_WID_Correctness` — `ob`
- `handle ASYM_PlayFeedback` — `ind, ob, mode, try`
- `get ASYM_CheckAnswerHyperlinks` — `ob`
- `handle ASYM_DoFeedback` — `ob, num, actualOb`
- `get ASYM_DoGenericTextFeedback` — `ob, tag, pos, option`
- `get ASYM_PlaySoundEffect` — `snd,sync`
- `handle ASYM_PlaySummaryFeedback` — `ob, try`
- `get ASYM_IniFile`
- `get ASYM_GetRuntimeIniVar` — `sxn, nm`
- `get ASYM_SetRuntimeIniVar` — `sxn, nm, val`
- `get ASYM_GetGlobalIniVar` — `sxn, nm`
- `get ASYM_SetGlobalIniVar` — `sxn, nm, val`
- `get ASYM_SetWorkWindow` — `object v`
- `get ASYM_WorkWindow`
- `get ASYM_DisableWindows`
- `get ASYM_EnableWindows` — `val`
- `get ASYM_ViewerContainer` — `ob`
- `handle killUserTooltipTimers`
- `get ASYM_LibrarianUniqueName` — `ob`
- `get ASYM_LibrarianUniqueNameInfo` — `ob, trunc`
- `get ASYM_LibrarianDisplayName` — `ob`
- `get ASYM_LMS_QuestionType`
- `get ASYM_LMS_GetAICCCompatibility` — `ob`
- `get ASYM_LMS_GetAICCSpec20` — `ob`
- `get ASYM_LMS_GetAICCPinnacleCompatibility` — `ob`
- `get ASYM_LMS_GetSCORM_ReportRawScore` — `ob`
- `get ASYM_GetFileDate` — `fn,frmt`
- `get ASYM_AddFileExtension` — `fn, ext`
- `get ASYM_ReplaceFileExtension` — `fn, ext`
- `get ASYM_GetTempFile` — `ext`
- `get ASYM_GetFileVersion` — `fn`
- `get ASYM_GetProductVersion` — `fn`
- `get ASYM_GetShortFileName` — `fn, opt`
- `get ASYM_GetLongFileName` — `fn, opt`
- `get ASYM_ExtensionName` — `ob`
- `get ASYM_FileFromCLSID` — `clsid`
- `get _ASYM_TBKFileVersion` — `fn`
- `get ASYM_FileToPrinter` — `fn, opts, hWnd, showAbort`
- `get ASYM_TextToPrinter` — `txt, opts, hWnd, showAbort`
- `handle ASYM_PrintWindow` — `hWnd, area, opts, xScl, yScl, jobNm, toTop, update, statusB`
- `handle ASYM_SaveWindowToFile` — `hWnd, area, fn, bits, compress, toTop, update, statusB`
- `get ASYM_PopGlossary` — `term, bk, styl, pos, captn, curs`
- `handle ASYM_PopGlossary` — `term`
- `get ASYM_PopupPage` — `object pgRef, popStyle, pos, captn, curs`
- `get ASYM_PopupWinComboValues`
- `handle ASYM_ShowPopupText` — `txt, pos`
- `handle ASYM_HidePopupText`
- `get ASYM_CompareDates` — `d1, d2, fmt`
- `get ASYM_DateToSeconds` — `d, fmt`
- `get ASYM_MillisecondsToTime` — `ms`
- `get millisecondsToTime` — `ms`
- `handle ASYM_PostMsg` — `msg, tgt`
- `handle ASYM_DoPostedMsg` — `msg, tgt`
- `get ASYM_IsMsgPosted` — `msg, tgt`
- `get ASYM_SetPostMsgBlock` — `pNewValue`
- `get ASYM_FlushPostMsgQueue`
- `get ASYM_Ellipsize` — `s, len, side`
- `get ASYM_EllipsizeFileToField` — `fld, file, fileOpt, dirOpt`
- `handle ASYM_LinkDLLs`
- `get ASYM_AskForPath` — `startPath, dbCaption`
- `get ASYM_WinHelp` — `cn, file`
- `get ASYM_IsWin31`
- `get ASYM_PopRTFHelp` — `fN, captn`
- `get ASYM_Wait` — `ms, breakKeys, yield`
- `get ASYM_Sleep` — `pMs`
- `get ASYM_UpdateTargetObject` — `ob`
- `get ASYM_DoProgressSingle` — `a,b,c,d,e,f`
- `get ASYM_DoProgressDouble` — `a,b,c,d,e,f,g,h,i,j,k`
- `handle ASYM_ShowProgress` — `n, maxN, captn`
- `handle ASYM_ShowProgressWithText` — `txt, n, maxN, captn`
- `handle ASYM_OpenEndedProgress` — `txt`
- `handle ASYM_ShowError` — `txt, winCaption, helpTag, helpFile`
- `get ASYM_ModalDialog` — `whatPage, whatCaption`
- `set ASYM_ModalState` — `to what`
- `get ASYM_MessageBox` — `txt,captn,icn,btns,hlpTag,hlpFile`
- `get ASYM_Ask` — `cptn,txt,icn,btns,defTxt,width,pos,frm,chk,rdio,hlp,lnk,moveCheckbox`
- `get ASYM_Request` — `cptn,txt,icn,btns,width,pos,frm,chk,rdio,hlp,lnk,moveCheckbox`
- `get ASYM_PopMenu` — `menuItemList, pos, rect`
- `get ASYM_INET_linkDLL`
- `get ASYM_GetFile_URL` — `rmtFn, locFn, overwrite, secSock`
- `get ASYM_GetFile_FTP` — `rmtSrv,rmtPrt,rmtDir,rmtFn,rmtUsr,rmtPW,locFn,overwrite,transType`
- `get ASYM_ActionsRuntimeLinked`
- `get TBK_VoiceRecordingControl` — `cmd, p1, p2`
- `get ASYM_Media_PlayerTable`
- `get ASYM_Media_PlayerIndexFromKey` — `key, val`
- `get ASYM_Media_FileIndexFromKey` — `key, val`
- `get ASYM_Media_PlayerInfo` — `idx, key`
- `get ASYM_Media_FileInfo` — `idx, key`
- `get ASYM_Media_MediaFilterList`
- `get ASYM_Media_PlayerIndex` — `fName, desc`
- `get ASYM_Media_FileIndex` — `fName`
- `get ASYM_Media_PlayerName` — `fName, desc`
- `get ASYM_Media_TimeFormat` — `fName`
- `get ASYM_Media_VideoSupport` — `fName, desc`
- `get ASYM_Media_ControlSupport` — `fName, desc`
- `get ASYM_GetDataElement` — `STACK data, STRING key, STRING dflt, validate`
- `get ASYM_SetDataElement` — `STACK data, STRING key, STACK val, validate`
- `get ASYM_GetStructureName` — `STACK data, validate`
- `get ASYM_GetElementList` — `STACK data`
- `get ASYM_SetStructureName` — `STACK data, val`
- `get ASYM_ForEachInit` — `STACK data, validate`
- `get ASYM_ForEachNext` — `structureID`
- `get ASYM_ForEachRelease` — `structureID`
- `get ASYM_NewDataStructure` — `nm`
- `get ASYM_IsDataStructure` — `STACK data`
- `get ASYM_ListToStack` — `STRING pList`
- `get ASYM_ArrayPropertyDataType` — `ob,prop`
- `get ASYM_InternationalFile` — `fn, validate`
- `get ASYM_QuickSortList` — `lst, asText`
- `get ASYM_QuickSortArray` — `lst[] by reference, txt`
- `get ASYM_QuickSortTable` — `lst[][] by reference, srtOrder, srtType`
- `handle ASYM_SyncTextValueWithList` — `ob, STRING txt, exact`
- `handle ASYM_SyncNumericValueWithList` — `ob, txt, exact`
- `handle ASYM_EnsureTextlineVisible` — `ob, ln`
- `get puToInches` — `pu`
- `get inchesToPU` — `inches`
- `get ASYM_PageUnitsToStandardUnits`
- `get ASYM_StandardUnitsToPageUnits` — `val, noRound`
- `get ASYM_GreatestCommonDivisor`
- `get ASYM_GreatestCommonDivisorArray` — `n[] by reference`
- `get ASYM_SelectObjectTarget` — `a,b,c,d,e,f,g,h,i`
- `get ASYM_SelectObjectFromList` — `obList, selType, cptn`
- `get ASYM_ObjectBitmapGroup` — `thisObj`
- `handle _ASYM_ReaderExit`
- `get ASYM_AltPgName` — `page ob`
- `get ASYM_ChooseFromTextLinesDlg` — `a,b,c,d,e`
- `get ASYM_decode` — `src, pw, ver`
- `get ASYM_HasAnsArray` — `ob`
- `get ASYM_HasFBArray` — `ob`
- `get ASYM_IsPointClose` — `a,b,c`
- `get ASYM_SuperEncode` — `txt, pwd`
- `get ASYM_GetDeploymentMethod` — `ob`
- `get ASYM_GetParameter` — `nm`
- `get getParameter` — `nm`
- `get ASYM_SetHTTPPostParameter` — `nm, val`
- `get ASYM_HTTPPost` — `url`
- `get httpPost` — `url`
- `get ASYM_IsObjectDirty` — `ob, bit`
- `get ASYM_IsObjectClean` — `ob, bit`
- `get ASYM_SetObjectClean` — `ob, bit`
- `get ASYM_IsPageDirty` — `whichPg, bit, bk`
- `get ASYM_IsPageClean` — `whichPg, bit, bk`
- `get ASYM_ReturnCleanPages` — `pgList, bit, bk`
- `get ASYM_ReturnDirtyPages` — `pgList, bit, bk`
- `get ASYM_SetPageClean` — `whichPg, bit, bk`
- `get ASYM_DisableBackup`
- `get ASYM_RestoreBackup`
- `handle ASYM_TimeMarker`
- `get ASYM_IsInstanceActive`
- `get TBK_Assert` — `cond, fatal, loc, str, r1, r2, r3, r4`
- `get ASYM_ItemOffset` — `itm, lst`
- `get ASYM_ItemContains` — `itm, lst`
- `get ASYM_ModalPopText` — `ttl, txt, pt`
- `get ASYM_CreateEncryptedFile` — `a,b`
- `get ASYM_CreateEncryptedFileEX` — `a,b,c`
- `get ASYM_WriteEncryptedFile` — `a,b,c`
- `get ASYM_GetMemBlock` — `a`
- `get ASYM_FreeMemBlock` — `a`
- `get ASYM_DecodeEX` — `a,b,c`
- `get ASYM_Encode` — `a,b`
- `get ASYM_EncodeEX` — `a,b,c`
- `get ASYM_SimpleHash` — `str`
- `get TBK_GdiPlus_BitmapFromBitmapResource` — `bitmapRef`
- `get TBK_GetBitmapResourceFileType` — `bitmapRef`
- `get TBK_GdiPlus_CreateBitmapFromFile` — `fileName`
- `get TBK_GdiPlus_GetImageGraphicsContext` — `pImage`
- `get TBK_GdiPlus_CreateBitmapFromGraphics` — `pGraphics, width, height`
- `get TBK_GdiPlus_CreateSimilarBitmap` — `pBitmap, width, height`
- `get TBK_GdiPlus_GetImageSize` — `pImage`
- `get TBK_GdiPlus_DrawImage` — `pGraphics, pBitmap, left, top`
- `get TBK_GdiPlus_CreateFont` — `pGraphics, fntFace, fntSize`
- `get TBK_GdiPlus_CreateFontFamily` — `fntFace`
- `get TBK_GdiPlus_GraphicsDpiY` — `pGraphics`
- `get TBK_GdiPlus_GraphicsDpiX` — `pGraphics`
- `get TBK_GdiPlus_GetGenericDefaultStringFormat`
- `get TBK_GdiPlus_CreateSolidFillBrush` — `brushColor`
- `get TBK_GdiPlus_DrawText` — `pGraphics, txt, fntFace, fntSize, left, top, width, height`
- `get TBK_GdiPlus_BitmapResourceFromBitmap` — `pDrawingBitmap, fileType`
- `get TBK_GdiPlus_GetEncoderClsid` — `mimeType`
- `get TBK_AnsiStringWideStringPointer` — `pWideString`
- `get TBK_WideStringPointerFromAnsiString` — `ansiString`
- `handle _linkDLLs`
- `handle _linkSysBook`
- `handle _doNeuronCheck`
- `handle _unLinkSysBook`
- `handle initSysBooks`
- `get SetSysBooksInOrder` — `bkFnList`
- `get shortFileName` — `fName`
- `get _ASYM_Ellipsize` — `s, len, side`
- `get _ASYM_EllipsizeFileToField` — `pField, pFileName, pFileOpt, pDirOpt`
- `handle cleanupDuplicateSysbooks`
- `handle _enterApplication` — `targetRef`
- `handle _leaveApplication`
- `handle _enterBook` — `targetRef`
- `handle _leaveBook`
- `handle _enterWindow` — `targetRef, vRef`
- `handle _destroy` — `targetRef`
- `handle sendPageEntered`
- `handle _rightButtonDown` — `targetRef, loc, sh, ct`
- `handle _rightButtonUp` — `targetRef, loc`
- `handle _CMS_EnterApplication` — `bk, bookmarkFn`
- `get blockSuspend` — `stckFull`
- `get restoreSuspend` — `opts`
- `get _ASYM_TBDLLErrorString` — `pDLL, pFunctionName, pErrorCode`
- `get _ASYM_PopupPage` — `object pgRef, popStyle, pos, captn, curs, fx`
- `get _ASYM_PopupWinComboValues`
- `handle _AutoCloseCheck` — `loc`
- `get viewerScript`
- `get _FindExecutableFile` — `fn`
- `get _ASYM_IsDirectoryWriteable` — `dirSpec`
- `get _ASYM_IsDriveReady` — `drv`
- `get _ASYM_IsFileAvailable` — `fN`
- `get _ASYM_MakeIntoRelPath` — `rootPath,longPath`
- `get _ASYM_SetCurrentDirectory` — `pathStr`
- `get _ASYM_SetPath` — `pathName, path`
- `get _ASYM_IsValidDrive` — `path, retry, prompt`
- `get _ASYM_CurrentDirectory`
- `get _ASYM_FindPathFile` — `fName, path, bkPath`
- `get _ASYM_FreeDiskSpace` — `drspec`
- `get _ASYM_GetPath` — `pathName`
- `get _ASYM_IsDirectory` — `dirspec`
- `get _ASYM_RelativePath` — `path, bkName`
- `get _ASYM_WindowsDirectory`
- `get _ASYM_IsAbsoluteFilePath` — `pFileName`
- `get _ASYM_RecurseCreateDirectory` — `dir`
- `get _ASYM_ParentDirectory` — `dir`
- `get _ASYM_ParsePath` — `path, op`
- `get ASYM_FileDotPosition` — `fileName`
- `get _ASYM_AppendFileToPath` — `dir, fn`
- `get _ASYM_ExpandRelPath` — `otherPath, rootPath`
- `get _ASYM_ResolvePath` — `filePath`
- `get _ASYM_ConvertPathToList` — `path`
- `get _ASYM_ConvertListToPath` — `pathList`
- `get _ASYM_RecurseRemoveDirectory` — `dir, options`
- `get _ASYM_FindMediaFile` — `pFilename, pBook, pSearchHD, pSearchCD, pSearchHyperPath`
- `get _ASYM_ExpandMediaPath` — `pPaths, pBook`
- `get _ASYM_FileRelativeToMedia` — `pFilename, pBook, pSearchHD, pSearchCD, pSearchHyperPath`
- `get _ASYM_PromptForCDROM` — `pFilename, pMessage, pCaption`
- `get _ASYM_FindFileOnCDROM` — `pFilename`
- `get _ASYM_PathOfFile` — `pPath`
- `get _ASYM_ShortFileName` — `pPath`
- `get _ASYM_TempDir`
- `get _ASYM_ExpandEnvironmentStrings` — `str`
- `get standardFolder` — `folderName`
- `get VoiceRecordingControl` — `cmd, p1, p2`
- `get recordingFolderPath` — `p1`
- `get constructFileRef` — `pgRef`
- `get playerKeyList`
- `get fileKeyList`
- `get playerTable`
- `get fileTable`
- `handle addArrayItem` — `itemArray[][] by reference`
- `get playerIndexFromKey` — `pInfoKey, pValue`
- `get fileIndexFromKey` — `pInfoKey, pValue`
- `get indexFromKey` — `pInfoKey, pValue, mediaTable[][] by reference, nameKeys`
- `get playerInfo` — `pIndex, pInfoKey`
- `get fileInfo` — `pIndex, pInfoKey`
- `get mediaInfo` — `pIndex, pInfoKey, mediaTable[][] by reference, nameKeys`
- `get mediaFilterList`
- `get playerIndex` — `fName, playerDesc, targetRef`
- `get fileIndex` — `fName, targetRef`
- `get playerName` — `fName, playerDesc, targetRef`
- `get timeFormat` — `fName, targetRef`
- `get videoSupport` — `fName, playerDesc, targetRef`
- `get controlSupport` — `fName, playerDesc, targetRef`
- `handle disableTaskSwitching` — `how`
- `handle _WM_SYSCOMMAND` — `hWnd, wMsg, wp, lp`
- `handle _sized` — `sizedObj, tbk_wid_type`
- `handle _ASYM_SizeButtonToGraphic` — `pTarget, pObj`
- `get isPointClose` — `p1,p2, dist`
- `get createButtonGraphic` — `masterRef, targetSize, margins, marginScale`
- `get createButtonGraphicGdiPlus` — `masterRef, targetSize, sourceWidth, sourceHeight, targetWidth, targetHeight, marginLeft, marginTop, marginRight, marginBottom`
- `get TBK_GdiPlus_DrawImageRectRect` — `pGraphics, pBitmap, targetX, targetY, targetWidth, targetHeight, sourceX, sourceY, sourceWidth, sourceHeight`
- `get TBK_GdiPlus_DrawImagePointRect` — `pGraphics, pBitmap, targetX, targetY, sourceX, sourceY, sourceWidth, sourceHeight`
- `get createButtonGraphicGdi` — `masterRef, targetSize, sourceWidth, sourceHeight, targetWidth, targetHeight, marginLeft, marginTop, marginRight, marginBottom`
- `get sizedBitmapName` — `masterName, targetSize`
- `get _ASYM_MakeBookmarkFileName`
- `get _readBookmarks` — `bookmarkFn`
- `get _writeBookmarks` — `bookmarkFn`
- `get readNextLine` — `fN`
- `get _AskStudentName` — `prompt`
- `handle _ASYM_CollectLogResponseData` — `sep`
- `get _ASYM_LogDispatchDirectory` — `LogDest`
- `get _ASYM_LogStart` — `bk, fName, logAppend, encryptIt, dest, typ, CMSLogFileName, CMSLogFileType`
- `get _ASYM_LogStop`
- `get _ASYM_LogTypeComboValues`
- `get _ASYM_MakeLogFileName` — `dest, logFn`
- `get IsRoomOnDisk` — `d`
- `get _ASYM_LogWriteEntry` — `txt`
- `get _ASYM_LogSetOptions` — `heading, logPages, logTimes, logAnswers, logOnLock, logStats`
- `get _ASYM_LogStatus`
- `get _ASYM_decode` — `source, password, ver`
- `handle _ASYM_LogDispatch` — `LogFileName, LogDest,\`
- `get _ASYM_LogDispatchComboValues`
- `handle _ASYM_MailLogFile` — `LogFileName, EmailLogRecipients,\`
- `get getMAPIErrorString` — `nErrorNumber`
- `get IsMAPIAvailable`
- `handle linkMAPI`
- `get logPrintDefaults`
- `handle mailDriverError` — `fName, EmailLogRecipients`
- `handle mailSendError` — `fName, EmailLogRecipients`
- `handle RequestDeleteTempFile` — `fN, titl`
- `handle ConfirmLogMailedOK` — `fN, titl, bConfirm`
- `get sendFile` — `fileName`
- `get SessionLogOff`
- `get SessionLogOn`
- `handle showLogMailError` — `fName, EmailLogRecipients`
- `get str_OK`
- `get ASYM_MAPISendMessage` — `recips,subject,msgText,attachments`
- `get _ASYM_FindFaxDriver`
- `get SendLogAsFax` — `fN, printdefaults, faxDevice`
- `handle AutoGlossary` — `hotWrd`
- `handle autoHotword` — `fld, loc`
- `get _asym_IsWin31`
- `get _ASYM_WinHelp` — `what, whatFile`
- `get _ASYM_AddString` — `strgName, s, tgt`
- `get _ASYM_ClearString` — `strgName, tgt`
- `get __ASYM_FindString` — `fixed strgs[][] by reference, strgName`
- `get _ASYM_GetStandardString` — `pTarget, strgName, strgDflt`
- `get _ASYM_GetString` — `pTarget, strgName, strgDflt`
- `get _ASYMA_GetStringList` — `pTarget`
- `get GetStringTargetBook` — `pTarget`
- `get _ASYM_Wait` — `ms, breakKeys, yield`
- `get _ASYM_Sleep` — `pMs`
- `get _ASYM_CompareDates` — `d1, d2, fmt`
- `get _ASYM_DateToSeconds` — `d, fmt`
- `get _ASYM_MillisecondsToTime` — `ms`
- `get _ASYM_FileToPrinter` — `fn, options, hParentWnd, showAbortDlg`
- `get _ASYM_TextToPrinter` — `txt, options, hParentWnd, showAbortDlg`
- `get cleanUpText` — `pText`
- `get PrintBand` — `hDC, lpRectOut, lpRectClip, lpDIBHdr, lpDIBBits`
- `get PrintDIB` — `hDib, fPrintOpt, wXScale, wYScale, szJobName`
- `handle printWindow` — `hWnd, wPrintArea, wPrintOpt, wXScale, wYScale, szJobName, toTop, update, statusB`
- `get doPrintWindow` — `hWnd, wPrintArea, wPrintOpt, wXScale, wYScale, szJobName`
- `get CalculatePrintRect` — `hDC, lpPrintRect, fPrintOpt, cxDIB, cyDIB`
- `get CopyWindowToDIB` — `hWnd, fPrintArea, bitCount, Compress`
- `get CopyScreenToDIB` — `lpRect, bitCount, Compress`
- `get CopyScreenToBitmap` — `lpRect`
- `get BitmapToDIB` — `hBitmap, hPal, bitCount, Compress`
- `get FindDIBBits` — `lpDIB`
- `get DIBNumColors` — `lpDIB`
- `get GetSystemPalette`
- `get PalEntriesOnDevice` — `hDC`
- `get PaletteSize` — `lpDIB`
- `get SaveDIBToFile` — `hDib, lpFileName`
- `get DIBError` — `ErrNo`
- `get getViewerName` — `whatViewer`
- `handle linkDlls`
- `handle saveWindowToFile` — `hWnd, wPrintArea, FileName, bitCount, compress, toTop, update, statusB`
- `get doSaveWindow` — `hWnd, printArea, fileName, bitCount, compress`
- `get GetPrinterDC` — `forPrinter   --32`
- `get _ASYM_IsObjectDirty` — `obRef, whichBit`
- `get _ASYM_IsObjectClean` — `obRef, whichBit`
- `get _ASYM_IsPageDirty` — `whichPg,whichBit,whichBk`
- `get _ASYM_IsPageClean` — `whichPg,whichBit,whichBk`
- `get _ASYM_ReturnCleanPages` — `pgList,whichBit,whichBk`
- `get _ASYM_ReturnDirtyPages` — `pgList,whichBit,whichBk`
- `get _ASYM_SetObjectClean` — `obRef, whichBit`
- `get _ASYM_SetPageClean` — `whichPg,whichBit,whichBk`
- `get modBit` — `whichBit`
- `get getDirtyBitsObject` — `obRef`
- `get _ASYM_GetParameter` — `paramName`
- `get replaceEscapeChars` — `txt`
- `get _ASYM_SetHTTPPostParameter` — `paramName, paramValue`
- `get _ASYM_HTTPPost` — `url`
- `get escapeChars` — `txt`
- `handle _ASYM_PostMsg` — `msg, tgt`
- `handle _ASYM_DoNextPostedMsg`
- `handle _ASYM_DoPostedMsg` — `hWnd, msgID`
- `get _ASYM_IsMsgPosted` — `msg, tgt`
- `get _ASYM_SetPostMsgBlock` — `pNewValue`
- `get _ASYM_FlushPostMsgQueue`
- `handle _ASYM_FlushMsgQ`
- `handle _ASYM_Reset` — `targetRef, mode, pResetTargetPage`
- `handle _ASYM_ResetPgWidgets` — `msg, setBeenHere`
- `handle sizeButtonToGraphic` — `obj`
- `handle sizeImageToGraphic` — `obj`
- `handle _ASYM_Locked` — `_target`
- `handle _ASYM_ResetRespData` — `_target`
- `handle _ASYM_ResetTestItem` — `QType, mode, _target`
- `get _ASYM_ShortReference` — `obj`
- `get _ASYM_ShowDialog` — `whatViewer, whatPage, whatCaption, whatMode`
- `handle _fixAnsArray` — `obj`
- `handle ASYM_QuestionLoad` — `mode, index, _target`
- `get ASYM_CleanState` — `pageRef`
- `set ASYM_CleanState` — `pageRef to cleanState`
- `handle AutoSizeCheck` — `tgt`
- `get _ASYM_WID_Responses` — `obj`
- `get _ASYM_BeginResponse` — `actualObj, respName, _target, resetToOld`
- `get _ASYM_CheckPoint` — `obj, loc, _target`
- `handle _ASYM_GetTypeInData` — `_target`
- `handle _ASYM_RegisterResponse` — `actualObj, respName, _target`
- `handle _moveObj` — `obj, _target`
- `get testExpressionWithX` — `expr, x`
- `get ASYM_cepr` — `s`
- `get ASYM_matchString` — `STRING testString, STRING refString, \`
- `get ASYM_SoundsLike` — `s1, s2`
- `get ASYM_stripPunctuation` — `whatText`
- `get defaultPhRules`
- `get defaultPhVowels`
- `handle LockAndAdjustTestItem` — `_target, actualObj, respName, QType`
- `get matchJumbledWords` — `STRING testString, ARRAY wrdList[],LOGICAL byCase`
- `get SetElapsedTime` — `_target, newTimeChosen`
- `get _cleanUp` — `txt`
- `handle _ASYM_CheckDropObj` — `pTarget, obj, loc`
- `get _ASYM_RegisterAttempt` — `pTarget, _target, mode, showFeedback, correctness, score`
- `handle _ASYM_CheckTries` — `pTarget, _target`
- `get _ASYM_FindAnswerIndex` — `pTarget, whatItem, col, all`
- `handle _ASYM_QLocked` — `obj, response`
- `handle _ASYM_QResponded` — `obj, response`
- `handle _ASYM_TypeInCompleted` — `pTarget, txt, stat, entryField`
- `get _ASYM_QuestionStatus` — `pTarget, obj, _score, mode, noUpdate, showFeedback`
- `handle handleButtonDown` — `loc, targetRef`
- `get _ASYM_DoGenericTextFeedback` — `obj, tag, pos, option`
- `get _ASYM_PlayAnswerFeedback` — `answerIndex, obj, actualObj`
- `get _ASYM_PlaySummaryFeedback` — `obj, actualObj, registerTry`
- `get _PlayFeedbackItem` — `fbArray[][] by reference, num, obj, actualObj, notSummary`
- `get isMediaFile` — `snd`
- `get _upgrade3SummaryFeedback` — `obj`
- `handle mmnotify` — `clipRef, cmd, result`
- `get _SmartPlaySound` — `snd, sync`
- `get _ASYM_CheckAnswerHyperlinks` — `obj`
- `handle _ASYM_PlayFeedback` — `pTarget, index, actualObj, mode, pRegisterTry`
- `handle ASYM_ShowYourScore` — `obj, score, mode, playFB, _target`
- `handle _ASYM_ShowYourScore` — `obj, score, mode, playFeedback, _target`
- `get _ASYM_WID_Correctness` — `_target`
- `get _ASYM_WID_Score` — `_target, mode`
- `get _ASYM_CollectTotalScore` — `includeSkip`
- `handle DoDragObject` — `tgt, obj, loc, whatButton`
- `handle DoMatchItemDrag` — `tgt, obj, loc, whatButton`
- `get _UpdateTargetObject` — `obj`
- `get _ASYM_Is32Bit`
- `get monitorContaining` — `where, defaultMonitor`
- `get monitorBounds` — `where, defaultMonitor, workArea`
- `get getPrimaryMonitorBounds` — `workArea`
- `get ScreenInfo`
- `get getSystemColor` — `sysColor`
- `get getColorBrightness` — `rgbColor, useNonLinearMethod`
- `get RGBtoXYZ` — `RGB`
- `get primaryMouseButton`
- `get setIniCompanyName` — `what`
- `get setIniUserName` — `what`
- `get ticksToTime` — `ms`
- `get mouseScreenPos` — `pReturnType`
- `get calculateRequiredFieldHeight` — `fRef, numLines, fontHeightTwips`
- `get fontHeight` — `fontName, fontHeightPoints, fontInfo, units`
- `get guessFontHeight` — `fontHeightPoints`
- `get fontWidth` — `fontName, fontHeightPoints, fontInfo, units, what, data`
- `get getScrollInfo` — `hWnd, which`
- `get setScrollInfo` — `hWnd, min, max, pgSize, value, which`
- `get monitorHandleList` — `pos, monitorList`
- `get SpawnProcess` — `commandLine, showWindow, wait`
- `get SpawnProcessAsynch` — `commandLine, showWindow`
- `get _ASYM_CBTIniVar` — `section, key, deflt`
- `get _ASYM_GetSystemVar` — `varName`
- `get _ASYM_RandomList` — `numItems, inList`
- `get _ASYM_ProductDirectory`
- `get _ASYM_LongProductDirectory`
- `get _ASYM_SystemDirectory`
- `get _ASYM_DrawFocusRect` — `pBounds, pViewer`
- `get _ASYM_DeleteHandler` — `obRef, handlerName`
- `get _ASYM_DisableBackup`
- `get _ASYM_RestoreBackup`
- `get _ASYM_GetDeploymentMethod` — `ob`
- `get _ASYM_MessageBox` — `txt, titl, icn, btns, hlpTag, hlpFile`
- `handle F1Pressed`
- `get _ASYM_ColorPaletteDlg` — `r, g, b`
- `get _ASYM_chooseColorDlg` — `r, g, b`
- `get _ASYM_ChooseFontDlg` — `a, b`
- `get _ASYM_OpenFileDlg` — `a, b, c, d, e`
- `get _ASYM_OpenFileDlgLFN` — `a, b, c, d, e`
- `get _ASYM_SaveAsDlg` — `a, b, c, d, e`
- `get _ASYM_ChooseDirectoryDlg` — `a, b`
- `get _ASYM_ChooseDirectoryDlgLFN` — `a, b`
- `get _ASYM_SaveAsDlgLFN` — `a, b, c, d, e`
- `get _ASYM_LockWindows`
- `get _ASYM_UnlockWindows` — `winDetails`
- `get __ASYM_SysCursor`
- `get _ASYM_WorkingCursor` — `pShow`
- `get _ASYM_CursorInResizeHandle`
- `handle _ASYM_ElapsedCursor` — `nmax, n, curName`
- `get getResizeTarget` — `pos`
- `get cursorSelectionHandle` — `pos, obRef`
- `get midPoint` — `p1, p2, px`
- `get selectionHandleRect` — `x, y`
- `get pointInRect` — `pt, rect`
- `get ASYM_DuplicateClip` — `clipRef`
- `get ASYM_IsClip` — `STRING pClip, pTargetBook`
- `get _ASYM_ViewerContainer` — `pObjRef`
- `get _ASYM_SetWorkWindow` — `object v`
- `get _ASYM_WorkWindow`
- `get _ASYM_DisableWindows`
- `get _ASYM_EnableWindows` — `val`
- `handle showToolbar`
- `handle showColorTray`
- `get _ASYM_ClearClipboard`
- `get _ASYM_CopyTextToClipboard` — `clipText`
- `get _ASYM_checkHyperSysBook`
- `get _ASYM_EnableHyperlinks`
- `get _ASYM_GlossaryPage` — `term, bkName`
- `get _ASYM_NumberToRoman` — `num, case, formatStyle`
- `get _ASYM_RomanToNumber` — `rom`
- `get _ASYM_CompareByCase` — `string1, string2`
- `get _revOffset` — `s1, s2`
- `get _ASYM_Trim` — `s`
- `get _wordContains` — `x, txt`
- `get _wordOffset` — `x, txt`
- `get _ASYM_FindWordStart` — `whatText, whatChar, whatLine`
- `get _ASYM_Offset` — `str, src, pos`
- `get _ASYM_ReverseStack` — `STACK stk`
- `get _ASYM_StringOf` — `str, cnt`
- `get _ASYM_TextlineFromPos` — `pPos, pText`
- `get _ASYM_SplitWordsOnCaps` — `txt`
- `get ASYM_EllipsizeFilenameInText` — `txt, fRef`
- `get ASYM_GetAvailableTextWidth` — `fRef`
- `get _getLongDate`
- `get ansiStringWideStringPointer` — `pWideString`
- `get wideStringPointerFromAnsiString` — `ansiString`
- `get _ASYM_TextlineOffset` — `x, txt, pos`
- `get _ASYM_FindField` — `fldName, pg`
- `get _ASYM_FindPage` — `pgN`
- `get _ASYM_GetObjectListByName` — `oContainer, otype, hasScript, nam`
- `get _ASYM_NameOrID` — `obj`
- `get _ASYM_ObjectCenter` — `pTarget, obj`
- `handle _ASYM_SetObjectCenter` — `pTarget, loc`
- `get _ASYM_OppositePos` — `pos`
- `handle _ASYM_ScrollListBoxToSelection` — `pTarget`
- `get _ASYM_WordFromPoint` — `loc`
- `handle _ASYMA_CopyUserProperties` — `obj1, obj2`
- `handle _ASYM_FixFieldScrollBar` — `pTarget, fld`
- `get _ASYM_CopyProperty` — `pSourceObj, pDestObj, pSourceProp, pDestProp`
- `get _ASYM_ObjectParentList` — `pObj, pCutOffLevel`
- `get ASYM_ConstructObjectIdentifier` — `objectRef, targetRef, noSelf, thisPage, layerRef`
- `get ASYM_ObjectDescriptionFromObjectInfo` — `obInfo, selfRef, event, initCaps, obRef`
- `get ASYM_ResolveObject` — `objectInfo, selfRef, targetRef, validate`
- `get ASYM_ResolveBookName` — `bookName, targetRef`
- `get ASYM_ResolvePage` — `pageName, pageID, bookRef, targetRef`
- `get ASYM_ResolveViewer` — `viewerName, viewerID, bookRef, targetRef`
- `get ASYM_ResolveBackground` — `bgName, bgID, bookRef, targetRef`
- `get ASYM_FindObject` — `objectType, objectName, objectID, layerRef, targetRef`
- `get ASYM_RelativeObjectDescription` — `targetRef, selfRef, initCaps, event`
- `handle ASYM_RegisterPath` — `path, targetRef`
- `get _ASYM_ObjectsWhere` — `ownerObj, objTypes, express`
- `get questionText` — `tgt, _option, _specifiedText, _specifiedField`
- `get getQuestionTextField` — `tgt, _specifiedField`
- `get getQuestionTextAutoFields` — `tgt`
- `get findQuestionTextField` — `qnRef`
- `handle _trigger` — `targetRef`
- `get _ASYM_LMS_UniqueName` — `obRef`
- `get _ASYM_LMS_UniqueNameInfo` — `obRef, truncateFlag`
- `get _ASYM_LMS_DisplayName` — `obRef`
- `get _ASYM_LMS_QuestionType` — `obj`
- `get getAICCCompatibility` — `ob`
- `get getAICCSpec20` — `ob`
- `get getAICCPinnacleCompatibility` — `ob`
- `get getSCORM_ReportRawScore` — `ob`
- `get _ASYM_GetFileDate` — `fName, formatString`
- `get _ASYM_AddFileExtension` — `fn, ext`
- `get _ASYM_ReplaceFileExtension` — `fn, ext`
- `get _ASYM_GetFileVersion` — `fName, productFlag`
- `get _ASYM_GetTempFile` — `pExt`
- `get _ASYM_GetShortFileName` — `fName, opt`
- `get _ASYM_GetLongFileName` — `fName, opt`
- `get _TBK_openAcrobatFile` — `fRef, showWarning`
- `get _ASYM_ExtensionName` — `ob`
- `get _ASYM_FileFromCLSID` — `pCLSID`
- `get _ASYM_PopMenu` — `menuItemList, pos, rect`
- `get buildMenu` — `menuItemList, vRef, hMenu, pMenuItemInfo, pMenuText, delimitByCRLF, parentItem`
- `get _ASYM_INET_linkDLL`
- `get _ASYM_GetFile_URL` — `pRemoteFile, pLocalFile, pOverWrite, pSecureSocket`
- `get _ASYM_GetFile_FTP` — `pRemoteServer, pRemotePort, pRemoteDir, \`
- `get INetNotifyResolvingName` — `pAlias, pName`
- `get INetNotifyNameResolved` — `pAlias, pName`
- `get INetNotifyConnecting` — `pAlias`
- `get INetNotifyConnected` — `pAlias`
- `get INetNotifySending` — `pAlias, pRequestHeaders`
- `get INetNotifySent` — `pAlias`
- `get INetNotifyReceivingResponse` — `pAlias`
- `get INetNotifyReceivedResponse` — `pAlias, pResponseHeaders, DWORD pBytesReceived`
- `get INetNotifyClosingConnection` — `pAlias`
- `get INetNotifyClosedConnection` — `pAlias`
- `get INetNotifyRequestComplete` — `pAlias`
- `get INetNotifyCopyProgress` — `pAlias, DWORD pBytesCopied, DWORD pTotalBytesToCopy`
- `get INetNotifyCopyComplete` — `pAlias, DWORD pBytesCopied`
- `get ASYM_SetDataElement` — `stack dataStructure, string elementName, stack elementValue, validate`
- `get ASYM_GetDataElement` — `stack dataStructure, string elementName, defaultValue, validate`
- `get ASYM_GetElementList` — `STACK dataStructure`
- `get ASYM_GetStructureName` — `STACK dataStructure, validate`
- `get ASYM_IsDataStructure` — `STACK dataStructure`
- `get ASYM_GetDataElement_Old` — `STACK dataStructure, STRING key, STRING default`
- `get ASYM_SetDataElement_Old` — `STACK dataStructure, STRING key, STRING value`
- `get ASYM_GetStructureName_Old` — `STACK dataStructure`
- `get ASYM_SetStructureName` — `STACK dataStructure, value`
- `get ASYM_SetStructureName_Old` — `STACK dataStructure, value`
- `get ASYM_GetElementList_Old` — `STACK dataStructure`
- `get ASYM_ExpandSpecialChars` — `STRING txt`
- `get ASYM_ReplaceSpecialChars` — `STRING txt`
- `get ASYM_Offset` — `str, src, pos`
- `get ASYM_ForEachInit` — `STACK dataStructure, validate`
- `get ASYM_ForEachNext` — `structureID`
- `get ASYM_ForEachRelease` — `structureID`
- `get ASYM_ListToStack` — `STRING pList`
- `get _asym_ArrayPropertyDataType` — `obj, prop`
- `get typeDataCheck` — `obj, prop, curType, dims`
- `get hash` — `str`
- `get _ASYM_InternationalFile` — `pFileName, pValidateFile`
- `get ASYM_QuickSortArray` — `lst[] by reference, asText`
- `get ASYM_QuickSortTable` — `lst[][] by reference, sortOrder, sortType`
- `get compare` — `val1, val2, datatype`
- `get ASYM_QuickSortList` — `lst, asText`
- `get quickSort` — `data[] by reference, STACK lStack, STACK rStack`
- `get quickSortText` — `data[] by reference, STACK lStack, STACK rStack`
- `handle _ASYM_SyncTextValueWithList` — `FIELD fRef, STRING testText, exactFit`
- `handle _ASYM_SyncNumericValueWithList` — `FIELD fRef, testText, exactFit`
- `handle _ASYM_EnsureTextlineVisible` — `FIELD fRef, currentLine`
- `get _ASYM_PageUnitsToStandardUnits`
- `get _ASYM_StandardUnitsToPageUnits` — `value, noRounding`
- `get gcd` — `nums[] by reference`
- `get bitmapFromBitmapResource` — `bitmapRef`
- `get getBitmapResourceFileType` — `bitmapRef`
- `get createBitmapFromFile` — `fileName`
- `get getImageGraphicsContext` — `pImage`
- `get createBitmapFromGraphics` — `pGraphics, width, height`
- `get createSimilarBitmap` — `pBitmap, width, height`
- `get getImageSize` — `pImage`
- `get createGdiPlusFont` — `pGraphics, fntFace, fntSize`
- `get createGdiPlusFontFamily` — `fntFace`
- `get graphicsDpiY` — `pGraphics`
- `get graphicsDpiX` — `pGraphics`
- `get getGenericDefaultStringFormat`
- `get createGdiPlusSolidFillBrush` — `brushColor`
- `get drawGdiPlusText` — `pGraphics, txt, fntFace, fntSize, left, top, width, height`
- `get bitmapResourceFromBitmap` — `pDrawingBitmap, fileType`
- `get getEncoderClsid` — `mimeType`
- `get tooltip` — `targetRef`
- `handle doToolTip` — `targetRef`
- `handle timerNotify` — `timerID`
- `handle showTooltip`
- `get getTooltipInfo`
- `handle hideTooltip` — `targetRef`
- `handle _killTooltipTimers`
- `handle ASYM_ShowPopupText` — `txt, pos`
- `handle buttonClick`
- `handle ASYM_HidePopupText`
- `handle resizeField` — `obj, fixedWidth, minWidth, maxWidth, textRightMargin`
- `get repairFieldWidth` — `obj, min, max`
- `get repairFieldHeight` — `obj, maxHeight`
- `handle ASYM_Reset`
- `get htmlToRichText` — `txt`
- `handle setRichText` — `obRef, txt`
- `get doProgress` — `mainCaption, progressCaption, progressValue, progressMax, viewerCaption, noCancel`
- `get checkCancel` — `vRef`
- `get TBK_Theme_ApplyButtonGraphic` — `targetRef, buttonStateString, switching, buttonSize`
- `get TBK_Theme_GetButtonGraphic` — `buttonStateString, userBitmapRef, transparentColor, captionText, captionTextPosition, buttonSize`
- `get calcButtonElementPositions` — `buttonSize, contentMargins, captionSize, bitmapSize, captionTextPosition`
- `get TBK_Theme_GetThemeSysFont` — `hTheme, fontType`
- `get TBK_Theme_GetButtonMasterSize` — `buttonStateString`
- `get TBK_Theme_GetButtonContentMargins` — `buttonStateString`
- `get TBK_Theme_GetButtonSizingMargins` — `buttonStateString`
- `get TBK_Theme_GetButtonCaptionMargins` — `buttonStateString`
- `get TBK_Theme_GetButtonMargins` — `buttonStateString, marginType`
- `get TBK_Theme_OpenThemeData` — `themeClass`
- `get TBK_Theme_GetCurrentThemeName`
- `get TBK_Theme_IsThemeActive`
- `get TBK_Theme_GetButtonStateFromString` — `buttonStateString`
- `get TBK_Theme_GetGraphicName` — `buttonState`
- `get TBK_Theme_GetButtonStateString` — `buttonState`
- `get TBK_Theme_GetTextSize` — `hTheme, hDC, themePart, themePartState, txt`
- `get ansiStringWideStringPointer` — `pWideString`
- `get wideStringPointerFromAnsiString` — `ansiString`
- `get hash` — `str`
- `get sizedBitmapName` — `masterName, targetSize`
- `handle ASYM_Reset`
- `handle restoreDefaultSize`
- `handle initializeObjectReferences`
- `get doProgress` — `mainCaption, progress1Caption, progress1Value, progress1Max, progress2Caption, progress2Value, progress2Max, viewerCaption, noCancel, confirmCancel, progressBounds`
- `get checkCancel` — `vRef, cancelRef, confirmCancel`
- `get confirmCancel` — `confirmCancel`
- `handle refreshLayout` — `bgSize, showMainCaption, mainCaptionVisibilityChanging, showCancel, cancelVisibilityChanging, fixedBounds`
- `get _ASYM_ChooseFromTextLinesDlg` — `dlgCaption, prompt, txtLines, deflt, helpTopicOrID`
- `handle enterPage`
- `handle Cancel`
- `handle closeThisWindow`
- `handle firstIdle`
- `handle idle`
- `handle OK`
- `set customSize` — `to what`
- `handle ASYM_Reset`
- `get _asym_ask_request` — `_caption, _text, _icon, _buttons, _type, _defText, _width, _position, _frame, _check, _radio, _help, _parseForLinks, _bottomCheckbox`
- `get stripSpecial` — `str, lst`
- `get findSpecial` — `str, lst`
- `handle resizeButtons`
- `get XpixelToPU` — `val`
- `get YpixelToPU` — `val`
- `handle resizeField` — `obj, fixedWidth, minWidth, maxWidth, textRightMargin`
- `get repairFieldWidth` — `obj, min, max`
- `get repairFieldHeight` — `obj, maxHeight`
- `get myPage`
- `get parseButtons` — `_buttons`
- `get screenWidth`
- `get screenHeight`
- `handle Paste`
- `get mnemonicChar` — `str`
- `handle keyChar` — `key`
- `handle buttonClick`
- `handle buttonClick`
- `handle keyDown` — `key`
- `get moveDefRect` — `object defRect, object obj`
- `get hideDefRect`
- `get resetRect` — `object oldObj`
- `get createDefRect` — `logical isBG`
- `get defaultRect` — `logical isBackground`
- `get pushButtonList`
- `get defPushButton`
- `get escPushButton`
- `get isBackground` — `obj`
- `get showDefRect`
- `get showRect` — `obj`
- `get _ASYM_PopRTFHelp` — `fN, captn`
- `handle ASYM_Reset`
- `handle cancel`
- `handle copy`
- `handle fixScroll` — `fld`
- `handle fixSize`
- `handle keyUp` — `x, iss, isc`
- `handle leavePage`
- `handle windowSized`
- `get _ASYM_SelectObjectTarget` — `pReturnType, pFullReference, pTargetWindow, pObjectTypes, pNamedOnly, \`
- `get processGroupStuff` — `thisObj, topLevelOnly, allowGroups, exportableOnly`
- `get includeThisObj` — `pObj, pObjectsToInclude`
- `get ignoreThisObj` — `pObj, pObjectsToIgnore`
- `get validateObject` — `thisObj, objectsToInclude, objectsToIgnore, validObjectTypes, returnNamedOnly, objectsWhere`
- `get findValidObjectType` — `thisObj, validObjectTypes`
- `get findNamedObject` — `thisObj, returnNamedOnly`
- `get findObjectWhere` — `thisObj, objectsWhere`
- `get ASYM_SelectObjectFromList` — `pObjList, selectType, pDialogTitle`
- `handle init` — `pObjList`
- `handle OK`
- `handle cancel`
- `get ASYM_ObjectBitmapGroup` — `thisObj`
- `handle enterBackground`
- `get actualMediaSize` — `STACK pFrameSizeInPageUnits`
- `get nonMediaAreaStageSizes`
- `get windowCaptionHeight`
- `get windowBorderHeight`
- `get windowBorderWidth`
- `handle buttonDown`
- `handle updateMedia` — `frame`
