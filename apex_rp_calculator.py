from colorsys import TWO_THIRD
from enum import Enum
from errno import EINVAL
import numpy as np
from prettytable import PrettyTable
from tabulate import tabulate

SEASON = 13
BASE_RP_PER_KILL = 10
BASE_RP_COST = 15 if SEASON == 13 else 0
BASE_RP_COST_INCREMENT = 3 if SEASON == 13 else 12
BASE_MASTER_RP = 15000
MAX_KILL_RP = 125
PLACEMENTS = [14,13,10,8,6,5,4,3,2,1]
PLAC_HEADERS = ["14+","13-11","10-9","8-7","6","5","4","3","2","1"]

dat_dtype = {
    'names' : ('Season', 'Rank', 'Placement', 'Kills/Assists', 'Participation',
               'RP cost', 'Net gained RP'),
    'formats' : ('i', '|U12', 'i', 'i', 'i', 'i', 'i')}

def set_global_values(season):
    global SEASON
    global BASE_RP_COST
    global BASE_RP_COST_INCREMENT
    SEASON = season
    BASE_RP_COST = 15 if SEASON == 13 else 0
    BASE_RP_COST_INCREMENT = 3 if SEASON == 13 else 12
    

class ApexRankTier(Enum):
    IV  = 1
    III = 2
    II  = 3
    I   = 4 
    
class ApexRankedDivision(Enum):
    ROOKIE   = 1
    BRONZE   = 2
    SILVER   = 3
    GOLD     = 4
    PLATINUM = 5
    DIAMOND  = 6
    MASTER   = 7
    PREDATOR = 8

def bonuskillrp(nb_kills, placement):
    if SEASON == 13:
        if placement < 0 or placement > 20:
            raise EINVAL
        if placement >= 14:
            return nb_kills * 1
        if placement in range(11,14):
            return nb_kills * 5
        if placement in range(9,11):
            return nb_kills * 10
        if placement in range(7,9):
            return nb_kills * 12
        if placement == 6:
            return nb_kills * 14
        if placement == 5:
            return nb_kills * 16
        if placement == 4:
            return nb_kills * 18
        if placement == 3:
            return nb_kills * 20
        if placement == 2:
            return nb_kills * 23
        if placement == 1:
            return nb_kills * 25
    else: # Based on season 12
        if placement < 0 or placement > 20:
            raise EINVAL
        if placement >= 14:
            return nb_kills * 0
        if placement in range(6,11):
            return nb_kills * 1
        if placement in range(4,6):
            return nb_kills * 5
        if placement == 3:
            return nb_kills * 8
        if placement == 2:
            return nb_kills * 11
        if placement == 1:
            return nb_kills * 15
    
def total_kill_rp(nb_kills, placement):
        return nb_kills * BASE_RP_PER_KILL + bonuskillrp(nb_kills, placement)
    
def total_kill_participation_rp(nb_kills, nb_participation, placement):
    if SEASON == 13:
        return (total_kill_rp(nb_kills, placement) 
                + total_kill_rp(nb_participation, placement) / 2)
    else:
        return total_kill_rp(nb_kills, placement)
    
def placement_rp(placement):
    if placement < 0 or placement > 20:
            raise EINVAL
    if placement >= 14:
        return 0
    if placement in range(11,14):
        return 5
    if placement in range(9,11):
        return 10
    if placement in range(7,9):
        return 20
    if placement == 6:
        return 30
    if placement == 5:
        return 45
    if placement == 4:
        return 55
    if placement == 3:
        return 70
    if placement == 2:
        return 95
    if placement == 1:
        return 125

def total_gained_rp(nb_kills, nb_participation, placement):
    if SEASON == 13:
        return (placement_rp(placement) +
                total_kill_participation_rp(nb_kills, nb_participation, 
                                            placement))
    else:
        return (placement_rp(placement) +
                min(MAX_KILL_RP, total_kill_participation_rp(nb_kills, 
                                                             nb_participation, 
                                                             placement)))

