# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import os.path
import sys

def err(message):
    sys.stderr.write(message+'\n')

def check_file(f):
    if not os.path.exists(f):
        err(f+' does not exist')
        return False
    if not os.path.isfile(f):
        err(f+' is not a regular file')
        return False
    if not f.endswith('.mobi') and not f.endswith('.azw'):
        err(f+' is not a .mobi file')
        return False
    return True

def do_copy(provider, filenames, strict):
    passed = filter(check_file, filenames)
    if strict:
        if len(passed) != len(filenames):
            sys.exit(1)
    kindles = list(provider.find_all())
    if not kindles:
        err('Kindle not found')
        sys.exit(1)
    if len(kindles) > 1:
        err('Too many Kindles')
        sys.exit(1)
    kindle = kindles[0]

    kindle.prepare()

    for f in passed:
        sys.stdout.write('Copying '+f+'\n')
        kindle.copy(f)

    kindle.cleanup()
