#!/bin/python
import json
import random
from pprint import pprint


def gen_zones(config):
    zones = []
    for i in range(config["nb_zone"]):
        zones.append(random.sample(range(config["nb_capteur"]),
                                   random.randint(1,
                                                  config["zone_par_capteur"])))
    for zone in zones:
        zone.sort()
    return zones


def groupby_capteur(zones, config):
    capteurs = dict()
    for i in range(config["nb_capteur"]):
        capteurs[i] = [zones.index(zone) for zone in zones
                       if zone.count(i)]
        capteurs[i] = [random.randint(1, 10), capteurs[i]]
    return capteurs


with open('config.json') as data_file:
    config = json.load(data_file)
pprint(config)
zones = gen_zones(config)
capteurs = groupby_capteur(zones, config)
print("Capteurs : " + str(capteurs))
print("Zones : " + str(zones))
