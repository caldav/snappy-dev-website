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

'''Release-related misc utilities'''

import logging
import os
import sys
import subprocess

from .settings import ROOT_DIR
from .tools import next_relevant_line

logger = logging.getLogger(__name__)


def _get_supported_releases_map():
    '''load supported release and master branch map'''
    release_map = {}
    with open(os.path.join(ROOT_DIR, "releases")) as f:
        try:
            for line in next_relevant_line(f):
                (release, branch_name) = line.split(" ")
                release_map[release] = branch_name
        except ValueError:
            logger.error("Release file is not of valid format: <release_name> <branch>")
            sys.exit(1)
    return release_map


def get_releases_in_context():
    '''Prepare for one release, switching context and return release name'''
    for release, branch in _get_supported_releases_map().items():
        subprocess.check_call(["git", "checkout", "-q", branch])
        yield release
