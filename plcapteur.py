#!/bin/python
import configparser
import json
import random
from pprint import pprint

def gen_capteurs(config):
    capteurs = []
    for i in range(0, config["nb_capteur"]):
        tmp = []
        for j in range(0, config["zone_par_capteur"]):
            tmp.append( random.randint(0, config["nb_zone"]) )
        capteurs.append( tmp )
        print("capteur " + str(i) + " : " + str(capteurs[i]))
    return capteurs

def groupe_capteur()

with open('config.json') as data_file:    
    config = json.load(data_file)
pprint(config)

