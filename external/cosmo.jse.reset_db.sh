#!/bin/bash -x

usage () {
    cat<<EOF
$0

Reset the sure database
EOF
}

if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
  usage
  exit 0
fi

rssDir="${HOME}/dev/rss_alstom_rss"

dropdb sure
createdb sure
java -jar ${rssDir}/Generated/Build/JavaSparkEngine/JSEProject/JSEProject-Domain/build/libs/Simulator-Domain-V1.4-executable-jar.jar  --action create --url jdbc:postgresql://localhost:5432/sure --username postgres --password postgres
vi ${rssDir}/Data/INSERT_DONE_BY_CAF.sql
psql -d sure -a -f ${rssDir}/Data/INSERT_DONE_BY_CAF.sql
psql -d sure -a -f ${rssDir}/Data/INSERT_FMU_CAF.sql
