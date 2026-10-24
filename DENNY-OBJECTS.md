# Denny Dedmore: OpenScript and draw objects

Notes from https://dennydedmore.com for the OpenScript language and for draw objects, especially the pie. This file records what those pages say. It does not assign class numbers or byte offsets. Another part of this project measures those from files.

OpenScript is the ToolBook language. The `script` property of an object holds OpenScript written for that object, and the book is one of those objects. A system book is a separate book, such as `TB89R.SBK`, bound above the current book. This note does not rename either of those "open script." The runtime-versus-distribution file list is not in this note.

## Pages used

- https://dennydedmore.com — personal site. He started at Asymetrix in 1996 supporting ToolBook 3.0, later worked on the development team, and says OpenScript is the built-in language.
- https://dennydedmore.com/toolbook/index.html — same ToolBook introduction, plus links to the Knowledge Base, the OpenScript reference, the catalog book, and the two Actions Editor cheat sheets. https://toolbook.dennydedmore.com/ is the same ToolBook introduction.
- https://dennydedmore.com/toolbook/books/ToolBookCatalog.pdf — *ToolBook Catalog Objects - Fully Explained*. Written for ToolBook Assistant and ToolBook Instructor 8.5. He says much of it also applies to ToolBook 8.0 and 8.1, and that the book is written with 8.5 in mind. PDF dated 2003, modified 2005.
- https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf — *OpenScript & Actions Editor Programming Reference Guide*, third edition, August 2005, for ToolBook Instructor 2004. He says much of it is valid for any version of ToolBook. https://dennydedmore.com/toolbook/knowledgebase/kb/History.html calls ToolBook 2004 "aka 8.9", which is after ToolBook 8.0, 8.1, 8.5, and 8.6. Facts below from this PDF are 2004 / 8.9 facts unless he marks an earlier version. They are not treated as ToolBook 8 rules merely because the guide says much of it is older.
- https://dennydedmore.com/toolbook/knowledgebase/kb/toc.html — Knowledge Base contents, used to find the articles below.
- https://dennydedmore.com/toolbook/knowledgebase/kb/History.html — shipped-version list.
- https://dennydedmore.com/toolbook/knowledgebase/kb/TransparentDraw.html — draw-object transparency. The page does not name a ToolBook version.
- https://dennydedmore.com/toolbook/knowledgebase/kb/CompressingAE.html — Actions Editor compression of generated OpenScript. The page does not name a ToolBook version.
- https://dennydedmore.com/toolbook/knowledgebase/kb/DHTMLPasswords.html — native book password versus a published lesson. The page does not name a ToolBook version.
- https://dennydedmore.com/toolbook/knowledgebase/kb/PasswordField.html — DHTML password-field glyph. The page does not name a ToolBook version.
- https://dennydedmore.com/toolbook/knowledgebase/kb/OSUpdatePost9.html — OpenScript and ToolBook 9.0.
- https://dennydedmore.com/toolbook/knowledgebase/kb/RelNotes11.html — ToolBook 11.0 release notes, 1 October 2011.
- https://dennydedmore.com/toolbook/cheatsheets/ActionsEditorCheatSheet.pdf and https://dennydedmore.com/toolbook/cheatsheets/ActionsEditorProgrammingCheatSheet.pdf — both titled ToolBook 11.5, March 2013. Their Actions Editor property lists are later than ToolBook 8 and are not used below as ToolBook 8 rules. The 11.5 programming sheet does list `rgbstroke` under draw objects; the 2004 draw-object Actions Editor list does not.
- https://dennydedmore.com/toolbook/knowledgebase/kb/LRC.html and https://dennydedmore.com/toolbook/knowledgebase/kb/MINILESSONS.html — opened from the Knowledge Base index. They point at in-product help, videos, and training, and they do not add pie, draw-object, or OpenScript property facts.

The word polyline does not appear on the catalog PDF, the OpenScript PDF, or the Knowledge Base table of contents. The multi-point line types he names are `line`, `angledLine`, `curve`, and `irregularPolygon`.

## Which ToolBook 8 the catalog is talking about

From https://dennydedmore.com/toolbook/knowledgebase/kb/History.html:

