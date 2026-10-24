# Runtime, Instructor, and the distribution split

Notes from Denny Dedmore's site, read 24 October 2026. This file is only that site. A behavior this reader implements belongs in `SETTLED.md`. Bytes from a book belong in `FINDINGS.md`.

Each fact names the page it came from. A later ToolBook version stays labeled with that version. ToolBook 8 is 8.0 through 8.6, then the 2004 line he also calls 8.9. Nothing below turns a 9, 10, or 11 detail into an 8 detail.

The pages do not use the name ToolBook II. The version history says there was never a 2.0 release. They do not name `TB80.EXE`, and they do not name a ToolBook 8 runtime DLL. No installer was opened, and no serial or activation key is recorded here.

## Five facts for a ToolBook 8 reader

1. Versions before ToolBook 9, which includes 8.0, 8.1, 8.5, 8.6, and 8.9, are the 16-bit line with some 32-bit mixed in. ToolBook 9 (2007) is the pure 32-bit product. ToolBook 8.9 and earlier could load 16-bit extensions; ToolBook 9 and higher cannot. Sources: the version history and the Version Updater article.
2. The authoring product edits a `.TBK`. The runtime only plays one. For ToolBook 7.x through 10.5, the runtime installer is the Neuron installer. Neuron 8.0/8.1 is the playback engine for those two releases, and the file he posts under that heading is named `neuron.exe`. Sources: the runtime-engine article and the Neuron installer list.
3. A `.TBK` extension does not say which version wrote the book. Text and graphics are inside it. Audio and video are files beside it. A bound system book is a `.SBK`, a library the book needs, and the version number is part of that filename. His examples are `TB105HYP.SBK` and `TB115HYP.SBK`. He never writes an 8.0 system-book name. Sources: the runtime-engine article and the Version Updater article.
4. From ToolBook 8 upward, the runtime files share one `TBSYSTEM` folder. In the uninstall article the usual path is `C:\Program Files\Common Files\ToolBook\TBSystem\`. Deleting the whole folder disables every engine from 8 up. He says to delete only the prefix of the version being removed, and the only prefix he gives is `TB115`. Source: the uninstall article.
5. What ships with a course is not the authoring product. Native delivery is the book, its external media, and a runtime. AutoPackager, added in ToolBook 6.0, builds that native installer when the book's deployment method is Native. The older runtime file list was `DISTRIB.WRI`. The file-list downloads he posts start at ToolBook 9.0. He does not post a ToolBook 8 file list. Sources: the version history, the AutoPackager menu article, and the runtime file-list article.

## Who is writing, and where the pages are

Denny Dedmore says he joined Asymetrix in 1996, supporting ToolBook 3.0 among other products, and stayed about 25 years, including time on the development team. He left in early 2021, about six months before SumTotal retired ToolBook. The personal site went up in January 2026. On the ToolBook index he says he wrote the knowledge base (over 95 percent of the articles) and that SumTotal removed public access in 2021. He hosts that copy himself.

- https://dennydedmore.com/
- https://dennydedmore.com/toolbook/index.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/index.html

The knowledge-base home page, last marked 10/12/2026, says license-key activation arrived with ToolBook 9.5 and applies to 9.5, 10.0, 10.5, 11.0, and 11.5. Versions older than 9.5 install without that key. His example of a release that still installs on 64-bit Windows 10 or 11 is ToolBook 9.0. He does not say that about ToolBook 8.

The same index links a 2003 OpenScript programming guide and a 2003 catalog manual. Those two PDFs are out of scope here (language reference, and the object catalog). The Actions Editor cheat sheets are out of scope for the same reason.

## ToolBook 8 on the version list

Source: https://dennydedmore.com/toolbook/knowledgebase/kb/History.html

The history is his list of English releases. The entries that bound ToolBook 8:

- 1998, ToolBook 6.0: Neuron Impulse is added, and AutoPackager replaces the Setup Manager.
- 1999, ToolBook 7.0: DHTML export is added.
- 2000, ToolBook 8.0: eLN support, HTTP Post and array support in the Actions Editor, SCORM support, and a redesigned catalog.
- 2001, ToolBook 8.1: media feedback on questions, a print command in the Actions Editor, and a backup feature.
- 2002, ToolBook 8.5: simulation support, DHTML export encryption and obfuscation, and a ZIP package of the DHTML export.
- 2003, ToolBook 8.6: Sun JVM, and cross-domain HTTP Post.
- 2004, ToolBook 2004, which he also calls 8.9, then SP1, SP2 (2005), and SP3 (2005).
- 2007, ToolBook 9.0: "Now a 32 bit product." Book Explorer and Smart Styles start here.
- 2007, ToolBook 9.01: last version of ToolBook Assistant.
- 2008, ToolBook 9.5: license-key activation, the TBKX file format, and the term Instructor dropped from the product name.
- 2011, ToolBook 11: Neuron is retired and removed from the product.
- 2012, ToolBook 11.5.

He lists ToolBook 8.0 as "ToolBook 8.0", not as "Instructor 8.0". Instructor and Assistant are edition names he uses on other pages for surrounding releases. See the runtime installer list below.

Source: https://dennydedmore.com/toolbook/knowledgebase/kb/VersionUpdater.html

The Version Updater article is written against ToolBook 11.5, and it also states the bitness rule that covers a ToolBook 8 book when someone moves it forward:

- A book cannot be downgraded. A book saved by a newer engine does not go back to an older one.
- Versions earlier than ToolBook 9 were written with 16-bit technologies and some 32-bit.
- ToolBook 9 and higher is a pure 32-bit product and cannot load 16-bit components.
- ToolBook 8.9 and earlier allowed 16-bit components (ActiveX controls or OLE objects).
- If a pre-9 book still has those 16-bit extensions, they have to be removed before the Version Updater can finish. The article's remedy is to open the book on the machine and in the version where it was made, remove the extension, and save.

That is the site's statement of why a ToolBook 8 book is a different engine from ToolBook 9.

## Authoring product versus the runtime

Source: https://dennydedmore.com/toolbook/knowledgebase/kb/RuntimeEngines.html

He separates two products:

- The Authoring Version opens a `.TBK` for editing. He also calls this the full ToolBook product.
- The Runtime version opens a `.TBK` to use or view it, for someone who does not own the authoring product.
- Each ToolBook version has its own runtime, matched to books from that version.
- Looking at a `.TBK` does not tell you which version wrote it. He says to ask the person who created the file.
- A `.TBK` holds the textual and graphical parts. Audio and video, when the project has them, are stored outside the `.TBK`. Opening a lone `.TBK` can fail later because those media files are missing.

The worked example on that page is ToolBook 11. The installer list on the same page is the part that places ToolBook 8:

| Heading on the page | Installer file he links |
|---|---|
| ToolBook 11.5 | `tbruntime115.exe` |
| ToolBook 11 | `tbruntime110.exe` |
| ToolBook 7.x through 10.5 | no separate runtime installer; use the Neuron installer |
| ToolBook Assistant and Instructor 6.5 | `tb65rt.exe` |
| ToolBook Publisher and Instructor 5.0 | `tb50rt.exe` |
| Multimedia ToolBook 4.0 CBT | `cbt40rt.exe` |
| Multimedia ToolBook 4.0 | `mtb40rt.exe` |
| Multimedia ToolBook 3.0 CBT | `cbt30rt.exe` |
| Multimedia ToolBook 3.0 | `mtb30rt.exe` |
| ToolBook 3.0 | `tb30rt.exe` |

For 7.x through 10.5 he says the Neuron installer is the older runtime installer plus browser plugins. ToolBook 8.0 and 8.1 fall in that range. There is no `tb80rt.exe` on the list.

Source: https://dennydedmore.com/toolbook/knowledgebase/kb/NeuronInstallers.html

Neuron was retired with ToolBook 11. The headings and the installer file names:

- Neuron 10.5, `neuron105.exe`
- Neuron 10.0, `neuron100.exe`
- Neuron 9.5, `neuron95.exe`
- Neuron 9, `neuron9.exe`
- Neuron 2004, which he also calls 8.9, `neuron.exe`
- Neuron 8.5/8.6, `neuron.exe`
- Neuron 8.0/8.1, `neuron.exe`
- Neuron 7.2, `neuron.exe`
- Neuron 7.0/7.1, `neuron.exe`

The 8.5/8.6, 2004, and 8.0/8.1 packages are different links that share the file name `neuron.exe`. This note does not compare their bytes.

Source: https://dennydedmore.com/toolbook/knowledgebase/kb/NeuronFAQ.html

He defines Neuron as the ToolBook runtime playback engine plus the ability to show that engine inside a browser window. The engine installed with Neuron is the same runtime engine installed with ToolBook. Neuron was pulled from the product at ToolBook 11. He says someone still on ToolBook 10.5 or earlier can still use the Neuron plugin, which is the range that includes ToolBook 8.

On install, Neuron puts the runtime components in a `TBSYSTEM` folder. The path he gives on this page is `c:\program files\common files\sumtotal\tbsystem`. Two extra files may be installed for the browser bridge: `NEURON.OCX` (Internet Explorer, under a `neuron` folder beside that SumTotal common-files tree) and `NP32NEUR.DLL` (Netscape, Firefox, and Safari, in the browser's plugins folder). Those two are the browser bridge, not the book engine.

The same article says Neuron's window is a child of the browser, so a Neuron-deployed book does not get a menu bar, and the usual full-screen techniques do not apply. Secure mode blocks a set of operations (he lists `linkDLL`, `linkDLL32`, file create/write, export, save, DDE, RUN, OLE, mail, VBX, and system books that use any of those). He says a full application is hard to run in Secure mode because hyperlinks, path animation, and catalog question objects need system books and DLL linking. He also says the engine is a Windows program and does not run on Macintosh or Unix. The article does not walk through a ToolBook 8.0 book.

Source: https://dennydedmore.com/toolbook/knowledgebase/kb/downloadtoolbook.html

The reinstall page offers three authoring installs: ToolBook 11.5, ToolBook 9.01, and ToolBook 8.1. That 8.1 entry is on the authoring download list. It is not the Neuron 8.0/8.1 runtime. The archive was not opened.

Edition names around, but not on, the 8.0 line:

- The 6.5 runtime is labeled "ToolBook Assistant and Instructor". The 5.0 runtime is labeled "ToolBook Publisher and Instructor". Source: the runtime-engine article.
- ToolBook 9.01 is the last Assistant, and the word Instructor is dropped at 9.5. Source: the version history.
- The 9.5 what's-new page still says "ToolBook Instructor 9.5" and "Instructor Startup dialog". Source: https://dennydedmore.com/toolbook/knowledgebase/kb/WhatsNew95.html
- The 11.5 path example for the authoring folder is `C:\Program Files\ToolBook\Instructor 11.5\`. Source: the special-paths article below.

So "Instructor" on this site is the authoring edition. By 11.5 the product name on the history list is ToolBook, while some 11.5 paths still say Instructor. He does not apply either sentence to the 8.0 folder layout.

Reader level inside the authoring product is not the runtime. Two later pages say so, and both are later than ToolBook 8:

- Quiz randomization does not run when you switch to Reader level. It does run if you close the book and use the Windows shell command he names, "Open In ToolBook 11.5 Runtime". In that runtime the book plays and cannot be edited. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/Randomization.html
- ToolBook 9.5 has a status-bar icon for Native versus DHTML, shown only in Author mode, and a "Hide At Reader Level" setting on the Universal Media Player. Source: the 9.5 what's-new page.

The LiveXtensions tool list, in a section whose basics page is headed ToolBook 11.5, describes a "Reader Author Reset" tool and says custom reset behavior is "Instructor only". Source: https://dennydedmore.com/toolbook/knowledgebase/kb/LivexTools.html and https://dennydedmore.com/toolbook/knowledgebase/kb/LiveXtensions.html

## `.TBK` versus `.SBK`

`.TBK` is the book file, for both the authoring product and the runtime. Sources: the runtime-engine article, and https://dennydedmore.com/toolbook/knowledgebase/kb/OpenBackup.html

The backup article does not name a version. The history says the backup feature was added in ToolBook 8.1. The backup article says a normal save keeps the `.TBK` extension, and a backup is the same book saved with another extension: `.BAK`, `.001` through `.009`, or `.1` through `.9`. Windows will not route those extensions to ToolBook. He says to rename the backup to `.TBK`, or open it from the Startup dialog, from File | Open, or by dropping it on an open ToolBook window.

`.SBK` is a system book. On the Version Updater page he calls bound system books library files ToolBook needs in order to function, and he says the version is in the name:

- ToolBook 11.5 hyperlink system book: `TB115HYP.SBK`
- The same book for ToolBook 10.5: `TB105HYP.SBK`

The updater replaces older names on the book's bound-system-book list with the 11.5 names. He does not list the ToolBook 8 names that would be replaced.

Other system-book names, all later than ToolBook 8:

- `TB115R.SBK`, the runtime system book, has to be on the book's Bound System Books list (File menu) or the 11.5 helpers `getConfigVar`, `setConfigVar`, and `ASYM_StandardFolderPath` return nothing useful in the runtime. Sources: https://dennydedmore.com/toolbook/knowledgebase/kb/INIProfile.html and https://dennydedmore.com/toolbook/knowledgebase/kb/SpecialPaths.html
- `TBxxR.SBK` is the placeholder he prints for the runtime system book that holds `ASYM_GetSystemColor`. He says that function was added in ToolBook 2004 SP3. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/SystemColors.html
- `TB115XML.SBK` is the 11.5 book that reads XML. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/xmlsbk.html
- `TB115AXF.SBK` is named in the 11.5 patch note for a web-publishing error. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/NotAnObjectTarget.html
- `TBxxstyles.sbk` appears in a Smart Styles error. Smart Styles begin at ToolBook 9.0 on the history list. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/CreateObjectError.html

A system book does not have to use the `.SBK` extension. The LiveXtensions "create your own" article says a tool is an ordinary `.TBK`, and pushing it onto the `sysBooks` stack is what puts it in the message hierarchy. The `.SBK` extension is not required for that. The basics page for that feature is headed ToolBook 11.5. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/CreatingLivex.html

The LiveXtensions tool list includes a tool that prints the file names on the `sysBooks` stack, the book's extensions, and the bound system books. Same 11.5 section.

Neuron, on the FAQ page, can load clips, system books, DLLs, and other ToolBook files from the web server directory that holds the running `.TBK`, after it looks for them locally. A `.TBK` on a web server is opened through the Neuron plugin when the browser is set up for the `application/toolbook` type (he also describes the `.tbk` registry class `tbkfile`). If ToolBook the authoring product is the handler instead, the browser opens the file in ToolBook rather than in Neuron. The deploy walkthrough he gives for TotalLMS is a ToolBook 10.5 lesson. Source: the Neuron FAQ, and https://dennydedmore.com/toolbook/knowledgebase/kb/NeuronTotalLMS.html

## Where the two installs sit

Authoring files and runtime files are different directories on the pages that give paths.

ToolBook 11.5 examples, special-paths article:

- Authoring components: the product folder, typically `C:\Program Files\ToolBook\Instructor 11.5\`, read with `ASYM_ProductDirectory()`.
- Runtime components: the system folder, typically `C:\Program Files\Common Files\ToolBook\TBSystem\`, read with `sysToolBookDirectory`.
- The open book: `ASYM_PathOfFile` on the book name.

Those two function names are documented there as living in `TB115R.SBK`. He does not say ToolBook 8 has them.

Uninstall article, which does name ToolBook 8: https://dennydedmore.com/toolbook/knowledgebase/kb/Uninstall.html

The article's product-folder example is `C:\Program Files\ToolBook\ToolBook 11.5\`. The uninstaller leaves that folder behind because it can hold catalog additions and personal settings. The runtime folder in the same article is `C:\Program Files\Common Files\ToolBook\TBSystem\`. He says this `TBSYSTEM` folder holds the runtime engine files for every version from ToolBook 8 upward. Deleting it disables ToolBook 8 and every later version until they are reinstalled. For a clean 11.5 reinstall he says to delete the files in that folder whose names start with `TB115`, and to leave the rest.

The Neuron FAQ path uses `sumtotal\tbsystem` instead of `ToolBook\TBSystem`. Both are "typical" paths on their own pages. This note does not pick one as the ToolBook 8 layout.

## What a distribution contains

Two delivery methods, on pages that do not name ToolBook 8:

- Native: a ToolBook `.TBK` delivered on a LAN or a CD-ROM. The File menu shows AutoPackager.
- DHTML: a web export. The File menu shows Publish to Web.

New books start as DHTML. The switch is Object menu, Properties for Book, Deployment tab, then Native ToolBook or DHTML Deployment. Sources: https://dennydedmore.com/toolbook/knowledgebase/kb/MissingAPMenu.html and https://dennydedmore.com/toolbook/knowledgebase/kb/MissingPubMenu.html

AutoPackager is the native packager from ToolBook 6.0 on the history list. The 9.01 history line still mentions AutoPackager fixes. The packager articles themselves do not say "ToolBook 8". They also do not list the files AutoPackager writes. One article says the packager will not offer the Extensions and Shortcuts step until its log is clean. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/ShortcutPackager.html

Runtime files for someone who will not use AutoPackager: https://dennydedmore.com/toolbook/knowledgebase/kb/RuntimeFilesList.html

He says older ToolBook versions kept that file list in `DISTRIB.WRI`. The downloads on the page are zip bundles for ToolBook 11.5, 11.0, 10.5, 10.0, 9.5, and 9.0. There is no ToolBook 8 bundle. The article text does not name the files inside the zips, and the zips were not opened. The license page points at this article (he numbers it P3028) for which files are redistributable.

The license text is the SumTotal agreement, with activation language, so it belongs to the 9.5-and-later licensing world, not to a ToolBook 8 license. In summary, without copying it: runtime files may be copied along with an application built in ToolBook, and he distinguishes runtime files that may travel separately from additional runtime files that travel only with the application. The same section says the license does not let you ship an application that creates new ToolBook applications, creates a DHTML application, creates scripts, or defines hyperlinks. That is the authoring side staying with the authoring product. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/LicenseAgreement.html

DHTML distribution is a different package. The history says ToolBook 8.5 added a ZIP package of the DHTML export. The how-to that names files does not give a version. It says the lesson opens from `index.html`, that an optional package file is a ZIP, and that CD autoplay, if that option was enabled, adds `autorun.exe`, `autrun.ico`, and `autorun.inf` at the root of the disc next to the export folder. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/AfterPublish.html

A DHTML version stamp is not the native engine version. The Mercury page reads a `MERCURY=` value from the exported `index.html`. The table starts at Instructor 2004. He labels `8.1.0.2689696` as Instructor 2004 and `8.9.0.2823820` as Instructor 2004 SP1 (and, the same digits, Assistant 2004 for 4.x browsers). On the history list, ToolBook 8.1 is the 2001 product and ToolBook 2004 is 8.9. The Mercury numbers are publisher stamps for DHTML, not the 2001 runtime. He does not list a ToolBook 8.0 stamp. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/Mercury.html

System requirements for "ToolBook Author and Runtime Environment" on https://dennydedmore.com/toolbook/knowledgebase/kb/SystemRequirements.html are stated for ToolBook 11.5, 11, and 10.5 (Neuron 10.5 included). ToolBook is a Windows program there, not Mac or Unix, and the install wants administrative rights. He does not give a ToolBook 8 requirements line on that page.

## Names only

Named on a page that covers ToolBook 8:

- `neuron.exe`, the Neuron 8.0/8.1 installer, and the same file name under the 8.5/8.6 and 2004 headings.
- `TBSYSTEM`, the shared runtime folder from ToolBook 8 upward.
- `DISTRIB.WRI`, the runtime file list from versions before the 9.0 zip bundles.

Named for other versions, so they are not ToolBook 8 engines:

- `tb65rt.exe`, `tb50rt.exe`, `cbt40rt.exe`, `mtb40rt.exe`, `cbt30rt.exe`, `mtb30rt.exe`, `tb30rt.exe`
- `tbruntime115.exe`
- Version 11 runtime installer, three spellings on three pages: `RUNTIME110.EXE` (what's-new for 11, formerly `NEURON110.EXE`), `TBRUNTIME110.EXE` (11.0 release notes), `tbruntime110.exe` (the runtime download page). Sources: https://dennydedmore.com/toolbook/knowledgebase/kb/WhatsNew11.html and https://dennydedmore.com/toolbook/knowledgebase/kb/RelNotes11.html
- `neuron105.exe`, `neuron100.exe`, `neuron95.exe`, `neuron9.exe`
- `NEURON.OCX`, `NP32NEUR.DLL`
- `TB115R.SBK`, `TB115HYP.SBK`, `TB105HYP.SBK`, `TB115XML.SBK`, `TB115AXF.SBK`, and the placeholders `TBxxR.SBK` and `TBxxstyles.sbk`
- `BAS.DLL`, named once, as a module that can GPF when a book is corrupt during use or authoring. No version and no path. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/RepairKit2.html
- `TbkSlice.dll`, a web-publisher DLL in a DHTML error, not the native runtime.

User-written DLLs, not the product runtime: he says older DLLs for ToolBook were 16-bit and declared exports `FAR PASCAL`, and that 32-bit Visual C++ compilers replaced that with `_stdcall`. Source: https://dennydedmore.com/toolbook/knowledgebase/kb/32bitdlls.html

## Pages used

- https://dennydedmore.com/
- https://dennydedmore.com/toolbook/index.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/index.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/History.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/VersionUpdater.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/RuntimeEngines.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/NeuronInstallers.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/NeuronFAQ.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/downloadtoolbook.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/Uninstall.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/RuntimeFilesList.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/OpenBackup.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/SpecialPaths.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/INIProfile.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/CreatingLivex.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/LivexTools.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/LiveXtensions.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/Randomization.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/MissingAPMenu.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/MissingPubMenu.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/ShortcutPackager.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/LicenseAgreement.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/AfterPublish.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/Mercury.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/WhatsNew95.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/WhatsNew11.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/RelNotes11.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/SystemRequirements.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/SystemColors.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/xmlsbk.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/NotAnObjectTarget.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/CreateObjectError.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/RepairKit2.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/32bitdlls.html
- https://dennydedmore.com/toolbook/knowledgebase/kb/NeuronTotalLMS.html

The knowledge-base table of contents and its search index were used to find those articles. The full set of HTML articles was scanned for `TB80`, `TB80.EXE`, and ToolBook II. Those strings are not in the articles.
