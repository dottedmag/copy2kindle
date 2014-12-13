# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import os.path
import sys

__all__ = ['filter_files', 'do_copy']

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

def filter_files(filenames, strict):
    passed = filter(check_file, filenames)
    if strict:
        if len(passed) != len(filenames):
            sys.exit(1)
    return passed

def do_copy(kindle, filenames):
    kindle.prepare()
    for f in filenames:
        sys.stdout.write('Copying '+f+'\n')
        kindle.copy(f)
    kindle.cleanup()