- 2000, ToolBook 8.0. The catalog was redesigned. Actions Editor array support and HTTP Post were added.
- 2001, ToolBook 8.1. Question media feedback, an Actions Editor print command, and a backup feature.
- 2002, ToolBook 8.5. Simulation support. DHTML export gained encryption, obfuscation, and a zip package.
- 2003, ToolBook 8.6. Then 2004, ToolBook 2004 (aka 8.9).

From the same page, later than this project's ToolBook 8, and not used here as ToolBook 8 behavior:

- ToolBook 9.0 (2007) is 32-bit. `RGBStroke` and `Transparent` were added to the Actions Editor. https://dennydedmore.com/toolbook/knowledgebase/kb/OSUpdatePost9.html says OpenScript works in native ToolBook and does not run in a web-published lesson, and that ToolBook 9.0 and higher cannot use 16-bit logic.
- ToolBook 11 (2011) enhanced draw objects: smoother lines, and transparency and color blending "on par with industry standards." https://dennydedmore.com/toolbook/knowledgebase/kb/RelNotes11.html says the same for version 11.0. That is not a ToolBook 8 rule.

The 2004 OpenScript guide's `bookVersion()` return list is `1.0`, `1.5`, `3.0`, `3.0MM`, `4.0`, `5.0`, `6.0`, `7.0`, `7.2`, `8.0`, or `8.5`. The function identifies a `.tbk` without opening it. The printed list stops at 8.5 even though the guide itself is for Instructor 2004. https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf

## What he says a pie is, and how it is drawn

### Catalog, ToolBook 8.5, with his note that much also applies to 8.0 and 8.1

https://dennydedmore.com/toolbook/books/ToolBookCatalog.pdf

Draw objects are ToolBook's own shapes, such as a rectangle or a line. Once on the page they can be moved, resized, reshaped, and recolored. Assistant users get them from the Draw Objects catalog. Instructor users draw them with the Tool Palette.

A pie is an ellipse, and the author chooses how much of that ellipse is visible. The catalog places a pie as a quarter of an ellipse. Reshape Pie, on the Draw menu, moves the pie's end points. Dragging the handles stretches and reshapes it. The Properties dialog applies colors and line styles. Holding Ctrl while dragging a corner handle resizes it in proportion. Instructor users also add a pie from the Tool Palette.

An arc, on the facing catalog page, is the perimeter counterpart: an ellipse where you choose how much of the perimeter is visible, also dropped as a quarter, adjusted with Reshape Arc. A pie is how much of the ellipse; an arc is how much of the outline.

A pie has no built-in behavior. An OpenScript handler such as `buttonClick` or `mouseEnter` runs in ToolBook or Neuron and does not run in DHTML. The Actions Editor events On Click and On Mouse Over run in ToolBook and in DHTML. A ToolTip needs no script. On DHTML export, draw objects usually become GIF images. Internet Explorer can draw them directly if the checkbox on the Web tab of that object's property sheet is checked. Netscape still uses the GIF.

He does not give a center, a radius, a start angle, or a sweep in numbers. He does not say which of the reshape handles is which end point.

### OpenScript draw command

https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf — Instructor 2004 (aka 8.9). He says much of the guide is valid for any version. He does not mark `draw pie` as new in 2004.

`draw pie from <location> to <location> to <location>`

A curve, an arc, or a pie needs three points. A point is two page-unit numbers: distance from the left edge of the page, then distance from the top. The guide's example is `draw pie from 1000,100 to 650,874 to 0,0`. Drawing sets `selection` to the new object's `uniqueName`. The same command's object types are `angledLine`, `arc`, `button`, `comboBox`, `curve`, `ellipse`, `field`, `irregularPolygon`, `line`, `ole`, `pie`, `polygon`, `rectangle`, `recordField`, `roundedRectangle`, and `stage`, plus an extension type if the book has one.

The `pie` object-type entry repeats that signature and says a pie's parent is a page, a background, or a group. The next sentence in that entry talks about a rounded rectangle, not a pie: it says a rounded rectangle's `bounds` and `vertices` are not equal. The `roundedRectangle` entry, and the `bounds` entry, both say the opposite for a rounded rectangle: `bounds` and `vertices` have the same value. That sentence is not a description of a pie.

