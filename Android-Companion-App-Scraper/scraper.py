import play_scraper
import os
import sys
import re

rootdir = sys.argv[1] if len(sys.argv)>1 else ''

apps = {}

for subdir, dirs, files in os.walk(rootdir):
  name = re.sub(r'^{}/'.format(rootdir), '', subdir)
  if not name or name == rootdir:
    continue
  try:
    print('collecting {}'.format(name), file=sys.stderr)
    app = play_scraper.details(name)
    val = app['score']
    apps[name] = val
  except:
    apps[name] = 'None'
    continue

for name in sorted(apps):
  print('{},{}'.format(name, apps[name]))