def gamecost(division, tier):
    if SEASON == 13:
        if (division == ApexRankedDivision.ROOKIE):
            return 0
        else:
            if (division.value >= ApexRankedDivision.MASTER.value):
                return (BASE_RP_COST + (ApexRankedDivision.MASTER.value - 2) 
                         * BASE_RP_COST_INCREMENT * 4)
            else:
                return (BASE_RP_COST + (division.value - 2) 
                        * BASE_RP_COST_INCREMENT * 4 + (tier.value - 1) * 3)
    else:
        if (division == ApexRankedDivision.ROOKIE):
            return 0
        else:
            if (division.value >= ApexRankedDivision.MASTER.value):
                return ((ApexRankedDivision.MASTER.value - 2) 
                        * BASE_RP_COST_INCREMENT)
            else:
                return (division.value - 2) * BASE_RP_COST_INCREMENT
        
def net_gained_rp(nb_kills, nb_participation, placement, division, tier):
        return int(total_gained_rp(nb_kills, nb_participation, placement) 
                - gamecost(division, tier))
        
def add_cost_master_game(total_rp):
    return int((total_rp - BASE_MASTER_RP) / 1000) * 5
        
def net_gained_rp_master_plus(nb_kills, nb_participation, placement, 
                              division, tier, total_rp):
    if (division.value >= ApexRankedDivision.MASTER.value):
        return int(net_gained_rp(nb_kills, nb_participation, 
                             placement, division, tier) 
                - add_cost_master_game(total_rp))
    else:
        return net_gained_rp(nb_kills, nb_participation, 
                             placement, division, tier)
    
#print(bonuskillrp(1, 1))
#print(total_kill_rp(1, 1))
#print(total_kill_participation_rp(1, 2, 1))
#print(add_cost_master_game (16500))

def print_array (array):
    for i in array:
        for j in i:
            print(j, end=" ")
        print()

def old_stats(nb_kills, nb_participation, placement, division, tier):
    cel_season = ["Season:", SEASON]
    if (division == ApexRankedDivision.MASTER or 
        division == ApexRankedDivision.PREDATOR):
        cel_rank = ["Rank:", division.name]
    else:
        cel_rank = ["Rank:", division.name + " "  + tier.name]
    cel_placement = ["Placement:", placement]
    cel_kills = ["Kills/Assists:", nb_kills]
    cel_participation = ["Participation:", nb_participation]
    cel_cost = ["RP cost:", gamecost(division, tier)]
    cel_gained_rp = ["Net gained RP:", net_gained_rp(nb_kills, nb_participation, 
                                                     placement, division, tier)]
    array = [cel_season, cel_rank, cel_placement, cel_kills, cel_participation, 
             cel_cost, cel_gained_rp]
    cel_season = ["Season:", SEASON]
    if (division == ApexRankedDivision.MASTER or 
        division == ApexRankedDivision.PREDATOR):
        cel_rank = ["Rank:", division.name]
    else:
        cel_rank = ["Rank:", division.name + " "  + tier.name]
    cel_placement = ["Placement:", placement]
    cel_kills = ["Kills/Assists:", nb_kills]
    cel_participation = ["Participation:", nb_participation]
    cel_cost = ["RP cost:", gamecost(division, tier)]
    cel_gained_rp = ["Net gained RP:", net_gained_rp(nb_kills, nb_participation, 
                                                     placement, division, tier)]
    array = [cel_season, cel_rank, cel_placement, cel_kills, cel_participation, 
             cel_cost, cel_gained_rp]
    #print_array(array)
    return array

#stats(nb_kills, nb_participation, placement, division, tier)

