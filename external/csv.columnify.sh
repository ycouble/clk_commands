#!/bin/bash

usage () {
    cat<<EOF
$0

Display a csv file with nice columns
--
A:file:str:The file to columnify
EOF
}
if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
	usage
	exit 0
fi

column -s, -t < ${CLK___FILE} | less -#2 -N -S
