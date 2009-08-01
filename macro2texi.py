#! /usr/bin/env python

assert __name__ == "__main__"

import sys
from macro import Macro, writeFile

tmpl = """\
@node %(name)s
@unnumbered %(name)s

@majorheading Synopsis

%(synopsis)s

@majorheading Description

%(description)s

@majorheading Homepage

@url{http://www.nongnu.org/autoconf-archive/%(name)s.html}

@majorheading License

%(authors)s

%(license)s
"""

def quoteTexi(buf):
  return buf.replace('@', "@@").replace('{', "@{").replace('}', "@}")

def formatParagraph(para):
  assert para
  assert para[0]
  assert para[0][0]
  if para[0][0].isspace():
    return "@smallexample\n%s\n@end smallexample" % quoteTexi('\n'.join(para))
  else:
    return quoteTexi('\n'.join(para))

def formatAuthor(a):
  assert a
  a["year"] = quoteTexi(a["year"])
  a["name"] = quoteTexi(a["name"])
  if "email" in a:
    a["email"] = quoteTexi(a["email"])
    return "Copyright @copyright{} %(year)s %(name)s @email{%(email)s}" % a
  else:
    return "Copyright @copyright{} %(year)s %(name)s" % a

if len(sys.argv) != 3:
  raise Exception("invalid command line syntax: %s" % ' '.join(map(repr, sys.argv)))
(m4File,outFile) = sys.argv[1:]
assert outFile != m4File
m = Macro(m4File)
m.synopsis = "@smallexample\n%s\n@end smallexample" % "\n".join(map(quoteTexi, m.synopsis))
m.description = '\n\n'.join(map(formatParagraph, m.description))
m.description = m.description.replace("@end smallexample\n@smallexample", "\n")
m.authors = " @* ".join(map(formatAuthor, m.authors))
m.license = "\n\n".join(map(formatParagraph, m.license))
writeFile(outFile, tmpl % m.__dict__)