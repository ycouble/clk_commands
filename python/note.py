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
    _note.name[:-3]
    for _note in NOTES_FOLDER_PATH.iterdir()
    if _note.name.endswith(".md")
]


class Suggestion(click.Choice):
    """Allow all choices + any other value"""

    def convert(self, value, param, ctx):
        return value

    def get_metavar(self, param):
        return "[{}|...]".format(
            "|".join(list(self.choices)[: max(3, len(self.choices))])
        )

    def get_missing_message(self, param):
        return "Either choose from:\n\t{}." " or provide a new one".format(
            ",\n\t".join(self.choices)
        )


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
@argument(
    "name", help="The name of the note to create/edit.", type=Suggestion(EXISTING_NOTES)
)
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
    for _note in NOTES_FOLDER_PATH.iterdir():
        if not (_note.name.endswith(".md") or _note.name.endswith(".txt")):
            continue
        root_categories[_note.name.split(".")[0]].append(_note)
    for cat, notes in root_categories.items():
        print(f"--  {cat}:")
        for _note in notes:
            print(f"  {_note.as_posix()}")


@note.command()
@argument("name", help="The note to print", type=click.Choice(EXISTING_NOTES))
def cat(name):
    """Displays an in terminal markdown impression of the note"""
    notepath = NOTES_FOLDER_PATH.joinpath(f"{name}.md")
    if name not in EXISTING_NOTES:
        LOGGER.error(f"No note by the name {name}")
        return
    if subprocess.call(
        "command -v mdv".split(" "),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ):
        LOGGER.error(
            "You need the mdv command to be able to cat a note.\n"
            "Use `pip[x] install mdv` to install it."
        )
    subprocess.call(["mdv", notepath.as_posix()])