`sysTool` at Author level can be `pie`, among the other tool names. At Reader level it is `Reader`. Setting it changes the tool palette.

`object` of a pie is the string `Pie`. The same property's strings include `AngledLine`, `Arc`, `Curve`, `Ellipse`, `IrregularPolygon`, `Line`, `Polygon`, `Rectangle`, and `roundedRectangle`.

`vertices` of a pie is in the group he describes as a comma-separated list of points that define the shape. That same sentence covers lines, angled lines, polygons, irregular polygons, arcs, pies, and curves. Each point is two numbers. He does not say how many points a pie stores, and he does not say that a pie uses the arc's four-value begin-and-end form. For other objects, `vertices` is four numbers and matches `bounds`. Viewer vertices are in pixels. Every other object's vertices are in page units. He notes that changing `vertices` of an irregular polygon reshapes it. He does not say that about a pie.

`bounds` of a draw object is four page-unit numbers: upper-left x,y, then lower-right x,y. He lists the types whose `bounds` and `vertices` are equal, including ellipses, rectangles, and rounded rectangles. Pie is not in that list. He also does not give a separate pie rule. He does not say whether the three points passed to `draw pie` are what `vertices` returns.

## Other draw objects

Catalog behavior is from https://dennydedmore.com/toolbook/books/ToolBookCatalog.pdf (8.5, and he says much applies to 8.0 and 8.1). OpenScript signatures and geometry are from https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf (Instructor 2004 / 8.9, "much of the information is valid for any version").

Shared catalog behavior for every draw object on these pages: no predefined behavior; OpenScript `buttonClick` and `mouseEnter` work in ToolBook and Neuron and not in DHTML; Actions Editor On Click and On Mouse Over work in both; DHTML usually exports a GIF, with the Internet Explorer exception above.

- `ellipse`. `draw ellipse from <location> to <location>`. Parent is page, background, or group. `vertices` and `bounds` are the same. The catalog Circle is an ellipse whose height and width match. The catalog Ellipse starts slightly oval. Handles stretch and reshape it. Ctrl plus a corner handle keeps the proportion. Colors and line styles come from the Properties dialog.
- `rectangle`. `draw rectangle from <location> to <location>`. Parent is page, background, or group. `bounds` and `vertices` are the same. The catalog rectangle is its own type. It must have four sides. You cannot add or remove segments. The catalog Square is not this type; it is a four-sided `polygon`.
- `roundedRectangle`. `draw roundedRectangle from <location> to <location>`. Parent is page, background, or group. `bounds` and `vertices` are the same. The catalog object starts slightly non-square. Ctrl plus a corner handle keeps the proportion.
- `polygon`. `draw polygon from <location> to <location>`. Parent is page, background, or group. `bounds` and `vertices` are not the same values. `sysPolygonShape` is the side count used when a polygon is drawn: an integer from 3 to 99, default 4. The catalog Triangle, Square, Pentagon, Hexagon, and Octagon are polygons of 3, 4, 5, 6, and 8 sides, and the polygon palette has to be set to that count before drawing. Reshape Polygon drags a node. Shift-click an existing node to add one. Ctrl+Shift-click removes one. In OpenScript, select it and `send reshape`, then use those same key gestures. After that it is still a `polygon`, even if it looks irregular.
- `irregularPolygon`. `draw irregularPolygon from <location> to <location> to <location>...`. Three or more points, at most 511. Two points make a straight line. Parent is page, background, or group. `bounds` are the selection handles. Each vertex is two numbers, from the first angle drawn to the last. ToolBook closes it if the first and last vertices differ. Reshape, add, and remove work as for a polygon (`send reshape`, Shift-click to add, Ctrl+Shift-click to remove). The catalog Freeform Polygon is this drawing process: a pencil, click each vertex, double-click to finish. Instructor's tool shows a cross-hair instead of the pencil.
- `line`. `draw line from <location> to <location>`. Parent is page, background, or group. Without line ends, `bounds` is two pairs of numbers, the end points. For a vertical line, a horizontal line, or a line that slopes down from left to right, those `bounds` match `vertices`. With line ends, `bounds` is the smallest rectangle around the line and the ends, and it changes with `lineEndStyle` and `lineEndSize`. The catalog line is stretched by its handles. Colors and line styles come from the Properties dialog.
- `angledLine`. `draw angledLine from <location> to <location> to <location>...`. Three or more points, at most 511. Two points make a straight line. Parent is page, background, or group. `bounds` and `vertices` differ. `bounds` are the selection handles. Each vertex is two numbers from the first angle to the last. An angled line cannot be filled with a color or a pattern. The catalog Angled Line sample is a three-segment line. The tool palette can draw as many segments as you want; double-click places the last node. Reshape Angled Line, Shift-click to add a node, Ctrl+Shift-click to remove one. The catalog Freeform Angled Line is that same drawing process, with a pencil cursor.
- `curve`. `draw curve from <location> to <location> to <location>`. Parent is page, background, or group. `bounds` and `vertices` differ. `bounds` are the selection handles. Each set of six vertex numbers is the x,y of the beginning, the middle, and the end. The catalog Simple Curve is one curve and the Complex Curve is two; both are curve objects. Instructor can add as many curves as wanted from the tool palette.
- `arc`. `draw arc from <location> to <location> to <location>`. Parent is page, background, or group. `bounds` and `vertices` differ. `bounds` are the selection handles. The four vertex numbers are the x,y of the beginning and the end. The arc sweeps between the imaginary radii from the center of the arc to those vertices. The catalog arc is a quarter of an ellipse's perimeter until Reshape Arc moves the end points.

