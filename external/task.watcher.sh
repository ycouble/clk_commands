#!/bin/bash

usage () {
    cat<<EOF
$0

Display the task summary as well as an organized view of the tasks
Can be filtered by project.
--
O:--project:str:The project to display
EOF
}
#O:--project:[$(task _projects | tr '\n' ',' | sed -E 's:([^,]*),:"\1", :g' | sed 's:, $::')]:The project to display

if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
	usage
	exit 0
fi
 

if [ -z "${CLK___PROJECT}" ]
  then
    project=""
  else
    project="project:${CLK___PROJECT}"
fi

show() {
  task summary $project
  task simple $project
}

show
inotifywait -q -r -m -e modify ~/.task/ | \
  while read _path _ _file; do  
    show
  done;
