import sys
import play_scraper as ps
from datetime import datetime

name = sys.argv[1]
if not name:
    sys.exit(1)

app = ps.details(name)
updated = app['updated'] # 'September 22, 2020'


delta = datetime.now().date() - datetime.strptime(updated, '%B %d, %Y').date() 

print(delta.days)
