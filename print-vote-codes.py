#!/usr/bin/env python
# synopsis: print-vote-codes <filename>

import sys
from pickle import load

TITLE = "Kindergarten St. Michael Elternumfrage 2015"
URL = "http://digitalarbeiter.de:8080/"
VOTECODE_FMT = "Vote-Code: %i"
sep = max(len(TITLE), len(URL)) * "-"
vc = load(file(sys.argv[1], "rb"))
for c in vc:
    print sep
    print TITLE
    print URL
    print VOTECODE_FMT % c
    print sep
    print ""
    print ""
    print ""
