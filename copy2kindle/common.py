# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import shutil
import sys

def fatal(message):
    sys.stderr.write(message+'\n')
    sys.exit(1)

class Kindle(object):
    def __init__(self, mountpoint):
        self.mountpoint = mountpoint
        self.needs_unmount = False

    def prepare(self):
        if self.mountpoint == '':
            self.needs_unmount = True
            self.mountpoint = self._do_mount()

    def cleanup(self):
        if self.needs_unmount:
            self._do_unmount()

    def copy(self, filename):
        shutil.copy(filename, self.mountpoint + '/documents')

def find_kindle(provider, pattern):
    kindles = list(provider.find_all())
    if not kindles:
        fatal('Kindle not found')
    if pattern:
        matched = filter(lambda x: x.match(pattern), kindles)
        if not matched:
            fatal('No Kindle matches %s' % pattern)
        if len(matched) > 1:
            fatal('Too many Kindles match %s' % pattern)
        return matched[0]
    if len(kindles) > 1:
        fatal('Too many Kindles')
    return kindles[0]
