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

'''Handling import from different external git branches'''

import logging
import os
import shutil
import subprocess

from .tools import next_relevant_line
from .settings import ROOT_DIR, GIT_IMPORT_MAPPING

logger = logging.getLogger(__name__)


def import_git_external_branches(out_root_dir, temp_repos_dir, release):
    '''Import and create needed path for each external git repository'''

    success = True
    with open(os.path.join(ROOT_DIR, GIT_IMPORT_MAPPING)) as f:
        try:
            for line in next_relevant_line(f):
                (rel_dest_path, git_repo, branch_name, copy_path) = line.split(" ")

                # create destination path, changing release with existing release
                rel_dest_path = rel_dest_path.replace("release", release)
                dest_path = os.path.join(out_root_dir, rel_dest_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                repo_mirror = os.path.join(temp_repos_dir, git_repo.split("/")[-1])
                # ensure we have the repo in temp_repos_dir, otherwise create it
                if not os.path.isdir(repo_mirror):
                    subprocess.check_call(["git", "clone", "-q", "-n", git_repo], cwd=os.path.dirname(repo_mirror))
                subprocess.check_call(["git", "checkout", "-q", branch_name], cwd=repo_mirror)
                shutil.copytree(os.path.join(repo_mirror, copy_path), dest_path, ignore=lambda src, names: [".git"])
        except ValueError:
            logger.error("Import file is not of valid format: <site_path> <repo_url> <branch_name> "
                         "<path_to_content_copy_in_branch>")
            success = False
    return success
