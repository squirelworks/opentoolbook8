# Instructor 8.1 headless analysis

Tool: Ghidra 12.2 PUBLIC, built 2026-Oct-16, revision `8ca9077040cc43cd790babcfccf19475622a3e9a`, with the squirreldra Win16 loader patch at commit `ff0ef27`. That patch bounds the NE entry table by `ne_cbenttab`, treats the entry-bundle segment index as unsigned, and adds the `__pascal16far` and `__pascal16near` prototypes. Each headless run used normal analysis, then `Win16NEFixes.java` and `ExportDecompile.java`, from `/tmp/ghidra-scripts-clean`. Projects are under `/tmp/squirreldra-projects-clean`. Exports are under `/tmp/squirreldra-out-clean/` and are not in this repository. Every imported file finished with headless exit 0.

The shared arguments were `analyzeHeadless /tmp/squirreldra-projects-clean <project> -import <file> -overwrite -scriptPath /tmp/ghidra-scripts-clean -postScript Win16NEFixes.java -postScript ExportDecompile.java -analysisTimeoutPerFile 300 -log /tmp/squirreldra-out-clean/logs/<file>.log`.

`_ISDEL.EXE` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/_ISDEL.EXE/`.
`_SETUP.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/_SETUP.DLL/`.
`AUTORUN.EXE` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/AUTORUN.EXE/`.
`COMPOBJ.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/COMPOBJ.DLL/`.
`decrypt.exe` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/decrypt.exe/`.
`dzactx.dll` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/dzactx.dll/`.
`impulse.exe` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/impulse.exe/`.
`Inst80.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/Inst80.exe/`.
`ISGDI32.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/ISGDI32.DLL/`.
`logread.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/logread.exe/`.
`OC25.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/OC25.DLL/`.
`OLE2.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/OLE2.DLL/`.
`OLE2CONV.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/OLE2CONV.DLL/`.
`OLE2DISP.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/OLE2DISP.DLL/`.
`OLE2NLS.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/OLE2NLS.DLL/`.
`OLE2PROX.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/OLE2PROX.DLL/`.
`Oxs.dll` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/Oxs.dll/`.
`PACKAGER.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/PACKAGER.exe/`.
`PACKLIST.EXE` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/PACKLIST.EXE/`.
`Regsvr.exe` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/Regsvr.exe/`.
`remover.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/remover.exe/`.
`Repair80.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/Repair80.exe/`.
`SCP.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/SCP.DLL/`.
`SETUP.EXE` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/SETUP.EXE/`.
`STDOLE.TLB` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/STDOLE.TLB/`.
`STORAGE.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/STORAGE.DLL/`.
`TB2FTP.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB2FTP.DLL/`.
`TB80.EXE` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80.EXE/`.
`TB80ACX.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80ACX.DLL/`.
`TB80ATH.EXE` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80ATH.EXE/`.
`TB80CMP.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80CMP.DLL/`.
`TB80CVT.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80CVT.DLL/`.
`TB80EDT.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80EDT.DLL/`.
`TB80ENU1.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80ENU1.DLL/`.
`TB80ENU2.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80ENU2.DLL/`.
`TB80ENU3.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80ENU3.DLL/`.
`TB80ENU4.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80ENU4.DLL/`.
`TB80F32L.dll` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80F32L.dll/`.
`TB80FLT.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80FLT.DLL/`.
`tb80ftp.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/tb80ftp.exe/`.
`TB80LNL.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80LNL.DLL/`.
`TB80MAIN.EXE` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80MAIN.EXE/`.
`TB80MM.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80MM.DLL/`.
`TB80NET.EXE` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80NET.EXE/`.
`TB80OCX.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80OCX.DLL/`.
`TB80OLE.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80OLE.DLL/`.
`TB80RCA.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80RCA.DLL/`.
`TB80RCR.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80RCR.DLL/`.
`TB80RMT.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80RMT.DLL/`.
`TB80RTM.EXE` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80RTM.EXE/`.
`TB80RUN.EXE` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80RUN.EXE/`.
`TB80UTL.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80UTL.DLL/`.
`TB80VBX.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80VBX.DLL/`.
`TB80W16.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80W16.DLL/`.
`TB80W32.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80W32.DLL/`.
`TB80XTR.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TB80XTR.DLL/`.
`TBCBT.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBCBT.DLL/`.
`TBCOM.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBCOM.DLL/`.
`TBDB3.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBDB3.DLL/`.
`TBDLG.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBDLG.DLL/`.
`TBDOS.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBDOS.DLL/`.
`TBFILE32.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBFILE32.DLL/`.
`TBINET32.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBINET32.DLL/`.
`Tbisx32.dll` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/Tbisx32.dll/`.
`TBKSLICE.DLL` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBKSLICE.DLL/`.
`Tbload.exe` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/Tbload.exe/`.
`TBPDX.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBPDX.DLL/`.
`TBREG.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBREG.DLL/`.
`TBUTIL32.dll` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBUTIL32.dll/`.
`TBWIN.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TBWIN.DLL/`.
`Tlist16p.ocx` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/Tlist16p.ocx/`.
`TList4.ocx` (PE) finished analysis. The export is `/tmp/squirreldra-out-clean/TList4.ocx/`.
`TYPELIB.DLL` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/TYPELIB.DLL/`.
`WINSOX.EXE` (NE) finished analysis. The export is `/tmp/squirreldra-out-clean/WINSOX.EXE/`.

Left unimported: `TB80BAS.DLL`, which `RESEARCH.md` already discusses; the picture modules `DIB.DRV`, `DIBUTIL.DLL`, `PALOPTX.DLL`, `PCDLIB.DLL`, `PCDXBMP.DLL`, `PHOTO.DLL`, `PXENGWIN.DLL`, `TB80BMP.DLL`, `TB80JPG.DLL`, and `Asymgif.ocx`; help files; the spelling lexicon `VEAMAA51.LEX`; system books; and the Media folder. Books, catalogs, and the other Instructor8 files that are not EXE, DLL, DRV, or OCX images stayed out of this pass.
