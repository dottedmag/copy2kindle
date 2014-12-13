# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import collections
import plistlib
import sys
import time

from . import common

try:
    import subprocess
    subprocess.TimeoutExpired
except AttributeError:
    import subprocess32
    subprocess = subprocess32

__all__ = ['find_all']

def run_diskutil(args):
    with open('/dev/null', 'r') as devnull:
        return subprocess.check_output(
            ['/usr/sbin/diskutil'] + args, stdin=devnull)


def parse_plist(contents):
    return plistlib.readPlistFromString(contents)


def info(disk):
    return parse_plist(run_diskutil(['info', '-plist', disk]))


def partitions(disk):
    if 'Partitions' not in disk:
        return
    for partition in disk['Partitions']:
        yield partition['DeviceIdentifier']


Disk = collections.namedtuple('Disk', ['dev', 'partitions'])


def disks():
    i = parse_plist(run_diskutil(['list', '-plist']))
    for disk in i['AllDisksAndPartitions']:
        yield Disk(disk['DeviceIdentifier'], list(partitions(disk)))


def try_do(command, max_attempts=10, delay=0.5):
    attempt = 1
    while attempt < max_attempts:
        try:
            return command(attempt)
        except:
            time.sleep(delay)
            attempt += 1
    return command(max_attempt)


class DarwinKindle(common.Kindle):
    def __init__(self, diskdev, dev, volume, mountpoint):
        super(DarwinKindle, self).__init__(mountpoint)
        self.diskdev = diskdev
        self.dev = dev
        self.volume = volume

    def _do_mount(self):
        run_diskutil(['mount', self.dev])
        sys.stdout.write('Mounted '+self.dev+'\n')
        return info(self.dev)['MountPoint']

    def _run_unmount(self, attempt):
        run_diskutil(['unmount', self.dev])
        sys.stdout.write('Unmounted '+self.dev)
        if attempt > 1:
            sys.stdout.write(' (attempt %d)' % attempt)
        sys.stdout.write('\n')

    def _do_unmount(self):
        # OS X takes some time to examine disk after mount, so
        # mount+copy+unmount fails. Try it several times in a row.
        try_do(self._run_unmount)

    def match(self, pattern):
        return pattern in[self.dev, self.diskdev, self.volume]


def find_all():
    for disk in disks():
        i = info(disk.dev)
        if i['MediaName'] == 'Kindle Internal Storage Media':
            pi = info(disk.partitions[0])
            yield DarwinKindle(disk.dev, disk.partitions[0], pi['VolumeName'],
                               pi['MountPoint'])
