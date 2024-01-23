import numpy as np

def wsprng(id1, id2, w1, w2, debiet, dn_des, prof_des):
    # Watersprongrelatie, alleen voor horizontale bodem!
    from KRACHT import kracht
    from OPPERV import opperv

    rho = 1000.0

    s1 = kracht(id2, w1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, w1, dn_des, prof_des)
    s2 = kracht(id2, w2, dn_des, prof_des) + rho * debiet**2 / opperv(id2, w2, dn_des, prof_des)
    # if np.round(s1, 3) <= np.round(s2, 3):
    if s1 <= s2:
        return True
    else:
        return False

