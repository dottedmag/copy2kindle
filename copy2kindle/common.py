# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import shutil

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
