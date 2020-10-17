#!/bin/bash

if [[ -n "$CLEAN" ]]; then
  # start mysql container if isn't already running
  C=`docker ps -q --filter name=mysql`
  if [[ -n "$C" ]]; then docker stop mysql; fi;
  C=`docker ps -aq --filter name=mysql`
  if [[ -n "$C" ]]; then docker rm mysql; fi;
  docker run -p 0.0.0.0:3306:3306 --name mysql -v /root/git/earthy/iccta/mysql:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password -d mysql;
fi

# configure iccta
if [[ -n "$CLEAN" || "$CONFIGURE" ]]; then
  if [[ ! -f "autoconf_iccta.sh" ]]; then
    wget https://github.com/JordanSamhi/Tools/raw/master/autoconf_iccta.sh
    chmod +x autoconf_iccta.sh
  fi
  ./autoconf_iccta.sh -u root -p password -j /usr/lib/android-sdk/platforms/
fi


# launch iccta
if [[ -n "$CLEAN" || "$LAUNCH" ]]; then
  if [[ ! -f "launch_iccta.sh" ]]; then
    wget https://github.com/JordanSamhi/Tools/raw/master/launch_iccta.sh
    chmod +x launch_iccta.sh
  fi
  ./launch_iccta.sh -p /usr/lib/android-sdk/platforms/android-23/android.jar $@
fi
