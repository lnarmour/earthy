#!/bin/bash

source Android-Companion-App-Scraper/virtual-scraper/bin/activate;

if [[ -z "$1" ]]; then
  apps_dir="$1";
else
  apps_dir="apps";
fi

python Android-Companion-App-Scraper/scraper.py $apps_dir
