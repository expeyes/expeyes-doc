expeyes-doc
===========

Documentation for expEYES and expEYES-junior

## Translating the brochure for expeyes-17 ##

### Dependencies ###

In order to work efficiently, you need a little set of tools:
  * GNU **make**, to automatically rebuild documents
  * **Python3**, which is called by the `make` scripts
  * **Qt5's language tools**: linguist, lconvert
  
If you cannot install those tools properly, you can still contribute:
editing the files `Back_??.ts` and `Front_??.ts` is enough. However, with
the suitable tools, you can see the final document, so you gain immediate
feedback.

### Working on translations ###

  * get a copy of the repository, either a zip file of a git clone
  * go to the subdirectory for your language (currently featured: de, es, fr, nl), and then to the subdirectory `Brochure-eyes17`
  * run the command `make` to update files. This updates translatable strings from the English documents, and applies current translations to the localized version of SVG files
  * run the command `linguist Back_??.ts`, where `??` stand for the two-letters code of your language, if you want to translate strings for the file `Back.svg`. The same method is ok for the other files: `.ts` files are translation files, and the command `linguist` allows you to update translations.
  * when translations were updated by you, run once again `make` to refresh the SVG document.
  * the SVG documents can be viewed properly with the command `inkscape`
  
### tuning finely the SVG documents ###

When the automatic translation with `make` gives an almost correct document, there are generally little details to fix. Every language uses longer or shorter phrases to express the same idea, so some paragraphs mays be wrongly located in the graphic layout. To fix those details, the best is to work on a copy.

  * copy the files `Back.svg` and `Front.svg` in the subdirectory `hand-rewritten`
  * open the files with the command `inkscape` and perform any needed modifications. Usual modifications are:
    * Changing the size of the font in a paragraph. If you select the paragraph, and open the Text tool, it is possible to select a font size and `Apply` the changes.
	* Changing the shape of a paragraph, for example its width. One easy way to do it is to enter the "on-screen text edit mode": double-click the paragraph, until you see a text cursor blinking in the text; then, the bounding box which contains the text can be modified with your mouse.
	* Modifying the overall geometry, for example to take in account margins of your printer. Please notice that Inkscape's aligning tools will be more useful for this is all the objects are grouped in a single object, which can be positioned precisely in the page as a whole.
