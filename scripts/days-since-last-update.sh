#!/bin/bash

source days_since_last_update/virtual-dslu/bin/activate

if [[ -z "$1" ]]; then
  echo "usage: $0 APPS_DIR"
  exit 1;
else
  APPS_DIR=$1
fi

for app in `ls $APPS_DIR`;
do
  days=`python days_since_last_update/get.py $app`
  echo "$app,$days"
done;
