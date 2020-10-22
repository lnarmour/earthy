#!/bin/bash


if [[ -z "$1" ]]; then
  echo "usage $0 APPS_DIR"
  exit 1;
else
  APPS_DIR=$1
fi


export ANDROID_SDK_HOME=`realpath android-platforms`
export DROIDSAFE_SRC_HOME="$(realpath .)/droidsafe-src"
export DROIDSAFE_MEMORY=32

if [[ ! -d "android-platforms" ]]; then
  git clone https://github.com/Sable/android-platforms.git
fi
if [[ ! -d "droidsafe-src" ]]; then
  git clone https://github.com/MIT-PAC/droidsafe-src.git
fi

pushd droidsafe-src > /dev/null
ant compile
popd > /dev/null


mkdir -p log/droidsafe;
if [[ -n "$CLEAN" ]]; then
  rm -rf log/droidsafe/*;
fi

rm -rf tmp
mkdir -p tmp
pushd tmp > /dev/null

for app in `find $APPS_DIR -name "*.apk" | grep -v '/config'`;
do
  LOG_DIR="../log/droidsafe/$(echo $app | rev | cut -d '/' -f 2 | rev)";
  mkdir -p $LOG_DIR
  echo "date # started at $(date)" > $LOG_DIR/timer.txt
  apk_name=`echo $app | sed 's~.*/\(.*\).apk$~\1~'`
  ln -s $app ${apk_name}.apk
  make -f $DROIDSAFE_SRC_HOME/android-apps/Makefile_apk NAME=$apk_name specdump-apk

  if [[ -d "droidsafe-gen" ]]; then
    mv droidsafe-gen $LOG_DIR/
  else
    echo "failed" > $LOG_DIR/failed.txt
  fi

  echo "date # finished at $(date)" >> $LOG_DIR/timer.txt
  rm -rf *
done;




popd > /dev/null
