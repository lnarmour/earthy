#!/bin/bash

export PYTHONPATH=/var/www/app

if [[ ! -d "/apps" ]]; then
  echo "error: there is no /apps dir"
  exit 1;
fi

if [[ -z "$(find /apps/ -name '*.apk')" ]]; then
  echo "error, no apk files in /apps/"
  exit 1;
fi

for apk in `find /apps/ -name "*.apk"`; 
do 
  APK_FILE=$apk python /var/www/app/analyze_single.py;
done;

