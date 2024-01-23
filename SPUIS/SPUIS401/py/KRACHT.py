#     jd : actueel profielnummer
#     pn : profielnummer
#     id : actuele doorsnede
#     dp : hoogte steunpunt boven bodem
#     bp : breedte tpv. steunpunt
#     ny : totaal aantal steunpunten in doorsnede
#     jy : hoogste steunpunt beneden waterspiegel
#     iy : teller steunpunten
#     d1: hoogte steunpunt
#     b1: breedte tpv steunpunt
#     dw : waterdiepte
#     somkrt : sommatievariabele kracht
#     brwspl : breedte waterspiegel
#    kracht : hydrostatische kracht

#Done
def kracht(id, hw, dn_des, prof_des):
    # Berekent de hydrostatische kracht
    # voor doorsnede ID bij waterstand HW
    from BRWOPP import brwopp

    zb, pn = dn_des['zb'], dn_des['pn']
    ny, dp, bp = prof_des['ny'], prof_des['dp'], prof_des['bp']

    rho = 1000.0
    g = 9.81

    # Actueel profielnummer
    jd = int(pn[id - 1])

    # Hoogte van en breedte tpv. alle steunpunten
    d1 = [dp[iy - 1, jd - 1] for iy in range(1, ny[jd - 1] + 1)]
    b1 = [bp[iy - 1, jd - 1] for iy in range(1, ny[jd - 1] + 1)]

    # Hoogste steunpunt onder water JY
    dw = hw - zb[id - 1]
    for iy in range(1, ny[jd-1]+1):
        if dw > d1[iy-1]:
            jy = iy

    # Actuele waterdiepte
    dw = hw - zb[id - 1]

    # Hydrostatische kracht
    somkrt = 0.0
    for iy in range(1, jy):
        somkrt += rho*g*(dw-d1[iy])*0.5*(d1[iy]-d1[iy-1])\
                 *(b1[iy]+b1[iy-1]) + rho*g*(d1[iy]-d1[iy-1])\
                 *(d1[iy]-d1[iy-1])*(b1[iy]+2.0*b1[iy-1])/6.0

    brwspl = brwopp(id, hw, dn_des, prof_des)
    somkrt += rho * g * (dw - d1[jy - 1]) * (dw - d1[jy - 1]) * (brwspl + 2 * b1[jy - 1]) / 6.0

    return somkrt
