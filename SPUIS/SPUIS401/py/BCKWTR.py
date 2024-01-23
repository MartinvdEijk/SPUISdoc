import numpy as np
#DONE
def bckwtr(id, ws, debiet, jfn, bm, dn_des, prof_des):
    #     Bevat de afvoerrelaties van een stuk kanaal (backwatercurves)
    # Functies
    from GRENSD import grensd
    from BRNOUL import brnoul
    from ERROR import error
    from ENERGH import energh
    from OPPERV import opperv
    from HYDSTR import hydstr
    from CHEZYC import chezyc
    from FROUDE import froude
    from IMPULS import impuls

    #     voor berekeningsmethode backwatercurves zijn de volgende
    #     berekeningsmogelijkheden

    #     jfn=1: Minimale waterstand bij critische doorsnede
    #     jfn=2: Bovenwaterstand als critische doorsnede
    #     jfn=3: Benedenwaterstand bij critische doorsnede bovenstrooms
    #     jfn=4: Berekent bovenwaterstand (stroomopwaarts rekenen)
    #     jfn=5: Berekent benedenwaterstand (stroomafwaarts rekenen)
    #
    #     voor berekeningsmethode Bernoulli/impulsvergelijkingen zijn
    #     de volgende berekeningsmogelijkheden
    #
    #     jfn=6: Berekent bovenwaterstand (stroomopwaarts rekenen)
    #     jfn=7: Berekent benedenwaterstand (stroomafwaarts rekenen)
    zb, xd = dn_des['zb'], dn_des['xd']

    #     Keuze rekenmethode
    if jfn == 2:
        # JFN=2: Bovenwaterstand als critische doorsnede
        return zb[id-2] + grensd(debiet, id-1, dn_des, prof_des)

    elif jfn == 3:
        # JFN=3: Benedenwaterstand bij critische doorsnede bovenstrooms
        # Critische bovenwaterstand:
        w1 = zb[id-2] + grensd(debiet, id-1, dn_des, prof_des)

        # Bereken benedenwaterstand W2 met Bernoulli (schietend water):
        w2 = brnoul(id-1, id, w1, 0.0, debiet, 3, dn_des, prof_des)
        return w2

    elif jfn == 4 or jfn == 5:
        # JFN=4: Berekent bovenwaterstand (stroomopwaarts rekenen)
        # JFN=5: Berekent benedenwaterstand (stroomafwaarts rekenen)
        # Gebruikte methode is step method in verkorte schrijfwijze
        # ID1: Nieuwe doorsnede
        # ID2: Oude doorsnede
        if jfn == 4:
            id1 = id - 1
            id2 = id
        elif jfn == 5:
            id1 = id
            id2 = id - 1
        else:
            melding = ' verkeerde jfn (routine BCKWTR) !'
            error(melding)
            exit()

        # X- positie van doorsnede
        x1 = xd[id1-1]
        x2 = xd[id2-1]
        # Stapgrootte
        dh = 0.0005
        getOut = 0
        i3 = 0
        while getOut!=1:
            # Initialiseer
            getOut2 = 0
            hx = ws[id2-1]
            h0 = hx
            xx = xd[id2-1]
            x0 = xx
            ex = energh(id2, h0, debiet, dn_des, prof_des)
            ax = opperv(id2, h0, dn_des, prof_des)
            rx = hydstr(id2, h0, dn_des, prof_des)
            cx = chezyc(id2, h0, dn_des, prof_des)
            sx = debiet * debiet / (cx * cx * rx * ax * ax)
            frx = froude(id2, h0, debiet, dn_des, prof_des)

            if x1 != x2:
                i1 = 0
                # Zolang X0 > X1: bereken nieuwe X0
                while getOut2 != 1:
                    h0 = hx
                    s0 = sx
                    e0 = ex
                    x0 = xx
                    fr0 = frx
                    hx = h0 + dh
                    a1 = opperv(id1, hx, dn_des, prof_des)
                    a2 = opperv(id2, hx, dn_des, prof_des)
                    ax = a1 + (x0 - x1) / (x2 - x1) * (a2 - a1)
                    r1 = hydstr(id1, hx, dn_des, prof_des)
                    r2 = hydstr(id2, hx, dn_des, prof_des)
                    rx = r1 + (x0 - x1) / (x2 - x1) * (r2 - r1)
                    c1 = chezyc(id1, hx, dn_des, prof_des)
                    c2 = chezyc(id2, hx, dn_des, prof_des)
                    cx = c1 + (x0 - x1) / (x2 - x1) * (c2 - c1)
                    sx = debiet * debiet / (cx * cx * rx * ax * ax)
                    sf = 0.5 * (s0 + sx)
                    fr1 = froude(id1, hx, debiet, dn_des, prof_des)
                    fr2 = froude(id2, hx, debiet, dn_des, prof_des)
                    frx = fr1 + (x0 - x1) / (x2 - x1) * (fr2 - fr1)
                    fr = 0.5 * (fr0 + frx)

                    if fr < 1.0E8:
                        de = dh * (1. - fr * fr)
                    else:
                        de = dh

                    if sf != 0.:
                        dx = -de / sf
                        xx = x0 + dx
                    else:
                        xx = np.sign(x1 - x2)

                    ex = e0 + de
                    i1 += 1

                    if i1 > 10000:
                        melding = ' geen oplossing bij iteratie i1 (routine BCKWTR) !'
                        error(melding)

                    # Test op einde interval
                    if (x1 - x0) * (xx - x1) <= 0:
                        # Test op in interval
                        if (x1 - x0) * (xx - x2) <= 0:
                            # X gaat de verkeerde kant uit
                            dh = -dh
                            i3 += 1
                            getOut2 = 1
                            if i3 > 10:
                                melding = ' geen oplossing bij iteratie i3 (routine BCKWTR) !'
                                error(melding)
                    else:
                        getOut = 1
                        getOut2 = 1

        #        XX: Eerste waarde van X die kleiner of gelijk is als X1
        #        Interpoleer energiediepte
        if x0 != xx:
           e1 = ex + (x1 - xx) / (x0 - xx) * (e0 - ex)
        else:
           e1 = e0

        # Bereken waterhoogte
        # Initialisatie
        hm = zb[id1-1] + grensd(debiet, id1, dn_des, prof_des)
        dh = 0.01

        if jfn == 5:
            dh = -0.1 * (hm - zb[id1-1])

        h1 = hm
        f1 = energh(id1, h1, debiet, dn_des, prof_des) - e1
        i2 = 0

        # Oplossen waterhoogte
        while abs(dh) > 0.00001:
            h2 = h1 + dh

            if h2 <= zb[id1-1]:
                h2 = zb[id1-1] + 0.1 * abs(dh)
                dh = h2 - h1

            f2 = energh(id1, h2, debiet, dn_des, prof_des) - e1

            if f2 * (f2 - f1) > 0:
                dh = -0.1 * dh

            h1 = h2
            f1 = f2
            i2 += 1

            if i2 > 10000:
                melding = ' geen oplossing bij iteratie i2 (routine BCKWTR) !'
                error(melding)

        if jfn == 4:
            if opperv(id1, h1, dn_des, prof_des) < opperv(id2, ws[id2-1], dn_des, prof_des):
                # Extra energieverlies door vertraging
                h1, h2 = impuls(id1, id2, h1, ws[id2-1], debiet, 1, bm, dn_des, prof_des)
                # e1 = energh(id1, h1, debiet, dn_des, prof_des)
        return h1
    elif jfn == 6:
        # Met stromend water naar boven
        # Berekent bovenwaterst. W1 met Bernoulli (stromend, stroomopwaarts)
        w1 = brnoul(id - 1, id, 0.0, ws[id-1], debiet, 1, dn_des, prof_des)
        # Controleer versnellingsgebied, anders impulsvergelijking
        if opperv(id - 1, w1, dn_des, prof_des) < opperv(id, ws[id-1], dn_des, prof_des):
            # TODO: Overwrites the waterlevel
            w1, w2 = impuls(id - 1, id, w1, ws[id-1], debiet, 1, bm, dn_des, prof_des)

        return w1

    elif jfn == 7:
        # Met schietend water naar beneden
        # Berekent benedenwaterst. W2 met Bernoulli (schietend, stroomafwaarts)
        w2 = brnoul(id - 1, id, ws[id - 2], 0.0, debiet, 3, dn_des, prof_des)
        # Controleer versnellingsgebied, anders impulsvergelijking
        if opperv(id - 1, ws[id - 2], dn_des, prof_des) < opperv(id, w2, dn_des, prof_des):
            # TODO: Overwrites the waterlevel
            w1, w2 = impuls(id - 1, id, ws[id - 2], w2, debiet, 3, bm, dn_des, prof_des)

        return w2

    else:
        # JFN=1: Minimale waterstand bij critische doorsnede
        # Bovenwaterstand als critische doorsnede
        w1 = zb[id - 2] + grensd(debiet, id - 1, dn_des, prof_des)
        # Bereken benedenwaterstand W2 met Bernoulli (stromend)
        w2 = brnoul(id - 1, id, w1, 0.0, debiet, 2, dn_des, prof_des)
        # Of benedenwaterstand W2 eventueel met impulsvergelijking (stromend)
        if opperv(id, w2, dn_des, prof_des) > opperv(id - 1, w1, dn_des, prof_des):
            # TODO: Overwrites the waterlevel
            w1, w2 = impuls(id - 1, id, w1, w2, debiet, 2, bm, dn_des, prof_des)

        r = hydstr(id, w2, dn_des, prof_des)
        a = opperv(id, w2, dn_des, prof_des)
        c = chezyc(id, w2, dn_des, prof_des)
        sf = debiet * debiet / (a * a * c * c * r)

        return w2 - sf * (xd[id-1] - xd[id - 2]) + 0.00001

