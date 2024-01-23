import numpy as np

def impuls(id1, id2, hw1, hw2, debiet, jfn, bm, dn_des, prof_des):
    #     IMPULS is bedoeld voor vertragende stroom
    #     Lost de stromingssituatie op dmv. impulsvergelijking
    #
    #     indien er gerekend wordt met backwatercurves, dan
    #     wordt de wrijvingskracht niet meegenomen in de berekening

    # Constants
    rho = 1000.0
    g = 9.81
    zb, xd = dn_des['zb'], dn_des['xd']

    # Functies
    from KRACHT import kracht
    from OPPERV import opperv
    from CHEZYC import chezyc
    from GRENSD import grensd
    from HYDSTR import hydstr
    from ERROR import error
    #     id1 : Doorsnede 1
    #     id2 : Doorsnede 2
    #     hw1 : bovenstroomse waterstand
    #     hw2 : benedenstroomse waterstand
    #     debiet: Debiet
    #     jfn=1: Berekent HW1 (stromend en stroomopwaarts rekenen)
    #     jfn=2: Berekent HW2 (stromend en stroomafwaarts rekenen)
    #     jfn=3: Berekent HW2 (schietend en stroomafwaarts rekenen)
    #     bm   : berekeningsmethode
    #            0 = berekeningmethode backwatercurves
    #            1 = ber. methode Bernoulli/impulsvgl.

    if jfn == 2 or jfn == 3:
        # Berekent benedenstroomse waterstand HW2
        hm = zb[id2-1] + grensd(debiet, id2, dn_des, prof_des)

        if hm > zb[id1-1]:
            h1 = hm
        else:
            h1 = zb[id1-1] + 1.0

        if hw1 > zb[id2-1]:
            hw1 = hw1
        else:
            hw1 = zb[id2-1] + 0.1

        if bm == 0:
            f1 = kracht(id2, hw1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, hw1, dn_des, prof_des) \
                 - kracht(id2, h1, dn_des, prof_des) - rho * debiet**2 / opperv(id2, h1, dn_des, prof_des)
        elif bm == 1:
            f1 = kracht(id2, hw1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, hw1, dn_des, prof_des) \
                 - kracht(id2, h1, dn_des, prof_des) - rho * debiet**2 / opperv(id2, h1, dn_des, prof_des) \
                 + rho * g * debiet**2 * (xd[id1-1] - xd[id2-1]) \
                 / ((opperv(id1, hw1, dn_des, prof_des) + opperv(id2, h1, dn_des, prof_des))
                    / 2 * ((chezyc(id1, hw1, dn_des, prof_des) + chezyc(id2, h1, dn_des, prof_des)) / 2)
                    ** 2 * (hydstr(id1, hw1, dn_des, prof_des) + hydstr(id2, h1, dn_des, prof_des)) / 2)
        else:
            error('Parameter BM niet gedefinieerd')
            exit()

        dh = 0.01
        if jfn == 3:
            dh = -dh
        i1 = 0
        while abs(dh)>=0.00001:
            i1 += 1
            h2 = h1 + dh

            if bm == 0:
                f2 = kracht(id2, hw1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, hw1, dn_des, prof_des) \
                     - kracht(id2, h2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, h2, dn_des, prof_des)
            elif bm == 1:
                f2 = kracht(id2, hw1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, hw1, dn_des, prof_des) \
                     - kracht(id2, h2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, h2, dn_des, prof_des) \
                     + rho * g * debiet**2 * (xd[id1-1] - xd[id2-1]) \
                     / ((opperv(id1, hw1, dn_des, prof_des) + opperv(id2, h2, dn_des, prof_des))
                        / 2 * ((chezyc(id1, hw1, dn_des, prof_des) + chezyc(id2, h2, dn_des, prof_des)) / 2)
                        ** 2 * (hydstr(id1, hw1, dn_des, prof_des) + hydstr(id2, h2, dn_des, prof_des)) / 2)
            else:
                error('Parameter BM niet gedefinieerd')
                exit()

            if f2 * (f2 - f1) > 0:
                dh = -0.1 * dh

            if jfn == 3:
                if h2 >= hm:
                    dh = -abs(dh)
            else:
                if h2 <= hm:
                    dh = abs(dh)

            h1 = h2
            f1 = f2
            if i1 >= 1000:
                melding = 'geen oplossing bij iteratie i1 (routine IMPULS !)'
                error(melding)
                exit()
            hw2 = h1
        return hw1, hw2
    else:
        # Berekent bovenstroomse waterstand HW1, initialisatie
        hm = zb[id1-1] + grensd(debiet, id1, dn_des, prof_des)

        if hm > zb[id2-1]:
            h1 = hm
        else:
            h1 = zb[id2-1] + 0.1
            hm = h1

        if bm == 0:
            f1 = kracht(id2, h1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h1, dn_des, prof_des) \
                 - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des )
        elif bm == 1:
            f1 = kracht(id2, h1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h1, dn_des, prof_des) \
                 - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des) \
                 + rho * g * debiet**2 * (xd[id1-1] - xd[id2-1]) \
                 / ((opperv(id1, h1, dn_des, prof_des) + opperv(id2, hw2, dn_des, prof_des))
                    / 2 * ((chezyc(id1, h1, dn_des, prof_des) + chezyc(id2, hw2, dn_des, prof_des)) / 2)
                    ** 2 * (hydstr(id1, h1, dn_des, prof_des) + hydstr(id2, hw2, dn_des, prof_des)) / 2)
        else:
            error('Parameter BM niet gedefinieerd')
            exit()
        dh = 0.01
        i1 = 0
        while abs(dh)>=0.00001:
            i1 += 1
            h2 = h1 + dh

            if bm == 0:
                f2 = kracht(id2, h2, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h2, dn_des, prof_des) \
                     - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des)
            elif bm == 1:
                f2 = kracht(id2, h2, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h2, dn_des, prof_des) \
                     - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des) \
                     + rho * g * debiet**2 * (xd[id1-1] - xd[id2-1]) \
                     / ((opperv(id1, h2, dn_des, prof_des) + opperv(id2, hw2, dn_des, prof_des))
                        / 2 * ((chezyc(id1, h2, dn_des, prof_des) + chezyc(id2, hw2, dn_des, prof_des)) / 2)
                        ** 2 * (hydstr(id1, h2, dn_des, prof_des) + hydstr(id2, hw2, dn_des, prof_des)) / 2)
            else:
                error('Parameter BM niet gedefinieerd')
                exit()

            if f2 * (f2 - f1) > 0:
                dh = -0.1 * dh

            if h2 <= hm:
                dh = abs(dh)

            h1 = h2
            f1 = f2
            if i1 >= 2500:
                melding = 'geen oplossing bij iteratie i1 (routine IMPULS !)'
                error(melding)
                exit()
            elif abs(dh) < 0.00001:
                hw1 = h1
                if abs(h1 - hm) >= 0.0001:
                    return hw1, hw2

        # Opnieuw met andere initialisatie
        h1 = hw2
        if bm == 0:
            f1 = kracht(id2, h1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h1, dn_des, prof_des) \
                 - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des)
        elif bm == 1:
            f1 = kracht(id2, h1, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h1, dn_des, prof_des) \
                 - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des) \
                 + rho * g * debiet**2 * (xd[id1-1] - xd[id2-1]) \
                 / ((opperv(id1, h1, dn_des, prof_des) + opperv(id2, hw2, dn_des, prof_des))
                    / 2 * ((chezyc(id1, h1, dn_des, prof_des) + chezyc(id2, hw2, dn_des, prof_des)) / 2)
                    ** 2 * (hydstr(id1, h1, dn_des, prof_des) + hydstr(id2, hw2, dn_des, prof_des)) / 2)
        else:
            print('Parameter BM not defined (not equal to 0 or 1)')
            exit()
        dh = 0.01
        i1 = 0
        #        Oplossen impulsvergelijking
        while abs(dh) >= 0.00001:
            i1 += 1
            h2 = h1 - dh

            if bm == 0:
                f2 = kracht(id2, h2, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h2, dn_des, prof_des) \
                     - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des)
            elif bm == 1:
                f2 = kracht(id2, h2, dn_des, prof_des) + rho * debiet**2 / opperv(id1, h2, dn_des, prof_des) \
                     - kracht(id2, hw2, dn_des, prof_des) - rho * debiet**2 / opperv(id2, hw2, dn_des, prof_des) \
                     + rho * g * debiet**2 * (xd[id1-1] - xd[id2-1]) \
                     / ((opperv(id1, h2, dn_des, prof_des) + opperv(id2, hw2, dn_des, prof_des))
                        / 2 * ((chezyc(id1, h2, dn_des, prof_des) + chezyc(id2, hw2, dn_des, prof_des)) / 2)
                        ** 2 * (hydstr(id1, h2, dn_des, prof_des) + hydstr(id2, hw2, dn_des, prof_des)) / 2)
            else:
                print('Parameter BM not defined (not equal to 0 or 1)')
                exit()

            if f2 * (f2 - f1) > 0:
                dh = -0.1 * dh

            if h2 <= hm:
                dh = abs(dh)

            h1 = h2
            f1 = f2
        hw1 = h1
        return hw1, hw2
    return hw1, hw2
