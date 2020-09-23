#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import cowsay as cowsaylib
import click
from click_project.decorators import command, argument, flag, option
from click_project.log import get_logger


LOGGER = get_logger(__name__)


@command()
@argument("word", help="The word to say")
@flag("--shout/--dont-shout", help="Shout the word")
@option("--animal", type=click.Choice(cowsaylib.char_names),
        help="The animal that will speak", default="cow")
def cowsay(word, shout, animal):
    """Let the cow say something"""
    LOGGER.debug("Running the command cowsay")
    if shout:
        word = word.upper() + "!"
    speaker = getattr(cowsaylib, animal)
    speaker(word)