`lineEndSize` and `lineEndStyle` are properties of a line, an angled line, an arc, or a curve. He does not list pie, polygon, ellipse, or rectangle for those two properties. `lineEndSize` is two integers from 1 to 9, start then end, default `sysLineEndSize`. `lineEndStyle` is two of `filledHead`, `filledTail`, `openHead`, `openTail`, `solidHead`, `solidTail`, or `none`, default `sysLineEndStyle`. The line-ends palette sets them and cannot be shown in Runtime ToolBook. History says line ends were added in ToolBook 3.0 (1994), so they are older than ToolBook 8. https://dennydedmore.com/toolbook/knowledgebase/kb/History.html

`lineStyle` is the line style of draw objects, and also the border of picture and paint objects. Values: `Dashed`, `dotted`, `none` (0), or `1`, `2`, `3`, `4`, `6`, or `8`. The numbers are thickness. The default is `sysLineStyle` at creation.

Convert Object, on the Edit menu, turns one draw-object style into another. That note is in the 2004 guide's draw-object chart.

## Handlers

https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf

A handler is `to handle <message name> [<parameters>]`, then statements, then `end`. The message name starts with a letter. Besides letters and digits, the only punctuation he allows in the name is underscore. User-defined messages use the same structure.

`forward` sends the current message, or a named message, to the next object up the hierarchy. `forward to system` sends it to the ToolBook system. `forward to parent` starts at the parent. The calling handler continues after the called handlers finish. He says a system book will not see the message unless a lower handler forwards it. In a shared script, a plain `forward` loops, because the order is object script, object shared script, parent script, parent shared script. Use `forward to parent` there. A message forwarded from a viewer goes to the book that owns the viewer.

`buttonClick <location>,<isShift>,<isCtrl>` goes to the object under the cursor when the left button is pressed and released. If the cursor leaves that object's `bounds` before the release, `buttonClick` is not sent. A click arrives as `buttonDown`, then `buttonUp`, then `buttonClick`. He says to forward system-generated messages unless there is a reason not to. `break to system` is how a `destroy` handler refuses the deletion.

Parents, from the `parent` property: a grouped object's parent is the group; an ungrouped object's parent is its page or background; a page's parent is a background; a background's parent is the book; a viewer's parent object is the book. Books have no parent. System books sit above books. There is no built-in message sent directly to the book. `enterBook` and `leaveBook` are sent to the current page. Messages can still travel up to the book, and scripts can send messages to it. The book's script is that book's `script` property.

`script` holds the OpenScript written for any object, including at runtime. Null means there is no script. Setting it requires a script that compiles.

## OpenScript property names

The names in this section are the 2004 / 8.9 guide's names, from https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf, except where a bullet cites the 8.5 catalog. History's "added to the Actions Editor in 9.0" note is called out where it matters. The guide's own draw-object Actions Editor list is shorter than the ToolBook 11.5 cheat sheet and is the list recorded here.

