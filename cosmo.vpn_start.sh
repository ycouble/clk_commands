#!/bin/bash

usage () {
    cat<<EOF
$0

Connect to Cosmo VPN for user ycouble
EOF
}

if [ $# -gt 0 ] && [ "$1" == "--help" ]
then
  usage
  exit 0
fi

sudo openvpn --config ~/.openvpn/ycouble.ovpn --auth-user-pass ~/.openvpn/.up
