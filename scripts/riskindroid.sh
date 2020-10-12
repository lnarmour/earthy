#!/bin/bash

# this assumes that a container based on the dockerfile at this commit from RiskInDroid exists
#
# docker build --tag riskindroid .

# the container assumes a host directory of apk files is mounted in the container on the /apps directory


if [[ -z "$(docker images | grep '^riskindroid')" ]]; then
  docker_build_dir=`realpath $0 | sed 's~\(.*\)/[^/]*~\1/../RiskInDroid/~'`
  docker build --tag riskindroid $docker_build_dir
fi

if [[ -z "$1" ]]; then
  apks_dir=/root/git/earthy/apps
else
  apks_dir=`realpath $1`
fi

docker run --rm -v ${apks_dir}:/apps -ti riskindroid
