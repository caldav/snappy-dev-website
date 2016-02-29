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

'''Copying and treating files internal metadata'''

import logging
import os
import re

logger = logging.getLogger(__name__)


def import_and_copy_file(source_path, destination_path):
    '''Copy and import file content.

    We handle:
        1. symlinks are replaced with real files
        2. ##IMPORT <file_path> to copy destination file content into current file
            (note: we don't handle IMPORT of IMPORT right now as we don't have this use case)

    We return an error if we couldn't copy or import all listed filed
    '''
    success = True
    import_regexp = re.compile("##IMPORT (.*)")
    with open(destination_path,'w') as dest_f:
        with open(source_path) as source_f:
            for line in source_f:
                result = import_regexp.findall(line)
                if result:
                    path = result[0]
                    try:
                        with open(os.path.join(os.path.dirname(source_path)), path) as import_f:
                            for line_import in import_f:
                                dest_f.write(line_import)
                    except FileNotFoundError:
                        logger.error("Couldn't import {} from {}".format(source_path, source_path))
                        success = False
                dest_f.write(line)
    return success

