#!/usr/bin/env python3
import os
import subprocess
import sys

import click
from click_project.decorators import group, command, argument, option
from click_project.log import get_logger


LOGGER = get_logger(__name__)
CONFIG_PATH = os.path.expanduser("~/.local/share/clk/git.txt")


@group()
@option("--config", help="git tracking file path file path", default=CONFIG_PATH)
@click.pass_context
def git(ctx, config):
    """ Git repositories related commands """
    # Context enrichment
    ctx.ensure_object(dict)
    ctx.obj["config"] = config
    # Ensure the config file and its directory exist
    LOGGER.debug(f"Creating config file {config} if it doesn't exist")
    try:
        os.makedirs(os.path.dirname(config))
    except FileExistsError:
        pass
    if not os.path.isfile(config):
        with open(config, "a+"):
            pass


@git.command()
@argument("path", help="The path to a git repository")
@click.pass_context
def add(ctx, path):
    """ Add a git repository to the command git tracking """
    config = ctx.obj["config"]
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
    with open(config, "r") as paths:
        existing_paths = paths.readlines()
        if path in [p.replace("\n", "") for p in existing_paths]:
            LOGGER.warning(f"Path {path} already in tracked repositories")
            return
    with open(config, "a+") as f:
        LOGGER.info(f"Adding path {path} to the tracked repositories")
        f.write(path + "\r\n")


@git.command(name="list")
@click.pass_context
def list_git_repos(ctx):
    """ List tracked git repositories """
    config = ctx.obj["config"]
    with open(config, "r") as f:
        for path in f.readlines():
            print(path)


@git.command(name="st")
@click.pass_context
def status(ctx):
    """ Get the git status for each tracked git repository """
    config = ctx.obj["config"]
    with open(config, "r") as f:
        for path in [p.replace("\n", "") for p in f.readlines()]:
            LOGGER.info("")
            LOGGER.info(f"==== GIT STATUS for {path} ====")
            subprocess.call(["git", "status", "-s"], cwd=path)


@git.command()
@click.pass_context
def edit(ctx):
    """ Edit the config file manually """
    config = ctx.obj["config"]
    subprocess.call(["vim", config])


# TODO List:
# - give a name to the repos
# - commit and push on a named repo
# - commit with a message on a list of named repos
# - fetch all without rebasing
# - pull a list of named repos
