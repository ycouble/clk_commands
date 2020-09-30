#!/usr/bin/env python3
import os
import subprocess
import sys

import click
from click_project.decorators import group, command, argument
from click_project.log import get_logger


LOGGER = get_logger(__name__)
CONFIG_PATH = os.path.expanduser("~/.local/share/clk/git.txt")


@group()
def git():
    """ Git repositories related commands """
    LOGGER.debug("creating config file if it doesn't exist")
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH))
    except FileExistsError:
        pass
    if not os.path.isfile(CONFIG_PATH):
        with open(CONFIG_PATH, "a+"):
            pass

@git.command()
@argument("path", help="The path to a git repository")
def add(path):
    """ Add a git repository to the command git tracking """
    path = os.path.abspath(os.path.expanduser(path))
    if not os.path.isdir(path):
        LOGGER.error(f"Path {path} is not a directory")
        sys.exit(1)
    ret = subprocess.call(
        ["git", "status"],
        cwd=path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if ret:
        LOGGER.error(f"Directory {path} is not a git repository")
        sys.exit(1)
    with open(CONFIG_PATH, "r") as paths:
        existing_paths = paths.readlines()
        if path in [p.replace('\n', '') for p in existing_paths]:
            LOGGER.warning(f"Path {path} already in tracked repositories")
            return
    with open(CONFIG_PATH, "a+") as f:
        LOGGER.info(f"Adding path {path} to the tracked repositories")
        f.write(path + "\r\n")

@git.command()
def list():
    """ List tracked git repositories """
    with open(CONFIG_PATH, "r") as f:
        for path in f.readlines():
            print(path)

@git.command()
def status():
    """ Get the git status for each tracked git repository """
    with open(CONFIG_PATH, "r") as f:
        for path in [p.replace('\n', '') for p in f.readlines()]:
            LOGGER.info("")
            LOGGER.info(f"==== GIT STATUS for {path} ====")
            subprocess.call(["git", "status", "-s"], cwd=path)
