import numpy as np

import res.apex_resources as apexRes
import apex_rp_calculator as apexRpCalc
import common_tools as comTool

PLAC_HEADERS = ["14+","13-11","10-9","8-7","6","5","4","3","2","1"]

dat_dtype = {
    'names' : ('Season', 'Rank', 'Placement', 'Kills/Assists', 'Participation',
               'RP cost', 'Net gained RP'),
    'formats' : ('i', '|U12', 'i', 'i', 'i', 'i', 'i')}

comp_rp_dtype = {
    'names' : ('Rank', 'Placement', 'Kills/Assists', 'Participation',
               'Season 12 RP cost', 'Season 13 RP cost', 
               'Season 12 Net gained RP', 'Season 13 Net gained RP'), 
    'formats' : ('|U12', 'i', 'i', 'i', 'i', 'i', 'i', 'i')}

comp_plc_rp_dtype = {
    'names' : ('Rank', 'Placement S12', 'Placement S13', 'Kills/Assists', 
               'Participation', 'Season 12 RP cost', 'Season 13 RP cost', 
               'Season 12 Net gained RP', 'Season 13 Net gained RP'), 
    'formats' : ('|U12', 'i', 'i', 'i', 'i', 'i', 'i', 'i', 'i')}

def stats(nb_kills, nb_participation, placement, tier, division):
    """ Return dtype array containing raked stats with the given parameters """
    dat_array = np.zeros(1, dat_dtype)
    dat_array['Season'] = apexRes.SEASON
    apexRes.set_global_values(apexRes.SEASON)
    if (tier == apexRes.ApexRankTier.MASTER or 
        tier == apexRes.ApexRankTier.PREDATOR):
        dat_array['Rank'] = tier.name
    else:
        dat_array['Rank'] =  tier.name + " "  + division.name
    dat_array['Placement'] =  placement
    dat_array['Kills/Assists'] =  nb_kills
    dat_array['Participation'] =  nb_participation
    dat_array['RP cost'] = apexRpCalc.gamecost(tier, division)
    dat_array['Net gained RP'] =  apexRpCalc.net_gained_rp(nb_kills, 
                                                            nb_participation, 
                                            placement, tier, division)
    return dat_array

def compare_stats(nb_kills, nb_participation, placement, tier, division):
    """ Return a single array showing stats in S12 and S13 with dat_dtype"""
    res = np.zeros(2, dat_dtype)
    apexRes.set_global_values(13)
    array_s13 = stats(nb_kills, nb_participation, placement, tier, division)
    print ('*' * 89)
    apexRes.set_global_values(12)
    array_s12 = stats(nb_kills, nb_participation, placement, tier, division)
    
    res = np.concatenate((array_s12, array_s13), dtype=dat_dtype)
    comTool.print_table(res)
    
def compare_stats2(nb_kills, nb_participation, placement, tier, division):
    """ Return a single array comparing stats between S12 and S13  with 
    comp_rp_dtype"""
    dat_array = np.zeros(1, comp_rp_dtype)
    if (tier == apexRes.ApexRankTier.MASTER or 
        tier == apexRes.ApexRankTier.PREDATOR):
        dat_array['Rank'] = tier.name
    else:
        dat_array['Rank'] =  tier.name + " "  + division.name
    dat_array['Placement'] =  placement
    dat_array['Kills/Assists'] =  nb_kills
    dat_array['Participation'] =  nb_participation
    apexRes.set_global_values(12)
    dat_array['Season 12 RP cost'] = apexRpCalc.gamecost(tier, division)
    dat_array['Season 12 Net gained RP'] =  apexRpCalc.net_gained_rp(nb_kills, 
                                                            nb_participation, 
                                            placement, tier, division)
    apexRes.set_global_values(13)
    dat_array['Season 13 RP cost'] = apexRpCalc.gamecost(tier, division)
    dat_array['Season 13 Net gained RP'] =  apexRpCalc.net_gained_rp(nb_kills, 
                                                            nb_participation, 
                                            placement, tier, division)
    return dat_array

def comp_check_stats_ranked(nb_kills, nb_participation, placement):
    """ Show a table comparing RP cost and gain at every rank """
    res = np.zeros(1, comp_rp_dtype)
    for tier in apexRes.ApexRankTier:
        for division in apexRes.ApexRankDiv:
            array = compare_stats2(nb_kills, nb_participation, placement, 
                                   tier, division)
            res = np.concatenate((res, array), dtype=comp_rp_dtype)
            if tier.value > apexRes.ApexRankTier.DIAMOND.value:
                break
    res = np.delete(res, 0, 0)
    comTool.print_table(res)

def check_stats_ranked(nb_kills, nb_participation, placement):
    """ Print arrays comparing ranked stats between s12 and s13 for every 
        rank """
    apexRes.set_global_values(apexRes.SEASON)
    for tier in apexRes.ApexRankTier:
        for division in apexRes.ApexRankDiv:
            compare_stats(nb_kills, nb_participation, placement, tier, division)

