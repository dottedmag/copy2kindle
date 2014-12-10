#!/usr/bin/python
# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import sys
import os.path
import argparse
import plistlib
import subprocess32
subprocess = subprocess32
import collections
import shutil


def run_diskutil(args):
    with open('/dev/null', 'r') as devnull:
        return subprocess.check_output(
            ['/usr/sbin/diskutil'] + args, stdin=devnull)


def parse_plist(contents):
    return plistlib.readPlistFromString(contents)

Disk = collections.namedtuple('Disk', ['dev', 'partitions'])


def partitions(disk):
    if 'Partitions' not in disk:
        return
    for partition in disk['Partitions']:
        yield partition['DeviceIdentifier']


def disks():
    i = parse_plist(run_diskutil(['list', '-plist']))
    for disk in i['AllDisksAndPartitions']:
        yield Disk(disk['DeviceIdentifier'], list(partitions(disk)))


def info(disk):
    return parse_plist(run_diskutil(['info', '-plist', disk]))

Kindle = collections.namedtuple('Kindle', ['dev', 'mountpoint'])


def find_kindles():
    for disk in disks():
        i = info(disk.dev)
        if i['MediaName'] == 'Kindle Internal Storage Media':
            pi = info(disk.partitions[0])
            yield Kindle(disk.partitions[0], pi['MountPoint'])


def is_mounted(kindle):
    return kindle.mountpoint != ''


def mount(kindle):
    run_diskutil(['mount', kindle.dev])
    return Kindle(kindle.dev, info(kindle.dev)['MountPoint'])


def unmount(kindle):
    run_diskutil(['unmount', kindle.dev])


def fatal(message):
    sys.stderr.write(message+'\n')
    sys.exit(1)

def do_copy(filenames):
    for f in filenames:
        if not os.path.exists(f):
            fatal(f+' does not exist')
        if not os.path.isfile(f):
            fatal(f+' is not a regular file')
        if not f.endswith('.mobi') and not f.endswith('.azw'):
            fatal(f+' is not a .mobi file')

    kindles = list(find_kindles())
    if not kindles:
        fatal('Kindle not found')
    if len(kindles) > 1:
        fatal('Too many Kindles')
    kindle = kindles[0]

    do_unmount = False
    if not is_mounted(kindle):
        do_unmount = True
        kindle = mount(kindle)

    destdir = kindle.mountpoint + '/documents'

    for f in filenames:
        sys.stdout.write(f+' -> '+destdir+'\n')
        shutil.copy(f, destdir)

    if do_unmount:
        unmount(kindle)

def main():
    do_copy(sys.argv[1:])