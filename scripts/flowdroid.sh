#!/bin/bash

if [[ -z "$1" ]]; then
  echo "usage $0 APPS_DIR"
  exit 1;
else
  APPS_DIR=$1
fi

if [[ -n "$CLEAN" ]]; then
  rm -rf log/flowdroid/*;
fi

for app in `find $APPS_DIR -name "*.apk" | grep -v '/config'`;
do
  LOG_FILE="log/flowdroid/$(echo $app | cut -f 2 -d '/').log";
  date > $LOG_FILE
  cmd="java -jar FlowDroid/soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar \
    -ns \
    -ne \
    -a $app \
    -p /usr/lib/android-sdk/platforms/ \
    -s FlowDroid/soot-infoflow-android/SourcesAndSinks.txt"
  echo $cmd >> $LOG_FILE 2>&1;
  echo $cmd;
  eval $cmd >> $LOG_FILE 2>&1;
  date >> $LOG_FILE
  echo "sleeping 60 sec..."
  sleep 60;
done;
