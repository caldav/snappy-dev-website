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

import logging
import os
import sys
import subprocess

from .settings import ROOT_DIR, RELEASES_BRANCH_MAPPING

logger = logging.getLogger(__name__)


def next_relevant_line(f):
    '''return stripped relevant next line. Ignore comments and blank ones'''
    for line in f:
        if not line or line.startswith("#"):
            continue
        yield line.strip()