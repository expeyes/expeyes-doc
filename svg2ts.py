#!/usr/bin/python3

import sys, argparse, gettext, os.path, subprocess, re, xml.dom.minidom

gettext.bindtextdomain('expeyes-doc', os.path.join(os.path.abspath(__file__),"lang"))
gettext.textdomain('expeyes-doc')
_ = gettext.gettext

TSminimal="""\
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS>
<TS version="2.1" language="fr_FR">
<context>
    <name>@default</name>
</context>
</TS>
"""

def error(msg, parser):
    print(msg)
    parser.print_help()
    sys.exit(1)

def warn(msg):
    print(msg, file=sys.stderr)
    return

def identsOf(doc):
    """
    make the set of id attributes found in a TS file
    @param doc an xml.dom.minidom instance
    """
    loc=doc.getElementsByTagName("location")
    return {l.getAttribute("id") for l in loc}


def getTheText(t):
    """
    Extract the textnodes' text from children of a flowPara element
    @param t a flowPara element
    """
    result=""
    first=True
    for tn in t.childNodes:
        if tn.nodeType==3: #TEXT_NODE
            if not first:
                result+="\n"
            else:
                result+=tn.data
    return result

def translatableOf(doc):
    """
    Harvest the translatable strings from a SVG document
    @param doc an xml.doc.minidoc instace parsed from a SVG file
    @return a dictionary identifier => translatable string
    """
    texts=doc.getElementsByTagName("flowPara")
    # harvest all the translatable strings with their ids
    translatable={t.getAttribute("id"): getTheText(t) for t in texts}
    # ignore the empty strings
    return {key: translatable[key] for key in translatable if translatable[key]}

def prettySave(doc, outFile):
    """
    save a prettyfied XML code.
    @param doc an xml.dom.minidom instance
    @param outFile a file name for saving
    """
    pretty=doc.toprettyxml(indent="  ")
    result=""
    for line in pretty.split("\n"):
        line=line.rstrip()
        if line:
            result+=line+"\n"
    open(outFile,"w").write(result)
    return
    
def extractStrings(args, parser):
    if not os.path.exists(args.inSvg[0]):
        error(_("file does not exist: %s") %args.inSvg[0], parser)
    else:
        if args.outTs:
            outTs=args.outTs
        else:
            if re.match(r".*\.svg$", args.inSvg[0], flags=re.I):
                outTs=re.sub("\.svg$", "_en.ts", args.inSvg[0], flags=re.I)
            else:
                outTs=args.inSvg[0]+"_en.ts"
            print(_("extracting strings from {} to {}").format(args.inSvg[0], outTs))
            try:
                doc=xml.dom.minidom.parse(args.inSvg[0])
            except:
                error(_("The document %s is not well-formed SVG") %args.inSvg[0], parser)
            translatable=translatableOf(doc)
            if not os.path.exists(outTs):
                open(outTs,"w").write(TSminimal)
            tDoc=xml.dom.minidom.parse(outTs)
            idents=identsOf(tDoc)
            context=tDoc.getElementsByTagName("context")[0]
            for i in translatable:
                if i in idents:
                    warn(_("{ident} was already defined in {file}").format(ident=i, file=outTs))
                    continue
                message=tDoc.createElement("message")
                location=tDoc.createElement("location")
                filename=tDoc.createAttribute("filename")
                filename.value=args.inSvg[0]
                location.setAttributeNode(filename)
                message.appendChild(location)
                source=tDoc.createElement("source")
                text=tDoc.createTextNode(translatable[i])
                source.appendChild(text)
                message.appendChild(source)
                translation=tDoc.createElement("translation")
                text=tDoc.createTextNode("")
                translation.appendChild(text)
                message.appendChild(translation)
                comment=tDoc.createElement("comment")
                text=tDoc.createTextNode(i)
                comment.appendChild(text)
                message.appendChild(comment)
                context.appendChild(message)
            prettySave(tDoc, outTs)
    return

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description=_("make a translation file from SVG content"),
        prog="svg2ts",
    )
    parser.add_argument('inSvg', nargs=1,
                        help=_('Input SVG file'),
    )
    parser.add_argument('outTs', nargs='?',
                        help=_('Output TS file; defaults to the same filename with .ts suffix'),
    )
    args=parser.parse_args(sys.argv[1:])
    extractStrings(args, parser)
    
