#!/bin/bash

if [[ -z "$JAVA_HOME" ]]; then
  export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.265.b01-1.fc32.x86_64
fi

if [[ -z "$1" ]]; then
  echo "usage $0 APPS_DIR"
  exit 1;
else
  APPS_DIR=$1
fi


export ANDROID_SDK_HOME=`realpath android-platforms`

if [[ ! -d "android-platforms" ]]; then
  git clone https://github.com/Sable/android-platforms.git
fi
if [[ ! -d "cryptoguard" ]]; then
  git clone https://github.com/CryptoGuardOSS/cryptoguard.git
fi

pushd cryptoguard > /dev/null
gradle build
popd > /dev/null


mkdir -p log/cryptoguard
LOG_DIR=`realpath log/cryptoguard`
if [[ -n "$CLEAN" ]]; then
  rm -rf $LOG_DIR/*
fi

for app in `find -L $APPS_DIR -name "*.apk" | grep -v '/config'`;
do
  app=`realpath $app`
  LOG_FILE="$LOG_DIR/$(echo $app | rev | cut -d '/' -f 2 | rev).log";
  echo "date # $(date)" > $LOG_FILE

  pushd cryptoguard > /dev/null
  cmd="java -Xmx8g -jar main/build/libs/main.jar 'apk' '$app' '' 1"
  echo $cmd >> $LOG_FILE 2>&1;
  echo $cmd;
  eval $cmd >> $LOG_FILE 2>&1;
  popd > /dev/null;

  echo "date # $(date)" >> $LOG_FILE
done;

