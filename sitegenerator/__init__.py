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
import tempfile

from . import settings
from .fileshandling import import_and_copy_file, replace_variables, reformat_links
from .gitimporter import import_git_external_branches
from .releases import get_releases_in_context, load_device_metadata

logger = logging.getLogger(__name__)


def main():
    '''Main entry point'''
    logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    # Ensure that the generated directory doen't exist. If it exists, bails out
    if os.path.exists(settings.OUTPUT_DIR):
        logger.error("{} exists, please delete it first".format(settings.OUTPUT_DIR))
        sys.exit(1)
    os.makedirs(settings.OUTPUT_DIR)

    if not os.path.exists(settings.SITE_SRC):
        logger.error("{} is required".format(settings.SITE_SRC))
        sys.exit(1)

    # Loop and switch for each release context
    for release in get_releases_in_context():
        output_for_release_dir = os.path.join(settings.OUTPUT_DIR, release)

        # Load device metadata and variable substitution
        devices = load_device_metadata()

        # 1. Handle external branch imports (because other pages can import them)
        with tempfile.TemporaryDirectory() as tmp_dirname:
            success = import_git_external_branches(output_for_release_dir, tmp_dirname)
        if not success:
            sys.exit(1)

        # 2. Handle local directory and files copy + import statements in files
        for path, dirs, files in os.walk(settings.SITE_SRC):
            for file_name in files:
                os.makedirs(path, exist_ok=True)
                file_path = os.path.join(path, file_name)
                dest_path = file_path.replace(settings.SITE_SRC, output_for_release_dir)
                if not import_and_copy_file(file_path, dest_path):
                    success = False



        # 2. Handle get-started and prepend "this is part of the tour" link

        # 3. Copy and import from other branches


