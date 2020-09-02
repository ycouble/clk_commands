#!/bin/bash

pip3 install pipx
pipx install click-project
pipx upgrade click-project
clk customcommands add-external-path $(pwd)/external
clk customcommands add-python-path $(pwd)/python
