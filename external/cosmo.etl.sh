#!/bin/bash

usage () {
    cat<<EOF
$0

Start PDI Kettle
EOF
}

if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
  usage
  exit 0
fi

pushd ~/soft/data-integration
{
  bash spoon.sh
}
