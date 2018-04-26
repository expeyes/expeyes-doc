#!/usr/bin/python3

import sys, argparse, gettext, os.path, subprocess, re, xml.dom.minidom

gettext.bindtextdomain('expeyes-doc', os.path.join(os.path.abspath(__file__),"lang"))
gettext.textdomain('expeyes-doc')
_ = gettext.gettext

def error(msg, parser):
    print(msg)
    parser.print_help()
    sys.exit(1)

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
    
def extractStrings(args, parser):
    if not os.path.exists(args.inSvg[0]):
        error(_("file does not exist: %s") %args.inSvg[0], parser)
    else:
        if args.outTs:
            outTs=args.outTs
        else:
            if re.match(r".*\.svg$", args.inSvg[0], flags=re.I):
                outTs=re.sub("\.svg$", ".ts", args.inSvg[0], flags=re.I)
            else:
                outTs=args.inSvg[0]+".ts"
            print(_("extracting strings from {} to {}").format(args.inSvg[0], outTs))
            try:
                doc=xml.dom.minidom.parse(args.inSvg[0])
            except:
                error(_("The document %s is not well-formed SVG") %args.inSvg[0], parser)
            texts=doc.getElementsByTagName("flowPara")
            # harvest all the translatable strings with their ids
            translatable={t.getAttribute("id"): getTheText(t) for t in texts}
            # ignore the empty strings
            translatable={key: translatable[key] for key in translatable if translatable[key]}
            print (translatable)
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
    
