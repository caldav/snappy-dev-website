#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Canonical
#
# Authors:
#  Didier Roche
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

'''General tools for handling files and metadata'''

import argparse
from contextlib import contextmanager
import logging
import os
import sys
import subprocess

from .settings import ROOT_DIR, RELEASES_BRANCH_MAPPING, OUTPUT_DIR

logger = logging.getLogger(__name__)


def next_relevant_line(f):
    '''Return stripped relevant next line. Ignore comments and blank ones'''
    for line in f:
        if not line or not line.strip() or line.startswith("#"):
            continue
        yield line.strip()


@contextmanager
def replace_file_inline(path):
    '''Replace a file atomically creating a temp .new one

    Skip non text files'''

    temp_file = "{}.new".format(path)
    try:
        with open(temp_file, 'w') as dest_f:
            with open(path) as source_f:
                yield (source_f, dest_f)
        os.rename(temp_file, path)
    except UnicodeDecodeError as e:
        # That should be the case of any binary files
        logger.debug("Couldn't replace in {}: {}".format(path, e))
        os.remove(temp_file)


def setup_args():
    '''Handle CLI arg setup'''
    parser = argparse.ArgumentParser(description="Generate in the {} directory the developer website "
                                                 "content, fetching from different sources.".format(OUTPUT_DIR))
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase output verbosity (2 levels)")
    parser.add_argument("-d", "--debug", action="store_true", help="Max verbose output (2nd level)")

    args = parser.parse_args(sys.argv[1:])
    setup_logging_level(args)


def setup_logging_level(args):
    level = logging.WARNING
    if args.verbose == 1:
        level = logging.INFO
    if args.verbose > 1 or args.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")
