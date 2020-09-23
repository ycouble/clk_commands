#!/bin/bash -x

usage () {
    cat<<EOF
$0

Edit the sql script to instantiate a new db entry to emulate a dataset upload
EOF
}

if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
  usage
  exit 0
fi

rssDir="${HOME}/dev/rss_alstom_rss"

vi ${rssDir}/Data/INSERT_DONE_BY_CAF.sql
psql -d sure -a -f ${rssDir}/Data/INSERT_DONE_BY_CAF.sql
psql -d sure -c "SELECT max(iddb) as YourSimulationID from csm_simulation;"
# TODO LIST:
# - copy to a tmp file, sed inside and use arg
