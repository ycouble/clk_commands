#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from pathlib import Path
import subprocess
import sys
import random

import click
from click_project.decorators import group, command, argument, option, flag
from click_project.log import get_logger


LOGGER = get_logger(__name__)
FILE_PATH = Path("~/notes/todo.articles.md").expanduser()
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


@group(invoke_without_command=True)
def read():
    """Commands related to the reading list"""
    _get(urls, True)


@read.command()
@argument(
    "url", help="the url to add"
)
def add(url):
    """Create or open a note with the given name """
    if url in urls:
        LOGGER.warning("url already present in the list")
        return
    if "?" in url:
        url = url[:url.index("?")]
        LOGGER.warning(f"Cropping url to: {url}")
    with open(FILE_PATH, "a") as f:
        f.write(url + "\n")

@read.command()
def edit():
    """Edit the article note"""
    default_open(FILE_PATH)

def _get(_urls, random_):
    """get the first / random item of the list"""
    if random_:
        url = random.choice(_urls)
    else:
        url = _urls[0]
    print(url)
    return url

@read.command()
@flag(
    "--random/--no-random",
    "random_",
    help="Get the first / a random one in the list",
    default=True,
)
def get(random_):
    """Get the first article of the list"""
    _get(urls, random_)

def _delete(_urls, url):
    url = url + "\n"
    present = True
    while present:
        try:
            _urls.remove(url)
        except ValueError:
            present = False
    with open(FILE_PATH, "w") as f:
        f.writelines(_urls)

@read.command(name="del")
@argument("url", help="Url to remove")
def delete(url):
    """Remove the given url from the list"""
    _delete(urls, url)

@read.command()
@flag(
    "--random/--no-random",
    "random_",
    help="Get the first / a random one in the list",
    default=False,
)
def pop(random_):
    """Get the first / a random article of the list"""
    url = _get(urls, random_)
    _delete(urls, url)
