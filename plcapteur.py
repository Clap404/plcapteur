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


def sort_configurations():
    global configurations
    temp_set = set(tuple(x) for x in configurations)
    configurations = [list(x) for x in temp_set]


def super_recursion_of_death(zones, capteurs, config):
    importants_plots = [zone[0] for zone in zones if len(zone) == 1]
    # Remove duplicates
    importants_plots = list(set(importants_plots))
    #FIXME BEGIN FOR THE DEBUG
    useless_plots = capteurs.copy()
    for key in importants_plots:
        useless_plots.pop(key, None)
    #FIXME END FOR THE DEBUG
    if(len(useless_plots) == 0):
        global configurations
        configurations.append(list(capteurs.keys()))
        sort_configurations()
        return
    for key in useless_plots:
        new_list_plots = capteurs.copy()
        new_list_plots.pop(key, None)
        new_list_zone = groupby_zones(new_list_plots, config)
        super_recursion_of_death(new_list_zone, new_list_plots, config)


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
# Exemple énoncé
#capteurs = {0: [6, [0, 1]], 1: [3, [1, 2]], 2: [2, [2]], 3: [6, [0, 2]]}
#zones = groupby_zones(capteurs, config)
super_recursion_of_death(zones, capteurs, config)
print(configurations)