### Draw objects, including pie

OpenScript messages on the draw-object chart: `make`, `destroy`, `moved`, `sized`, `buttonClick`, `buttonDown`, `buttonUp`, `buttonDoubleClick`, `buttonStillDown`, `rightButtonDown`, `rightButtonUp`, `rightButtonDoubleClick`, `mouseEnter`, `mouseLeave`.

OpenScript properties on that chart: `bounds`, `defaultAllowDrag`, `defaultAllowDrop`, `dragImage`, `drawDirect`, `fillColor`, `idNumber`, `layer`, `lineEndSize`, `lineEndStyle`, `lineStyle`, `name`, `noDropImage`, `notifyAfterMessages`, `notifyBeforeMessages`, `object`, `parent`, `pattern`, `position`, `rgbFill`, `rgbStroke`, `script`, `sharedScript`, `size`, `strokeColor`, `transparent`, `uniqueName`, `userProperties`, `useWindowsColors`, `vertices`, `visible`.

Actions Editor events on that chart: click, double-click, load page, mouse off, mouse over, property change, reset, right-click, trigger, unload page, user event.

Actions Editor properties on that chart: `height`, `left`, `name`, `top`, `visible`, `width`. `rgbstroke` is on the ToolBook 11.5 cheat sheet's draw-object column, not on this 2004 chart. History says `RGBStroke` and `Transparent` were added to the Actions Editor in ToolBook 9.0, which is after ToolBook 8.

Property behavior he spells out for draw objects:

- `fillColor` is the HLS fill of a background, draw object, record field, field, stage, button, combo box, or graphic. Three numbers, hue 0–360, lightness 0–100, saturation 0–100, or a color constant. Default is `sysFillColor` at creation. It stays in step with `rgbFill`.
- `rgbFill` is the same fill in RGB, each component 0–255, or a color constant. Default is `sysRGBFill` at creation. The Actions Editor supports `rgbFill`.
- `strokeColor` is the HLS stroke of a background, draw object, record field, field, button, combo box, or graphic. Same HLS ranges. Default is `sysStrokeColor` at creation. It stays in step with `rgbStroke`.
- `rgbStroke` is the RGB form of that stroke, 0–255 or a color constant, default `sysRGBStroke`. The description line says "fill color"; the notes say it is interchangeable with `strokeColor`. The notes are the pairing he actually describes.
- `pattern` is the fill of a draw object or a background: `none`, `solidFill`, `solidStroke`, or a whole number from 1 to 128. Default is `sysPattern` at creation. For a solid color, set `solidStroke` or `solidFill` rather than `none`. `none` makes the object look white and transparent.
- `transparent` is true or false on a draw object, record field, field, button, combo box, group, or paint object. Default is `sysTransparent`. A transparent object still receives keyboard and mouse messages. Picture objects do not have this property. The Actions Editor support he notes for `transparent` matches History's ToolBook 9.0 Actions Editor addition, not the 2004 draw-object Actions Editor column.
- `drawDirect` is on every object type except hotwords, pages, backgrounds, viewers, and books. True draws on screen in layer order. False composes off screen first. An on-screen object paints above the off-screen image. Default is `sysDrawDirect` at creation. Moving animation wants false, or it flickers. Show, hide, and layer-swap animation wants true.
- `position` is the upper-left corner. For a draw object it is two page-unit numbers relative to the client area of the ToolBook window.
- `dragImage` is the cursor shown while dragging over an object that accepts a drop. `noDropImage` is the cursor when the target does not accept a drop. Either is an icon, bitmap, cursor, or null.
- `idNumber` is read-only, a whole number from 0 to 65535, unique per page, per background, and per resource type. It changes if the object is imported or pasted. He recommends names instead.

https://dennydedmore.com/toolbook/knowledgebase/kb/TransparentDraw.html, version not stated: a draw object whose `fillColor` is white and whose transparent setting is on still looks milky. Set `pattern` to `none` so the fill is not drawn. He defines draw objects there as circles, lines, rectangles, and polygons from the tool palette or the Draw Objects catalog. Do not read ToolBook 11's "true transparency" into this article. That change is version 11.

### Button

OpenScript messages added beyond the draw-object set: `enterButton`, `leaveButton`, `keyChar`, `keyDown`, `keyUp`.

