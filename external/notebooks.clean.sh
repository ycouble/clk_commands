#!/bin/bash

usage () {
    cat<<EOF
$0

Cleans the outputs of all notebooks in the current folder
EOF
}
if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
	usage
	exit 0
fi

nbtb clean --inplace -o ./*.ipynb
