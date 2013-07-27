#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-
#
# $Id: aliasdiff.py $
#
# Author: Markus Stenberg <fingon@iki.fi>
#
# Created:       Sat Mar  9 17:19:41 2013 mstenber
# Last modified: Sat Jul 27 14:22:35 2013 mstenber
# Edit time:     23 min
#
"""

This utility scripts takes one mail-alias file, and compares it with
another. Only the aliases within the first file are actually used for
comparison.

"""

import re

comment_re = re.compile('^#').match
alias_re = re.compile('^(.*[^:]+):(.*)$').match

class AliasFile:
    def __init__(self):
        self.aliases = {}
    def readLines(self, lines):
        for line in lines:
            line = line.strip()
            if len(line) == 0:
                continue
            if comment_re(line) is not None:
                continue
            m = alias_re(line)
            assert m is not None, 'unknown line: %s' % line
            (name, list) = m.groups()
            l = list.split(',')
            l = map(lambda x:x.strip().lower(), l)
            l = filter(lambda x:len(x)>0, l)
            self.addAlias(name, set(l))
    def addAlias(self, name, content):
        old = self.aliases.get(name, set())
        self.aliases[name] = old.union(content)

if __name__ == '__main__':
    import sys
    a1 = AliasFile()
    a1.readLines(open(sys.argv[1]))
    a2 = AliasFile()
    a2.readLines(open(sys.argv[2]))
    kl = a1.aliases.keys()
    kl.sort()
    covered = {}
    for k in kl:
        covered[k] = True
        # Consider contents within a1 <> contents within a2
        h1 = a1.aliases[k]
        h2 = a2.aliases.get(k, None)
        if not h2:
            print '[miss-whole-a2] missing', k, 'from a2 ALTOGETHER'
            continue
        for k2 in h1.difference(h2):
            print '[miss-alias-a2] missing from', k, 'a2', k2
        for k2 in h2.difference(h1):
            print '[miss-alias-a1] missing from', k, 'a1', k2
    kl2 = a2.aliases.keys()
    kl2.sort()
    for k2 in kl2:
        if not covered.has_key(k2):
            print '[miss-whole-a1] missing', k2, 'from a1 ALTOGETHER'

