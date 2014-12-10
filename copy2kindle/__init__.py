#!/usr/bin/python
# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import os.path
import sys

from . import darwin

def fatal(message):
    sys.stderr.write(message+'\n')
    sys.exit(1)

def do_copy(provider, filenames):
    for f in filenames:
        if not os.path.exists(f):
            fatal(f+' does not exist')
        if not os.path.isfile(f):
            fatal(f+' is not a regular file')
        if not f.endswith('.mobi') and not f.endswith('.azw'):
            fatal(f+' is not a .mobi file')

    kindles = list(provider.find_all())
    if not kindles:
        fatal('Kindle not found')
    if len(kindles) > 1:
        fatal('Too many Kindles')
    kindle = kindles[0]

    kindle.prepare()

    for f in filenames:
        sys.stdout.write('Copying '+f+'\n')
        kindle.copy(f)

    kindle.cleanup()

def main():
    do_copy(darwin, sys.argv[1:])
