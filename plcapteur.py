#!/bin/python
import json
import random
from pprint import pprint


configurations = []


def gen_zones(config):
    zones = []
    for i in range(config["nb_zone"]):
        zones.append(random.sample(range(config["nb_capteur"]),
                                   random.randint(1,
                                                  config["zone_par_capteur"])))
    for zone in zones:
        zone.sort()
    return zones


def groupby_zones(capteurs, config):
    zones = [[] for i in range(config["nb_zone"])]
    for capteur in capteurs:
        for zone in capteurs[capteur][1]:
            zones[zone].append(capteur)
    return zones


def groupby_capteur(zones, config):
    capteurs = dict()
    for i in range(config["nb_capteur"]):
        capteurs[i] = [j for j in range(0, len(zones))
                       if zones[j].count(i)]
        capteurs[i] = [random.randint(1, 10), capteurs[i]]
    return capteurs


def super_recursion_of_death(zones, capteurs):
    importants_plots = [zone[0] for zone in zones if len(zone) == 1]
    # Remove duplicates
    importants_plots = list(set(importants_plots))
    useless_plots = capteurs.copy()
    for key in importants_plots:
        useless_plots.pop(key, None)


with open('config.json') as data_file:
    config = json.load(data_file)

config["zone_par_capteur"] = min([
    config["zone_par_capteur"],
    config["nb_capteur"]
])

pprint(config)
zones = gen_zones(config)
capteurs = groupby_capteur(zones, config)
print("Capteurs : " + str(capteurs))
print("Zones : " + str(groupby_zones(capteurs, config)))
print("Zones : " + str(zones))

print("==================")
super_recursion_of_death(zones, capteurs)
