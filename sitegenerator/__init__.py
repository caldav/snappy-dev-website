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

import logging
import os
import sys

from . import settings
from releases import get_releases_in_context

logger = logging.getLogger(__name__)


def main():
    '''Main entry point'''
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    # ensure that out doen't exist. If it exists, bail out
    if os.path.exists(settings.OUTPUT_DIR):
        logger.error("{} exists, please delete it first".format(settings.OUTPUT_DIR))
        sys.exit(1)

    if not os.path.exists(settings.SITE_SRC):
        logger.error("{} is required".format(settings.OUTPUT_DIR))
        sys.exit(1)

    for release in get_releases_in_context():
        print(release)


    # 2. handle setup/ generation p


