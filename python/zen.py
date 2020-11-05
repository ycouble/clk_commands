#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
from click_project.decorators import group, command, argument
from click_project.log import get_logger


LOGGER = get_logger(__name__)


def pyzen():
    import this


def ycozen():
    print("Curious is better than nothing")
    print("Be interested in people")


ZENS = {
    "python": pyzen,
    "yco": ycozen,
}


@command()
@argument("topic", help="The topic to display the zen of")
def zen(topic):
    """Displays the zen of a topic"""
    ZENS[topic]()
