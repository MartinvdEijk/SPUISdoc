import numpy as np

def brnoul(id1, id2, hw1, hw2, debiet, jfn, dn_des, prof_des):
    #     Brnoul is bedoeld voor versnellende stroom
    #     Lost de stromingssituatie op mbv. Bernoulli-vergelijking
    #     Inclusief wrijvingsverlies

    # Functies
    from GRENSD import grensd
    from OPPERV import opperv
    from CHEZYC import chezyc
    from HYDSTR import hydstr
    from ENERGH import energh

    # id1: Doorsnede 1
    # id2: Doorsnede 2
    # hw1: Bovenstroomse waterstand
    # hw2: Benedenstroomse waterstand
    # debiet: Debiet
    # jfn=1: Berekent HW1 (stromend en stroomopwaarts rekenen)
    # jfn=2: Berekent HW2 (stromend en stroomafwaarts rekenen)
    # jfn=3: Berekent HW2 (schietend en stroomafwaarts rekenen)
    zb, xd = dn_des['zb'], dn_des['xd']

    if jfn == 2 or jfn == 3:
        # Initialisatie
        dh = 0.1
        if jfn == 3:
            dh = -dh
        hm = zb[id2-1] + grensd(debiet, id2, dn_des, prof_des)
        h1 = hm
        dhw = (debiet**2 * (xd[id1-1] - xd[id2-1]) / (opperv(id1, hw1, dn_des, prof_des) + opperv(id2, h1, dn_des, prof_des)) / 2 / (
                (chezyc(id1, hw1, dn_des, prof_des) + chezyc(id2, h1, dn_des, prof_des)) / 2) ** 2 /
               (hydstr(id1, hw1, dn_des, prof_des) + hydstr(id2, h1, dn_des, prof_des)) / 2)
        f1 = energh(id1, hw1, debiet, dn_des, prof_des) - energh(id2, h1, debiet, dn_des, prof_des) + dhw

        # Oplossen
        while abs(dh)>=0.00001:
            h2 = h1 + dh
            if h2 <= zb[id2-1]:
                h2 = h1
            dhw = (debiet**2 * (xd[id1-1] - xd[id2-1]) / (opperv(id1, hw1, dn_des, prof_des) + opperv(id2, h2, dn_des, prof_des)) / 2 / (
                    (chezyc(id1, hw1, dn_des, prof_des) + chezyc(id2, h2, dn_des, prof_des)) / 2) ** 2 /
                   (hydstr(id1, hw1, dn_des, prof_des) + hydstr(id2, h2, dn_des, prof_des)) / 2)
            f2 = energh(id1, hw1, debiet, dn_des, prof_des) - energh(id2, h2, debiet, dn_des, prof_des) + dhw
            if f2 * (f2 - f1) >= 0:
                dh = -0.1 * dh
            if jfn == 3:
                if h2 >= hm:
                    dh = -abs(dh)
            else:
                if h2 <= hm:
                    dh = abs(dh)
            h1 = h2
            f1 = f2
        hw2 = h1
        return hw2
    else:
        # Initialisatie
        dh = 0.1
        hm = zb[id1-1] + grensd(debiet, id1, dn_des, prof_des)
        h1 = hm
        dhw = debiet**2 * (xd[id1-1] - xd[id2-1]) / (opperv(id1, h1, dn_des, prof_des) + opperv(id2, hw2, dn_des, prof_des)) / 2 / (
                (chezyc(id1, h1) + chezyc(id2, hw2)) / 2) ** 2 / (hydstr(id1, h1) + hydstr(id2, hw2)) / 2
        f1 = energh(id1, h1, debiet, dn_des, prof_des) - energh(id2, hw2, debiet, dn_des, prof_des) + dhw

        # Oplossen
        while abs(dh)>=0.00001:
            h2 = h1 + dh
            dhw = debiet**2 * (xd[id1-1] - xd[id2-1]) / (opperv(id1, h2, dn_des, prof_des) + opperv(id2, hw2, dn_des, prof_des)) / 2 / (
                    (chezyc(id1, h2) + chezyc(id2, hw2)) / 2) ** 2 / (hydstr(id1, h2) + hydstr(id2, hw2)) / 2
            f2 = energh(id1, h2, debiet, dn_des, prof_des) - energh(id2, hw2, debiet, dn_des, prof_des) + dhw
            if f2 * (f2 - f1) > 0:
                dh = -0.1 * dh
            if h2 <= hm:
                dh = abs(dh)
            h1 = h2
            f1 = f2
        hw1 = h1
        return hw1
