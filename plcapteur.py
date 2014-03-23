#!/bin/python
import json
import random
from pprint import pprint


def gen_capteurs(config):
    capteurs = []
    for i in range(config["nb_capteur"]):
        capteurs.append(random.sample(range(config["nb_zone"]),
                        config["zone_par_capteur"]))
    for i in range(len(capteurs)):
        capteurs[i] = [random.randint(1, 10), capteurs[i]]
        capteurs[i][1].sort()
    return capteurs


def groupby_zones(capteurs, config):
    zones = dict()
    for i in range(config["nb_zone"]):
        zones[i] = [capteurs.index(capteur) for capteur in capteurs
                    if capteur[1].count(i)]
        test = [0]
        if len(zones[i]):
            test = [capteurs[x][0] for x in zones[i]]
        zones[i] = [max(test), zones[i]]
    return zones


with open('config.json') as data_file:
    config = json.load(data_file)
pprint(config)
capteurs = gen_capteurs(config)
zones = groupby_zones(capteurs, config)
print("Capteurs : " + str(capteurs))
print("Zones : " + str(zones))
