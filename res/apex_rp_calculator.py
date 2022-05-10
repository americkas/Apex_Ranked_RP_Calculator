import res.apex_resources as apexRes
from errno import EINVAL

def bonuskillrp(nb_kills, placement):
    """ Return the bonus rp given by a number of kills at 
        a defined placement """
    if apexRes.SEASON == 13:
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
        if placement >= 11:
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
    """ Return the total rp gained from kills at a given placement """
    return nb_kills * apexRes.BASE_RP_PER_KILL + bonuskillrp(nb_kills, placement)
    
def total_kill_participation_rp(nb_kills, nb_participation, placement):
    """ Return the total rp gained with kills and participation """
    if apexRes.SEASON == 13:
        return (total_kill_rp(nb_kills, placement) 
                + total_kill_rp(nb_participation, placement) / 2)
    else:
        return total_kill_rp(nb_kills, placement)
    
def placement_rp(placement):
    """ Return the total rp gained from placement alone """
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
    """ Return the raw amount of rp gained in a game """
    if apexRes.SEASON == 13:
        return (placement_rp(placement) +
                total_kill_participation_rp(nb_kills, nb_participation, 
                                            placement))
    else:
        return (placement_rp(placement) +
                min(apexRes.MAX_KILL_RP, total_kill_participation_rp(nb_kills, 
                                                             nb_participation, 
                                                             placement)))

def gamecost(tier, division):
    """ Return the rp cost for a given tier/division """
    if apexRes.SEASON == 13:
        if (tier == apexRes.ApexRankTier.ROOKIE):
            return 0
        else:
            if (tier.value >= apexRes.ApexRankTier.MASTER.value):
                return (apexRes.BASE_RP_COST 
                        + (apexRes.ApexRankTier.MASTER.value - 2) 
                        * apexRes.BASE_RP_COST_INCREMENT * 4)
            else:
                return (apexRes.BASE_RP_COST + (tier.value - 2) 
                        * apexRes.BASE_RP_COST_INCREMENT * 4 
                        + (division.value - 1) * 3)
    else:
        if (tier == apexRes.ApexRankTier.ROOKIE):
            return 0
        else:
            if (tier.value >= apexRes.ApexRankTier.MASTER.value):
                return ((apexRes.ApexRankTier.MASTER.value - 2) 
                        * apexRes.BASE_RP_COST_INCREMENT)
            else:
                return (tier.value - 2) * apexRes.BASE_RP_COST_INCREMENT
        
def net_gained_rp(nb_kills, nb_participation, placement, tier, division):
        return int(total_gained_rp(nb_kills, nb_participation, placement) 
                - gamecost(tier, division))
        
def add_cost_master_game(total_rp):
    return int((total_rp - apexRes.BASE_MASTER_RP) / 1000) * 5
        
def net_gained_rp_master_plus(nb_kills, nb_participation, placement, 
                              tier, division, total_rp):
    if (tier.value >= apexRes.ApexRankTier.MASTER.value):
        return int(net_gained_rp(nb_kills, nb_participation, 
                             placement, tier, division) 
                - add_cost_master_game(total_rp))
    else:
        return net_gained_rp(nb_kills, nb_participation, 
                             placement, tier, division)
