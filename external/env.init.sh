#!/bin/bash

usage () {
    cat<<EOF
$0

creates a virtual environement with the given name and creates the ipykernel for this venv
--
A:name:str:The name of the venv
EOF
}
if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
	usage
	exit 0
fi

virtualenv ${HOME}/.venvs/"${CLK___NAME}"
python3 -m ipykernel install --user --name="${CLK___NAME}"
