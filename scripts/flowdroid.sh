#!/bin/bash

if [[ -z "$1" ]]; then
  echo "usage $0 APPS_DIR ANDROID_SDK"
  exit 1;
else
  APPS_DIR=$1
fi

if [[ -z "$2" ]]; then
  echo "usage $0 APPS_DIR ANDROID_SDK"
  exit 1;
else
  ANDROID_SDK=$2
fi


mkdir -p log/flowdroid;
if [[ -n "$CLEAN" ]]; then
  rm -rf log/flowdroid/*;
fi


# limit each app to 10 min (600 seconds from -dt + -ct + -rt)
#
for app in `find $APPS_DIR -name "*.apk" | grep -v '/config'`;
do
  LOG_FILE="log/flowdroid/$(echo $app | rev | cut -d '/' -f 2 | rev).log";
  echo "date # $(date)" > $LOG_FILE
  cmd="java -jar FlowDroid/soot-infoflow-cmd/target/soot-infoflow-cmd-jar-with-dependencies.jar \
    -ns \
    -ne \
    -dt 200 -ct 200 -rt 200 \
    -a $app \
    -p $ANDROID_SDK/platforms/ \
    -s FlowDroid/soot-infoflow-android/SourcesAndSinks.txt"
  echo $cmd >> $LOG_FILE 2>&1;
  echo $cmd;
  eval $cmd >> $LOG_FILE 2>&1;
  echo "date # $(date)" >> $LOG_FILE
done;
