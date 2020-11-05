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
NOTES_FOLDER_PATH = Path("~/notes").expanduser()
EXISTING_NOTES = [
    note.name[:-3] for note in NOTES_FOLDER_PATH.iterdir() if note.name.endswith(".md")
]


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
def note():
    """Note management related commands """


@note.command()
@argument("name", help="The name of the new note.", type=click.Choice(EXISTING_NOTES))
def new(name):
    """Create or open a note with the given name """
    notepath = NOTES_FOLDER_PATH.joinpath(f"{name}.md")
    if notepath.is_file():
        LOGGER.warning(f"Note {name} already exists, opening it.")
    else:
        notepath.touch()
    default_open(notepath)


@note.command("list")
def list_():
    """List notes """
    root_categories = defaultdict(list)
    for note in NOTES_FOLDER_PATH.iterdir():
        if not (note.name.endswith(".md") or note.name.endswith(".txt")):
            continue
        root_categories[note.name.split(".")[0]].append(note)
    for cat, notes in root_categories.items():
        print(f"--  {cat}:")
        for note in notes:
            print(f"  {note.as_posix()}")
