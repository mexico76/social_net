import sys
import os
script_path = os.path.dirname(__file__)
project_dir = os.path.abspath(os.path.join(script_path, 'SocialNet', '..', 'SocialNet'))
sys.path.insert(0, project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'SocialNet.settings'

import django
django.setup()

import geonamescache
from edit_data.models import Countrie, City



gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
cities = gc.get_cities()
for country in countries:
    country_info = countries.get(country)
    new_country = Countrie.objects.create(iso=country_info.get('iso'), name=country_info.get('name'))
    new_country.save()
for city in cities:
    city_info = cities.get(city)
    new_city = City.objects.create(name=city_info.get('name'), country=Countrie.objects.get(iso=city_info.get('countrycode')))
    new_city.save()
print('The base is ready!')