#!/usr/bin/python3

import sys, argparse, gettext, os.path, subprocess, re, xml.dom.minidom, copy

gettext.bindtextdomain('expeyes-doc', os.path.join(os.path.abspath(__file__),"lang"))
gettext.textdomain('expeyes-doc')
_ = gettext.gettext

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

def error(msg, parser):
    print(msg)
    parser.print_help()
    sys.exit(1)

def warn(msg):
    print(msg, file=sys.stderr)
    return

def enforceSuffix(suf, filename):
    """
    enforce a suffix for a file name
    """
    result=filename
    if filename.endswith("."+suf):
        pass
    else:
        result+="."+suf
    return result

def translatableElementsOf(doc):
    """
    Harvest the translatable strings from a SVG document
    @param doc an xml.doc.minidoc instace parsed from a SVG file
    @return a dictionary identifier => xml element
    """
    texts=doc.getElementsByTagName("flowPara")
    # harvest all the translatable strings with their ids
    translatable={t.getAttribute("id"): t for t in texts}
    # ignore the empty strings
    return {key: translatable[key] for key in translatable if translatable[key]}
    
def translationsOf(trdoc):
    """
    Gets translations from a TS file
    @param trdoc an xml.dom.minidom instance parsed from a TS file
    @return a dictionary identifier => translated string
    """
    messages=trdoc.getElementsByTagName("message")
    result={}
    for m in messages:
        ident=m.getElementsByTagName("comment")[0].firstChild.data
        transTextNode=m.getElementsByTagName("translation")[0].firstChild
        if transTextNode:
            trans=transTextNode.data
        else:
            trans=m.getElementsByTagName("source")[0].firstChild.data
        result[ident]=trans
    return result

def translateDoc(doc,translations):
    """
    translates an SVG file
    @param doc an xml.doc.minidoc instace parsed from a SVG file
    @param translations a dictionary identifier => translated string
    @return a deep copy of doc, with translations applied
    """
    auxDoc=xml.dom.minidom.parseString("<ts></ts>")
    doc=copy.deepcopy(doc)
    translatable=translatableElementsOf(doc)
    translated={} # dictionary of id => elements which need no longer to be managed
    for ident in translatable:
        text=""
        if ident in translations and ident not in translated:
            # search whether there are other texts to be concatenated
            # i.e. whether there are next siblings with non-empty text
            # first keep the current text available at id==ident
            text+=translations[ident]
            # create a pointer to the possible text chain
            chainBegin=ident
            # the boolean finished will control the following loop
            finished=False
            while not finished:
                # finished will remain True is no next text is detected
                finished=True
                for maybeNext in translatable:
                    # test whether there is a non-empty (translated) next text
                    if translatable[maybeNext] == \
                       translatable[chainBegin].nextSibling and \
                       maybeNext in translations:
                        # when a next text is detected,
                        isNext=maybeNext
                        # its content is accumulated,
                        text += " "+translations[isNext]
                        # its id is added to the set of already seen texts,
                        translated[isNext]=translatable[isNext]
                        # the pointer of the chain is shifted forward,
                        chainBegin=isNext
                        # and the search for next text must be reactivated.
                        finished=False
            newTextNode=auxDoc.createTextNode(text)
            t=translatable[ident]
            t.replaceChild(newTextNode,t.firstChild)
        # now we must get rid of any text which was accumulated as
        # next text
        for ident in translated:
            node=translated[ident]
            if node.parentNode:
                node.parentNode.removeChild(node)
    return doc


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
    open(outFile,"w", encoding="utf-8").write(result)
    return
    
def translate(args, parser):
    """
    translates an SVG file
    @param args a NameSpace with variables inSvg, inTS and outSvg
    @parser an argparse parser instance, to keep the help message
    """
    ok=True
    msg=[]
    if not os.path.exists(args.inSvg[0]) :
        msg.append( _("Non-existent file: {}").format(args.inSvg[0]))
        ok=False
    if not os.path.exists(args.inTs[0]) :
        msg.append( _("Non-existent file: {}").format(args.inTs[0]))
        ok=False
    if not ok:
        error("\n".join(msg), parser)
    inSvg=args.inSvg[0]
    inTs=args.inTs[0]
    outSvg=enforceSuffix('svg', args.outSvg[0])
    doc=xml.dom.minidom.parse(inSvg)
    trdoc=xml.dom.minidom.parse(inTs)
    translations=translationsOf(trdoc)
    newdoc=translateDoc(doc,translations)
    prettySave(newdoc, outSvg)
    return

if __name__=="__main__":
    parser = argparse.ArgumentParser(
        description=_("Translate strings of an SVG file"),
        prog="translateSvg",
    )
    parser.add_argument('inSvg', nargs=1,
                        help=_('Input SVG file'),
    )
    parser.add_argument('inTs', nargs=1,
                        help=_('input TS file'),
    )
    parser.add_argument('outSvg', nargs=1,
                        help=_('Output SVG file'),
    )
    args=parser.parse_args(sys.argv[1:])
    translate(args, parser)
    
