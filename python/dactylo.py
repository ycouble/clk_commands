#!/usr/bin/env python3
import datetime
import os.path
from contextlib import contextmanager

import pandas as pd
from click_project.decorators import command, argument, option, group


DACTYLO_FILEPATH=os.path.expanduser("~/public_data/dactylo.csv")
DACTYLO_COLS=["date", "source", "wpm"]

@contextmanager
def open_df_from_file(path: str):
    if os.path.isfile(path):
        df = pd.read_csv(path, parse_dates=True)
    else:
        df = pd.DataFrame({}, columns=DACTYLO_COLS)
    try:
        yield df
    finally:
        df.to_csv(path, index=False)



@group()
def dactylo():
    """ dactylo related commands """


@dactylo.group()
def keybr():
    """ keybr related commands """


@keybr.command()
@argument("wpm", help="words per minute")
@option("--date", help="date of the record", default=datetime.datetime.today())
def add(wpm, date):
    """ add a record for keybr """
    with open_df_from_file(DACTYLO_FILEPATH) as df:
        df.loc[df.shape[0] + 1] = {"date": date, "source": "keybr", "wpm": wpm}


@dactylo.group()
def fastfingers():
    """ fastfingers related commands """


@fastfingers.command()
@argument("wpm", help="words per minute")
@option("--date", help="date of the record", default=datetime.datetime.today())
def add(wpm, date):
    """ add a record for fastfingers """
    with open_df_from_file(DACTYLO_FILEPATH) as df:
        df.loc[df.shape[0] + 1] = {"date": date, "source": "fastfingers", "wpm": wpm}
