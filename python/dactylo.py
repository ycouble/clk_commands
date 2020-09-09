#!/usr/bin/env python3
import datetime
import os.path
import sys
import subprocess
from contextlib import contextmanager

import pandas as pd
from click_project.decorators import command, argument, option, group, flag


DACTYLO_FILEPATH = os.path.expanduser("~/public_data/dactylo.csv")
DACTYLO_COLS = ["date", "source", "wpm"]


@contextmanager
def open_df_from_file(path: str):
    if os.path.isfile(path):
        df = pd.read_csv(path, parse_dates=True)
    else:
        df = pd.DataFrame({}, columns=DACTYLO_COLS)
    old_hash = pd.util.hash_pandas_object(df)
    try:
        yield df
    finally:
        # Write to file only if df has changed
        if not (pd.util.hash_pandas_object(df) == old_hash).all():
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

@dactylo.command()
@flag("--generate-only", help="do not open the plot", default=False)
def plot(generate_only):
    """
    Plot the progress over time and optionally open it with the default 
    image viewer
    """
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set()
    def default_open(something_to_open):
        """Open given file with default user program."""
        if sys.platform.startswith('linux'):
            subprocess.call(['xdg-open', something_to_open])
        elif sys.platform.startswith('darwin'):
            subprocess.call(['open', something_to_open])
        elif sys.platform.startswith('win'):
            subprocess.call(['start', something_to_open], shell=True)
    with open_df_from_file(DACTYLO_FILEPATH) as df:
        data = {}
        for source in df["source"].unique():
            data[source] = df.loc[df["source"] == source, :]
            print(data[source])
        // TODO




@dactylo.command()
def send():
    """ Send dactylo data to server """
    today = datetime.date.today()
    directory = os.path.dirname(DACTYLO_FILEPATH)
    subprocess.call(f"git add -u".split(" "), cwd=directory)
    subprocess.call(
        f"git commit -m".split(" ") + [f"'dactylo stats {today}'"], cwd=directory
    )
    subprocess.call(f"git pull --rebase".split(" "), cwd=directory)
    subprocess.call(f"git push".split(" "), cwd=directory)


@dactylo.command()
def pull():
    """ Pull dactylo data from server """
    directory = os.path.dirname(DACTYLO_FILEPATH)
    subprocess.call(f"git pull --rebase".split(" "), cwd=directory)


@dactylo.command()
def init():
    """ Pull dactylo data from server """
    directory = os.path.dirname(os.path.dirname(DACTYLO_FILEPATH))
    subprocess.call(f"git clone git@github.com:ycouble/public_data.git".split(" "), cwd=directory)

# TODO LIST:
# - dactylo undo