OpenScript properties on the button chart: `borderStyle`, `bounds`, `caption`, `captionPosition`, `checked`, `checkedGraphic`, `defaultAllowDrag`, `defaultAllowDrop`, `disabledGraphic`, `dragImage`, `drawDirect`, `enabled`, `excludeTab`, `fillColor`, `fontFace`, `fontSize`, `fontStyle`, `highlight`, `idNumber`, `invert`, `invertGraphic`, `layer`, `name`, `noDropImage`, `normalGraphic`, `notifyAfterMessages`, `notifyBeforeMessages`, `object`, `parent`, `position`, `rgbFill`, `rgbStroke`, `script`, `sharedScript`, `size`, `stretchGraphic`, `strokeColor`, `textOverflow`, `textUnderflow`, `transparent`, `uniqueName`, `userProperties`, `useWindowsColors`, `vertices`, `visible`.

Actions Editor properties on that chart: `caption`, `checked`, `enabled`, `height`, `name`, `rgbFill`, `selectedItemText`, `itemSelected`, `itemText`, `left`, `top`, `transparent`, `visible`, `width`. The chart includes `transparent` here. History still dates the Actions Editor's `Transparent` addition to ToolBook 9.0, so this chart is not evidence that ToolBook 8's Actions Editor had it.

`draw button from <location> to <location>`. Parent is page, background, or group. Every button style is this one type. `borderStyle` is `checkBox`, `checkBox3D`, `commandButton`, `label`, `none`, `pushButton`, `radioButton`, `radioButton3D`, `rectangle`, `rounded`, or `shadowed`. The default is `pushButton`. Check boxes and radio buttons are drawn as buttons and then given that `borderStyle`. A caption mnemonic is an `&` before the character. `normalGraphic` attaches an image. `enabled` false drops keyboard and mouse messages and removes the button from the tab order. `checked` toggles when the user clicks a radio button or check box. `autoRadioButtons` on a group, true by default, makes grouped radio buttons exclusive. `invert` true looks pushed. `excludeTab` true keeps the focus outline off. `stretchGraphic` true stretches bitmap graphics to the button face.

The 8.5 catalog repeats the same OpenScript-versus-Actions-Editor split for pushbutton, command, shadow, rounded, rectangle, checkbox, radio button, and label buttons. A button can show a graphic, a caption, or both, and can carry a script, an action sequence, or a hyperlink. https://dennydedmore.com/toolbook/books/ToolBookCatalog.pdf

### Field

`draw field from <location> to <location>`, from the `draw` command. The field entry itself does not repeat a signature. A field holds editable, formattable text and can be a list box. It can contain hotwords, and it is their parent. Its parent is a page, a background, or a group. A record field exists only on a background; referring to the record field uses the background, and referring to its text uses the page.

OpenScript messages on the field chart include `make`, `activated`, `destroy`, `enterField`, `leaveField`, `moved`, `sized`, `textScrolled`, the mouse messages, and `keyChar`, `keyDown`, `keyUp`.

OpenScript properties on that chart: `activated`, `baselines`, `borderStyle`, `bounds`, `defaultAllowDrag`, `defaultAllowDrop`, `dragImage`, `drawDirect`, `drawTextDirect`, `enabled`, `fieldType`, `fillColor`, `fontFace`, `fontSize`, `fontStyle`, `idNumber`, `indents`, `layer`, `name`, `noDropImage`, `notifyAfterMessages`, `notifyBeforeMessages`, `object`, `objects`, `parent`, `position`, `rgbFill`, `rgbStroke`, `richText`, `script`, `scroll`, `selectedTextlines`, `sharedScript`, `singleLine`, `size`, `spacing`, `strokeColor`, `tabSpacing`, `tabType`, `text`, `textAlignment`, `textOverflow`, `textRightOverflow`, `textUnderflow`, `transparent`, `uniqueName`, `userProperties`, `useWindowsColors`, `vertices`, `visible`.

Actions Editor properties on that chart: `height`, `left`, `name`, `rgbFill`, `scroll`, `text`, `top`, `visible`, `width`.

