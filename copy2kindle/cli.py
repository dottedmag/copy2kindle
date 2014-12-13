# Copyright (c) 2014 Mikhail Gusarov <dottedmag@dottedmag.net>
# BSD 2-clause license. See COPYING for details.

import argparse
import sys

from . import darwin
from . import copier
from . import common

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--sloppy', action='store_true',
                    help='skip missing files and files of unknown type')
parser.add_argument('-m', '--match',
                    help='match Kindle by volume name or device name, e.g.'+
                        ' disk4 or KINDLE_PAPERWEIGHT')
parser.add_argument('file', nargs='*',
                    help='.mobi file(s) to be copied')

def main():
    args = parser.parse_args()
    if not len(args.file):
        parser.print_help()
        sys.exit(0)

    filenames = copier.filter_files(args.file, not args.sloppy)
    kindle = common.find_kindle(darwin, args.match)
    copier.do_copy(kindle, filenames)
