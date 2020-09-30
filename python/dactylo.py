#!/usr/bin/env python3
import datetime
import os.path
import sys
import subprocess
from contextlib import contextmanager

import click
import pandas as pd
from click_project.log import get_logger
from click_project.decorators import command, argument, option, group, flag


LOGGER = get_logger(__name__)

DACTYLO_FILEPATH = os.path.expanduser("~/public_data/dactylo.csv")
DACTYLO_COLS = ["date", "source", "wpm"]


@contextmanager
def open_df_from_file(path: str):
    if os.path.isfile(path):
        df = pd.read_csv(path, parse_dates=True)
    else:
        df = pd.DataFrame({}, columns=DACTYLO_COLS)
    # Sum to support change of # of columns
    old_hash = pd.util.hash_pandas_object(df.transpose()).sum()
    try:
        yield df
    finally:
        # Write to file only if df has changed
        new_hash = pd.util.hash_pandas_object(df.transpose()).sum()
        if not (new_hash == old_hash).all():
            LOGGER.info("Dataframe has change, write to disk")
            df.to_csv(path, index=False)


@group()
def dactylo():
    """ touch typing training related commands """


@dactylo.command()
@argument("source", help="source of the record", type=click.Choice(["fastfingers", "keybr"])) 
@argument("wpm", help="words per minute")
@option("--date", help="date of the record", default=datetime.datetime.today())
def add(source, wpm, date):
    """ add a record (commands group) """
    with open_df_from_file(DACTYLO_FILEPATH) as df:
        df.loc[df.shape[0] + 1] = {"date": date, "source": source, "wpm": wpm}


@dactylo.command()
@flag("--generate-only", help="do not open the plot", default=False)
def plot(generate_only):
    """
    Plot the progress over time and optionally open it with the default 
    image viewer
    """
    def default_open(something_to_open):
        """Open given file with default user program."""
        if sys.platform.startswith('linux'):
            LOGGER.info("Calling xdg-open")
            subprocess.call(['xdg-open', something_to_open])
        elif sys.platform.startswith('darwin'):
            LOGGER.info("Calling open")
            subprocess.call(['open', something_to_open])
        elif sys.platform.startswith('win'):
            LOGGER.info("Calling start")
            subprocess.call(['start', something_to_open], shell=True)
    with open_df_from_file(DACTYLO_FILEPATH) as df:
        data = {}
        for source in df["source"].unique():
            data[source] = df.loc[df["source"] == source, :]
            print(data[source])
        # TODO




@dactylo.command()
def send():
    """ Send dactylo data to server """
    today = datetime.date.today()
    directory = os.path.dirname(DACTYLO_FILEPATH)
    subprocess.call(f"git add -u".split(" "), cwd=directory)
    subprocess.call(
        f"git commit -m".split(" ") + [f"'dactylo stats {today}'"], cwd=directory
    )
    LOGGER.info("git pull")
    subprocess.call(f"git pull --rebase".split(" "), cwd=directory)
    LOGGER.info("git push")
    subprocess.call(f"git push".split(" "), cwd=directory)


@dactylo.command()
def pull():
    """ Pull dactylo data from server """
    directory = os.path.dirname(DACTYLO_FILEPATH)
    LOGGER.info("git pull")
    subprocess.call(f"git pull --rebase".split(" "), cwd=directory)


@dactylo.command()
def init():
    """ Pull dactylo data from server """
    directory = os.path.dirname(os.path.dirname(DACTYLO_FILEPATH))
    LOGGER.info("cloning remote repo for dactylo data")
    subprocess.call(f"git clone git@github.com:ycouble/public_data.git".split(" "), cwd=directory)

# TODO LIST:
# - dactylo undo
# - dactylo ff/kbr start (start browser with url)
