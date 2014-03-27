#!/bin/python2
# -*- coding: utf-8 -*-
import json
import random
from pprint import pprint
from pulp.pulp import *

configurations = []


def gen_zones(config):
    """Randomly generate the list of sensors supervising each area
    return [[index of sensors supervising the area]]
    """
    zones = []
    for i in range(config["nb_zone"]):
        zones.append(random.sample(range(config["nb_capteur"]),
                                   random.randint(1,
                                                  config["zone_par_capteur"])))
    for zone in zones:
        zone.sort()
    return zones


def gen_capteurs(zones, config):
    """Generate sensors from the area list and randomly generate the life time
    return {life_time, [index of areas supervised]}
    """
    capteurs = groupby_capteur(zones, config)
    for i in range(len(capteurs)):
        capteurs[i] = [random.randint(1, 10), capteurs[i]]
    return capteurs


def groupby_zones(capteurs, config):
    """Sort the sensors by area supervised
    return [[index of sensors supervising]]
    """
    zones = [[] for i in range(config["nb_zone"])]
    for capteur in capteurs:
        for zone in capteurs[capteur][1]:
            zones[zone].append(capteur)
    return zones


def groupby_capteur(zones, config):
    """Sort the areas by sensors supervising
    return [[index of areas supervised]]
    """
    capteurs = dict()
    for i in range(config["nb_capteur"]):
        capteurs[i] = [j for j in range(0, len(zones))
                       if zones[j].count(i)]
    return capteurs


def remove_duplicates_lol(list_to_clean):
    """Remove duplicates of a list composed of lists
    return sorted list
    """
    temp_set = set(tuple(x) for x in list_to_clean)
    list_sorted = [list(x) for x in temp_set]
    return list_sorted


def get_configurations(zones, capteurs, config):
    """Generate the elementary configurations
    return list of configurations : [[sensors index]]
    """
    importants_sensors = [zone[0] for zone in zones if len(zone) == 1]
    # Remove duplicates
    importants_sensors = list(set(importants_sensors))
    if(len(importants_sensors) == len(capteurs)):
        # No sensor can't be removed if we want to supervise all areas, it is
        # an elementary configuration
        global configurations
        # Add this configuration to the configurations list (and remove
        # duplicates)
        configurations.append(list(capteurs.keys()))
        configurations = remove_duplicates_lol(configurations)
        return
    for key in capteurs:
        # For each "unimportant" sensors
        if key not in list(importants_sensors):
            # We copy the sensors list and remove this "unimportant" sensor
            new_list_sensors = capteurs.copy()
            new_list_sensors.pop(key, None)
            new_list_zone = groupby_zones(new_list_sensors, config)
            get_configurations(new_list_zone, new_list_sensors, config)


with open('config.json') as data_file:
    config = json.load(data_file)

config["zone_par_capteur"] = min([
    config["zone_par_capteur"],
    config["nb_capteur"]
])

#pprint(config)

if "capteurs" in config:
    capteurs = eval(config["capteurs"])
    zones = groupby_zones(capteurs, config)
else:
    zones = gen_zones(config)
    capteurs = gen_capteurs(zones, config)

print("")
print("Capteurs : " + str(capteurs))
print("Zones : " + str(zones))

print("\n========================================================\n")

# Generate the elementary configurations
get_configurations(zones, capteurs, config)

# Print configurations
for key in range(len(configurations)):
    print("Configuration " + str(key + 1) + ": " + str(configurations[key]))

# Creating problem…
prob = LpProblem("max_time", LpMaximize)

# lpvariables for the solver
lpvars = []
for i in range(len(configurations)):
    lpvars.append(LpVariable("Temps pour la configuration " + str(i + 1),
                             0, None))

# Print the linear equations
resultList = groupby_capteur(configurations, config)
result = dict()
for i in range(config["nb_capteur"]):
    result[i] = [capteurs[i][0], resultList[i]]
# print(result)

for i in range(config["nb_capteur"]):
    # setting constraints
    prob += lpSum([lpvars[j] for j in result[i][1]]) <= result[i][0]

# objective
prob += lpSum(lpvars)

# optionnal line to get the problem file
# prob.writeLP("problemfile.lp")
prob.solve(GLPK(msg=0))

print("\n\n    Résultats de GLPK :\n  =======================\n")
print("Status: " + LpStatus[prob.status])

# Display results
for i in lpvars:
    print(i.name + " " + str(value(i)))
print("")
