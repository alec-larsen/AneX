import anefrost

__all__ = ["series_probs", "rev_series_probs", "modal_series_outcome", "series_prob_partial", "series_prob_partial_modal"]

def series_probs(home: int, away: int):
    hw = anefrost.state.hth_table[home][away]
    al = anefrost.state.hth_table[away][home]
    hl = 1 - hw
    aw = 1 - al

    p4 = hw**2*aw**2
    p5 = 2*hw**3*aw*al + 2*hw**2*aw**2*hl
    p6 = hw**3*aw*al**2 + 6*hw**2*aw**2*hl*al + 3*hw*aw**3*hl**2
    p7 = hw*aw**3*hl**3 + 9*hw**2*aw**2*hl**2*al + 9*hw**3*aw*hl*al**2 + hw**4*al**3

    return p4 + p5 + p6 + p7

def rev_series_probs(home: int, away: int):
    hw = anefrost.state.hth_table[home][away]
    al = anefrost.state.hth_table[away][home]
    hl = 1 - hw
    aw = 1 - al

    p4 = hl**2*al**2
    p5 = 2*hl**3*al*aw + 2*hl**2*al**2*hw
    p6 = hl**3*al*aw**2 + 6*hl**2*al**2*hw*aw + 3*hl*al**3*hw**2
    p7 = hl*al**3*hw**3 + 9*hl**2*al**2*hw**2*aw + 9*hl**3*al*hw*aw**2 + hl**4*aw**3

    return p4 + p5 + p6 + p7

def modal_series_outcome(home: int, away: int):
    hw = anefrost.state.hth_table[home][away]
    al = anefrost.state.hth_table[away][home]
    hl = 1 - hw
    aw = 1 - al
    
    p4 = hw**2*aw**2
    p5 = 2*hw**3*aw*al + 2*hw**2*aw**2*hl
    p6 = hw**3*aw*al**2 + 6*hw**2*aw**2*hl*al + 3*hw*aw**3*hl**2
    p7 = hw*aw**3*hl**3 + 9*hw**2*aw**2*hl**2*al + 9*hw**3*aw*hl*al**2 + hw**4*al**3
    
    a4 = hl**2*al**2
    a5 = 2*hl**3*al*aw + 2*hl**2*al**2*hw
    a6 = hl**3*al*aw**2 + 6*hl**2*al**2*hw*aw + 3*hl*al**3*hw**2
    a7 = hl*al**3*hw**3 + 9*hl**2*al**2*hw**2*aw + 9*hl**3*al*hw*aw**2 + hl**4*aw**3

    outcomes = {
        "Home in 4": p4,
        "Home in 5": p5,
        "Home in 6": p6,
        "Home in 7": p7,
        "Away in 4": a4,
        "Away in 5": a5,
        "Away in 6": a6,
        "Away in 7": a7
    }
    
    return max(outcomes.keys(), key= lambda k: outcomes[k])

def series_prob_partial(home: int, away: int, w: int = 0, l: int = 0, p: float = 0, p_frac: float = 1):
    hw = anefrost.state.hth_table[home][away]
    al = anefrost.state.hth_table[away][home]
    hl = 1 - hw
    aw = 1 - al

    #Total games played in the series so far
    g = w + l

    #Recursively run series calculations when next game is win or loss.
    for i in [0,1]:
        #Adjust wins/losses (internal to loop, keeping external values unchanged)
        wi = w + i
        li = l + (1-i)
        
        #If the next game is a home game:
        if g+1 in [1,2,5,7]:
            p_fraci = p_frac*(hw*i+hl*(1-i))

        #If the next game is an away game:
        else:
            p_fraci = p_frac*(aw*i+al*(1-i))

        #Add current fractional probability to total probability if home-ice team won series.  
        if wi == 4:
            p += p_fraci

        #If series is not over, move to next game.
        elif li != 4:
            p = series_prob_partial(home, away, wi, li, p, p_fraci)

    return p

def series_prob_partial_modal(home: int, away: int, w: int = 0, l: int = 0, p: list[float] = [0,0,0,0,0,0,0,0], p_frac: float = 1):
    hw = anefrost.state.hth_table[home][away]
    al = anefrost.state.hth_table[away][home]
    hl = 1 - hw
    aw = 1 - al

    #Total games played in the series so far
    g = w + l

    #Recursively run series calculations when next game is win or loss.
    for i in [0,1]:
        #Adjust wins/losses (internal to loop, keeping external values unchanged)
        wi = w + i
        li = l + (1-i)
        
        #If the next game is a home game:
        if g+1 in [1,2,5,7]:
            p_fraci = p_frac*(hw*i+hl*(1-i))

        #If the next game is an away game:
        else:
            p_fraci = p_frac*(aw*i+al*(1-i))

        #Add current fractional probability to total probability if home-ice team won series.  
        if wi == 4:
            p[li] += p_fraci

        #If series is not over, move to next game.
        elif li == 4:
            p[4+wi] += p_fraci

        else:
            p = series_prob_partial_modal(home, away, wi, li, p, p_fraci)

    return p