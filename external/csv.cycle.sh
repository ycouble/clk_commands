#!/bin/bash
 
usage () {
    cat<<EOF
$0

Cycle through all files in the current directory and show a columnified version of it.
EOF
}
if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
	usage
	exit 0
fi

for file in $(ls *.csv); do clk csv columnify@sh $file; done
