#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from pathlib import Path
import subprocess
import sys

import click
from click_project.decorators import group, command, argument, option
from click_project.log import get_logger


LOGGER = get_logger(__name__)
FILE_PATH = Path("~/notes/todo.music.md").expanduser()
with open(FILE_PATH, "r") as f:
    urls = f.readlines()


def default_open(something_to_open):
    """Open given file with default user program."""
    if sys.platform.startswith("linux"):
        LOGGER.info("Calling xdg-open")
        subprocess.call(["xdg-open", something_to_open])
    elif sys.platform.startswith("darwin"):
        LOGGER.info("Calling open")
        subprocess.call(["open", something_to_open])
    elif sys.platform.startswith("win"):
        LOGGER.info("Calling start")
        subprocess.call(["start", something_to_open], shell=True)


@group()
def music():
    """Music downloads related commands """


@music.command()
@argument(
    "url", help="the url to add"
)
def add(url):
    """Create or open a note with the given name """
    if url in urls:
        LOGGER.warning("url already present in the list")
        return
    with open(FILE_PATH, "a") as f:
        f.write(url + "\n")
