from colorsys import TWO_THIRD
from enum import Enum

import numpy as np

SEASON = 13
BASE_RP_PER_KILL = 0 if SEASON == 13 else 10
BASE_RP_COST = 15 if SEASON == 13 else 0
BASE_RP_COST_INCREMENT = 3 if SEASON == 13 else 12
BASE_MASTER_RP = 15000
MAX_KILL_RP = 125
PLACEMENTS_DIV = [14,13,10,8,6,5,4,3,2,1]
PLAC_HEADERS = ["14+","13-11","10-9","8-7","6","5","4","3","2","1"]

class ApexRankDiv(Enum):
    IV  = 1
    III = 2
    II  = 3
    I   = 4 
    
class ApexRankTier(Enum):
    ROOKIE   = 1
    BRONZE   = 2
    SILVER   = 3
    GOLD     = 4
    PLATINUM = 5
    DIAMOND  = 6
    MASTER   = 7
    PREDATOR = 8

def set_global_values(season):
    """ Update global variables values """
    global SEASON
    global BASE_RP_COST
    global BASE_RP_COST_INCREMENT
    SEASON = season
    BASE_RP_COST = 15 if SEASON == 13 else 0
    BASE_RP_COST_INCREMENT = 3 if SEASON == 13 else 12