#!/bin/python
# -*- coding: utf-8 -*-
import json
import random
from pprint import pprint
from pulp import *

configurations = []


def gen_zones(config):
    """Randomly generate the list of plots supervising each area
    return [[index of plots supervising the area]]
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
    """Generate plots from the area list and randomly generate the life time
    return {life_time, [index of areas supervised]}
    """
    capteurs = groupby_capteur(zones, config)
    for i in range(len(capteurs)):
        capteurs[i] = [random.randint(1, 10), capteurs[i]]
    return capteurs


def groupby_zones(capteurs, config):
    """Sort the plots by area supervised
    return [[index of plots supervising]]
    """
    zones = [[] for i in range(config["nb_zone"])]
    for capteur in capteurs:
        for zone in capteurs[capteur][1]:
            zones[zone].append(capteur)
    return zones


def groupby_capteur(zones, config):
    """Sort the areas by plots supervising
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
    return list of configurations : [[plots index]]
    """
    importants_plots = [zone[0] for zone in zones if len(zone) == 1]
    # Remove duplicates
    importants_plots = list(set(importants_plots))
    if(len(importants_plots) == len(capteurs)):
        # No plot can't be removed if we want to supervise all areas, it is an
        # elementary configuration
        global configurations
        # Add this configuration to the configurations list (and remove
        # duplicates)
        configurations.append(list(capteurs.keys()))
        configurations = remove_duplicates_lol(configurations)
        return
    for key in capteurs:
        # For each "unimportant" plots
        if key not in list(importants_plots):
            # We copy the plots list and remove this "unimportant" plot
            new_list_plots = capteurs.copy()
            new_list_plots.pop(key, None)
            new_list_zone = groupby_zones(new_list_plots, config)
            get_configurations(new_list_zone, new_list_plots, config)


with open('config.json') as data_file:
    config = json.load(data_file)

config["zone_par_capteur"] = min([
    config["zone_par_capteur"],
    config["nb_capteur"]
])

pprint(config)

# Generates areas and plots
zones = gen_zones(config)
capteurs = gen_capteurs(zones, config)
print("Capteurs : " + str(capteurs))
print("Zones : " + str(zones))

print("\n============================\n")

# Exemple de l'énoncé
capteurs = {0: [6, [0, 1]], 1: [3, [1, 2]], 2: [2, [2]], 3: [6, [0, 2]]}
zones = groupby_zones(capteurs, config)

# Generate the elementary configurations
get_configurations(zones, capteurs, config)
print(configurations)

# Creating problem…
prob = LpProblem("max_time", LpMaximize)

#lpvariables for the solver
lpvars = []
for i in configurations:
    lpvars.append( LpVariable("C"+str(i), 0, None ) )

# Print the linear equations
resultList = groupby_capteur(configurations, config)
result = dict()
for i in range(config["nb_capteur"]):
    result[i] = [capteurs[i][0], resultList[i]]
print(result)

for i in range(config["nb_capteur"]):
    # setting constraints
    prob += lpSum([ lpvars[j] for j in result[i][1] ]) <= result[i][0]

# objective
prob += lpSum(lpvars)

# optionnal line to get the problem file
#prob.writeLP("problemfile.lp")
prob.solve(GLPK(msg=0))
print("Status: " + LpStatus[prob.status])

# Display results
for i in lpvars:
    print(i.name +" "+ str(value(i)))