`borderStyle` for a field or record field: `inset`, `none`, `raised`, `rectangle`, `scrolling`, or `shadowed`. Default `rectangle`. `fieldType`: `noWrap`, `singleLineWrap`, `wordWrap`, `multiSelect`, or `singleSelect`. Default `wordWrap`. `text` is the raw characters. `richText` is the RTF. Setting `richText` equal to `text` strips character formatting. A field holds one paragraph setting, so two paragraphs cannot have different alignment. The chart note says a field holds 32,000 characters. `drawTextDirect` true draws the text on screen even when the field is composed off screen, and speeds scrolling. `activated` true means the field is not typed into and instead receives mouse messages. `enabled` false drops keyboard and mouse messages.

Catalog password field, ToolBook 8.5, Instructor catalog only: https://dennydedmore.com/toolbook/books/ToolBookCatalog.pdf. It shows a masking character instead of the typed text. In native ToolBook the mask is an asterisk unless `_passwordChar` is set. He calls `_passwordChar` undocumented and says to set it from the Command Window. The printed statement is a figure; the text layer does not include the command. He says the figure uses a pound character. In native ToolBook, `ASYM_Text` is the real string and `text` is the masked string. In the Actions Editor, and in DHTML, `text` is the real string. The DHTML mask character depends on the operating system and the browser.

https://dennydedmore.com/toolbook/knowledgebase/kb/PasswordField.html, version not stated: at Reader level the field shows asterisks, but DHTML can show a vertical bar when the font has no bullet. He names SYSTEM as such a font, and Arial, Times New Roman, and Courier as fonts that have a bullet. That is a published-lesson glyph, not the book password.

## Compression

Two different mechanisms. Neither one is the runtime file list.

https://dennydedmore.com/toolbook/knowledgebase/kb/CompressingAE.html, version not stated. The Actions Editor writes OpenScript into the object's script, including error checks and comment lines. One comment he quotes as an example warns that the handler was created by the Actions system. An object's OpenScript is limited to 64K, which he states as 65,535 characters. Shared Actions are stored as OpenScript in the script of the book. A simulation's Actions Editor logic is stored on a button named Simulation. The Devex LiveXtension named Actions Editor Compression tells ToolBook to stop writing those comment lines for new Actions Editor code in that book. Existing code is compressed by enabling the tool, opening the event, and choosing Update Actions & Close, once per event. He does not say this tool existed in ToolBook 8.0. History puts the Actions Editor in 7.1 and Simulation support in 8.5.

https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf, the book chart in the Instructor 2004 guide. Save As to a different file name compacts the book. Ctrl+Shift+S saves and compacts, and he marks that key as undocumented. `percentFreeSpace` of a page or background is the largest free block as a percent of 64K. Deleted objects do not free that space until Save As writes a new file. Each page and each background holds at most 64K of data. That 64K is page data, not the 65,535-character script limit in the compression article.

## Book passwords

https://dennydedmore.com/toolbook/books/OpenScriptReferenceManual.pdf

`ask password <question>` opens a dialog with a question, a typed answer, and OK and Cancel. The question is at most three lines. OK or Enter puts the answer in `IT`. Cancel, Esc, or the control-menu close sets `IT` to null and `sysError` to `cancel`. ToolBook encrypts what the user typed. Compare that encrypted string with `sysPasswords`, or add it to that list. He says to use this to control access to a book.

`sysPasswords` is a system property, get or set. It holds up to ten encrypted passwords, one per text line. The default is null. If ToolBook wants an Author, Open, or Save password and the encrypted form is already in `sysPasswords`, it does not ask. Otherwise it shows the Password dialog. The encrypted form comes from `ask password`, in `IT`.

`failedAuthorPassword` is a viewer property, get only. It is true when a password is required to go from Reader level to Author level and the user types the wrong one. Otherwise it is false.

https://dennydedmore.com/toolbook/knowledgebase/kb/DHTMLPasswords.html, version not stated. The built-in password feature protects the native book. It has no effect on a DHTML lesson in a browser. His suggested lesson gate is a first page with a catalog password field, a submit button, and an explanation, optionally boxed by a rounded rectangle. The password field masks the typing. The Actions Editor on the submit button checks the typed value. That is a lesson page, not `sysPasswords`.

The catalog password field in the previous section is the masking field. It is not the Author, Open, or Save password.
