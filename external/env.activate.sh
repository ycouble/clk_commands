#!/bin/bash

usage () {
    cat<<EOF
$0

creates a virtual environement with the given name and creates the ipykernel for this venv
--
A:name:[$(ls ${HOME}/.venvs | sed -E 's/^(.*)$/"\1"/' | tr '\n' ',' | sed 's/,$//')]:The name of the venv
EOF
}
if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
	usage
	exit 0
fi

source ${HOME}/.venvs/"${CLK___NAME}"/bin/activate