def check_stats_ranked_kill_range_per_tier(nb_participation, tier, division):
    """ Show rp gain per number of kills and placement with a specific number of 
        participation  for a specific rank"""
    apexRes.set_global_values(apexRes.SEASON)
    res = []
    for nb_kill in range (0,20):
        temp=[str(nb_kill)]
        for placement in apexRes.PLACEMENTS_DIV:
            gained_rp = apexRpCalc.net_gained_rp(nb_kill, nb_participation, 
                                  placement, tier, division)
            temp.append(str(gained_rp)) 
        res.append(temp)
    #return res 
    print(comTool.tabulate(res, headers=PLAC_HEADERS))

def check_stats_ranked_kill_range(nb_participation):
    """ Show rp gain per number of kills and placement with a specific number of 
        participation  for every rank"""
    apexRes.set_global_values(apexRes.SEASON)
    for tier in apexRes.ApexRankTier:
        if tier.value < 7:
            for division in apexRes.ApexRankDiv:
                print ('*' * 70)
                print(tier.name + " " + division.name + " with " + 
                    str(nb_participation) + " participation points.")
                res = check_stats_ranked_kill_range_per_tier(nb_participation, 
                                                            tier, division)
                print(comTool.tabulate(res, headers=PLAC_HEADERS)) 
        else:
            print ('*' * 70)
            print(tier.name + " with " + str(nb_participation)
                    + " participation points.")
            res = check_stats_ranked_kill_range_per_tier(nb_participation, 
                                                        tier, 
                                                        apexRes.ApexRankDiv.IV)
            print(comTool.tabulate(res, headers=PLAC_HEADERS)) 

def check_min_placement_per_tier(nb_kills, nb_participation, tier, division):
    """ Print the minimum placement a specific rank with season corresponding to
        global variable SEASON """
    apexRes.set_global_values(apexRes.SEASON)
    for placement in range (20,0,-1):
                array = stats(nb_kills, nb_participation, placement, tier, 
                              division)
                if array['Net gained RP'][0] >= 0:
                    return array      

def check_min_placement(nb_kills, nb_participation):
    """ Print the minimum placement of every rank with season corresponding to
        global variable SEASON """
    apexRes.set_global_values(apexRes.SEASON)
    res = np.zeros(1, dat_dtype)
    for tier in apexRes.ApexRankTier:
        for division in apexRes.ApexRankDiv:
            array = check_min_placement_per_tier(nb_kills, nb_participation,
                                                 tier, division)
            res = np.concatenate((res, array), dtype=dat_dtype)
    comTool.print_table(res)     
    
def compare_min_placement_per_tier(nb_kills, nb_participation, tier, division):
    """ Return a single array showing the minimum placement to have positive
        RP in S12 and S13 depending on the given parameters """
    dat_array = np.zeros(1, comp_plc_rp_dtype)        
    if (tier == apexRes.ApexRankTier.MASTER or 
        tier == apexRes.ApexRankTier.PREDATOR):
        dat_array['Rank'] = tier.name
    else:
        dat_array['Rank'] =  tier.name + " "  + division.name
    
    dat_array['Kills/Assists'] =  nb_kills
    dat_array['Participation'] =  nb_participation
    apexRes.set_global_values(12)
    for placement12 in range (20,0,-1):
        dat_array['Season 12 Net gained RP'] =  apexRpCalc.net_gained_rp(nb_kills, 
                                                            nb_participation, 
                                            placement12, tier, division)
        if dat_array['Season 12 Net gained RP'][0] >= 0:
            break
    dat_array['Placement S12'] =  placement12
    dat_array['Season 12 RP cost'] = apexRpCalc.gamecost(tier, division)
    
    apexRes.set_global_values(13)
    for placement13 in range (20,0,-1):
        dat_array['Season 13 Net gained RP'] =  apexRpCalc.net_gained_rp(nb_kills, 
                                                            nb_participation, 
                                            placement13, tier, division)
        if dat_array['Season 13 Net gained RP'][0] >= 0:
            break
    dat_array['Placement S13'] =  placement13
    dat_array['Season 13 RP cost'] = apexRpCalc.gamecost(tier, division)
    
    return dat_array
    
def compare_min_placement(nb_kills, nb_participation): 
    """ Return a single array showing the minimum placement to have positive
        RP in S12 and S13 depending on the given parameters """       
    res = np.zeros(1, comp_plc_rp_dtype)
    for tier in apexRes.ApexRankTier:
        for division in apexRes.ApexRankDiv:
            array = compare_min_placement_per_tier(nb_kills, nb_participation,
                                                   tier, division)
            res = np.concatenate((res, array), dtype=comp_plc_rp_dtype)
    comTool.print_table(res)