def stats(nb_kills, nb_participation, placement, division, tier):
    dat_array = np.zeros(1, dat_dtype)
    dat_array['Season'] = SEASON
    if (division == ApexRankedDivision.MASTER or 
        division == ApexRankedDivision.PREDATOR):
        dat_array['Rank'] = division.name
    else:
        dat_array['Rank'] =  division.name + " "  + tier.name
    dat_array['Placement'] =  placement
    dat_array['Kills/Assists'] =  nb_kills
    dat_array['Participation'] =  nb_participation
    dat_array['RP cost'] =  gamecost(division, tier)
    dat_array['Net gained RP'] =  net_gained_rp(nb_kills, nb_participation, 
                                            placement, division, tier)
    #print_array(array)
    return dat_array

def print_table(dat_array):
    table = PrettyTable(dat_array.dtype.names)
    for row in dat_array:
        table.add_row(row)
    # Change some column alignments; default was 'c'
    print (table)

def compare_stats(nb_kills, nb_participation, placement, division, tier):
    res = np.zeros(2, dat_dtype)
    global SEASON
    set_global_values(13)
    array_s13 = stats(nb_kills, nb_participation, placement, division, tier)
    print ('*' * 89)
    set_global_values(12)
    array_s12 = stats(nb_kills, nb_participation, placement, division, tier)
    
    res = np.concatenate((array_s12, array_s13), dtype=dat_dtype)
    print_table(res)
    
nb_kills = 0
nb_participation = 0
placement = 5
division = ApexRankedDivision.MASTER
tier = ApexRankTier.IV
total_rp = 15000
SEASON = 13

#compare_stats(nb_kills, nb_participation, placement, division, tier)

def check_stats_ranked(nb_kills, nb_participation, placement):
    for division in ApexRankedDivision:
        for tier in ApexRankTier:
            compare_stats(nb_kills, nb_participation, placement, division, tier)
        
#check_stats_ranked(nb_kills, nb_participation, placement)

def check_stats_ranked_kill_range_per_tier(nb_participation, division, tier):
    set_global_values(SEASON)
    res = []
    for nb_kill in range (0,20):
        temp=[str(nb_kill)]
        for placement in PLACEMENTS:
            gained_rp = net_gained_rp(nb_kill, nb_participation, 
                                  placement, division, tier)
            temp.append(str(gained_rp)) 
        res.append(temp)
    return res

def check_stats_ranked_kill_range(nb_participation):
    for division in ApexRankedDivision:
        if division.value < 7:
            for tier in ApexRankTier:
                print ('*' * 70)
                print(division.name + " " + tier.name + " with " + 
                    str(nb_participation) + " participation points.")
                res = check_stats_ranked_kill_range_per_tier(nb_participation, 
                                                            division, tier)
                print(tabulate(res, headers=PLAC_HEADERS)) 
        else:
            print ('*' * 70)
            print(division.name + " with " + str(nb_participation)
                    + " participation points.")
            res = check_stats_ranked_kill_range_per_tier(nb_participation, 
                                                        division, 
                                                        ApexRankTier.IV)
            print(tabulate(res, headers=PLAC_HEADERS)) 

# Merge les colonnes pareilles
check_stats_ranked_kill_range(0)

def check_min_placement_per_tier(nb_kills, nb_participation, division, tier):
    for placement in range (20,0,-1):
                array = stats(nb_kills, nb_participation, placement, division, 
                              tier)
                if array['Net gained RP'][0] >= 0:
                    return array

def check_min_placement(nb_kills, nb_participation):
    res = np.zeros(1, dat_dtype)
    for division in ApexRankedDivision:
        for tier in ApexRankTier:
            array = check_min_placement_per_tier(nb_kills, nb_participation,
                                                 division, tier)
            res = np.concatenate((res, array), dtype=dat_dtype)
    print_table(res)
    
#check_min_placement(nb_kills, nb_participation)
#check_min_placement_per_tier()
#check_min_placement_per_tier(0, 0, ApexRankedDivision.MASTER, ApexRankTier.IV)