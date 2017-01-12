'''
Created on Jan 6, 2017

@author: Administrator
'''
from xml.dom.minidom import parse

XML = """
<nodeA>
    <nodeB>Text hello</nodeB>
    <nodeC><noText></noText></nodeC>
</nodeA>
"""


def replaceText(node, newText):
    if node.firstChild.nodeType != node.TEXT_NODE:
        raise Exception("node does not contain text")

    node.firstChild.replaceWholeText(newText)

def main():
    doc = parseString(XML)

    node = doc.getElementsByTagName('nodeB')[0]
    replaceText(node, "Hello World")

    print doc.toxml()

    try:
        node = doc.getElementsByTagName('nodeC')[0]
        replaceText(node, "Hello World")
    except:
        print "error"


xmlFile = parse( FILE_PATH )

for script in SCRIPTS:

    newScript = xmlFile.createElement("script")

    newScript.setAttribute("name"  , script.name)
    newScript.setAttribute("action", script.action)

    newScriptText = xmlFile.createTextNode( script.description )

    newScript.appendChild( newScriptText  )
    xmlFile.childNodes[0].appendChild( newScript )

print xmlFile.toprettyxml()


# if __name__ == '__main__':
#     main()