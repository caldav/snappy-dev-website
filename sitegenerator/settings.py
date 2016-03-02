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

'''Variables and settings constants'''

import os

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_SRC = os.path.join(ROOT_DIR, "src")

OUTPUT_DIR = os.path.join(ROOT_DIR, "out")

# important mapping files
RELEASES_BRANCH_MAPPING = "releases"
GIT_IMPORT_MAPPING = "import-mapping"
VARIABLES_MAPPING = "variables-mapping"

PREPEND_TOUR_TEMPLATES = {
    "as-dev": "This content is part of the snappy developer tour, feel free to hop on it!",
    # "as-devops": "This content is part of the snappy devops tour, feel free to hop on it!",
    # "as-boardmaker": "This content is part of the snappy board maker tour, feel free to hop on it!"
}
