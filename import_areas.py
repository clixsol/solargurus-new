import os
import csv
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings'
application = get_wsgi_application()

from solargurus.models import Area

area_map = {
    'Los Angeles': {
        'img': '/static/img/la.jpeg',
        'zips': 'lazips.txt'
    },
    'San Diego': {
        'img': '/static/img/sd.jpeg',
        'zips': 'sdzips.txt'
    },
    'San Francisco': {
        'img': '/static/img/sf.jpeg',
        'zips': 'sfzips.txt'
    },
    'San Jose': {
        'img': '/static/img/sj.jpeg',
        'zips': 'sjzips.txt'
    },
    'Sacramento': {
        'img': '/static/img/sc.jpeg',
        'zips': 'sczips.txt'
    },
    'Santa Barbara': {
        'img': '/static/img/sb.jpeg',
        'zips': 'sbzips.txt'
    },
    'Oakland': {
        'img': '/static/img/ok.jpeg',
        'zips': 'okzips.txt'
    },
    'Las Vegas': {
        'img': '/static/img/lv.jpeg',
        'zips': 'lvzips.txt'
    },
}

for area in area_map:
    with open(area_map[area]['zips']) as fp:
        zipcodes = [f.strip() for f in fp.readlines()]
        a = Area.objects.create(
            name=area,
            img=area_map[area]['img'],
            zipcodes=zipcodes
        )
        a.save()
