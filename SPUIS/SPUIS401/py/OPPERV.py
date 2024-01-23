#     jd : actueel profielnummer
#     pn : profielnummer
#     id : actuele doorsnede
#     dw : waterdiepte
#     hw : niveau waterspiegel
#     zb : bodemniveau
#     dp : hoogte steunpunt boven bodem
#     ny : totaal aantal steunpunten in doorsnede
#     jy : hoogste steunpunt beneden waterspiegel
#     iy : teller steunpunten
#     bp : breedte tpv. steunpunt
#     b  : actuele breedte tpv. wateroppervlak
#     so : sommatievariabele
#     brw : breedte wateroppervlak
#     opperv : natte doorsnede

#Done
def opperv(id, hw, dn_des, prof_des):
    # Berekent natte doorsnede OPPERV
    # voor doorsnede ID bij waterstand HW
    from BRWOPP import brwopp
    zb, pn = dn_des['zb'], dn_des['pn']
    ny, dp, bp = prof_des['ny'], prof_des['dp'], prof_des['bp']

    # Actueel profielnummer
    jd = int(pn[id - 1])

    # Actuele waterdiepte
    dw = hw - zb[id - 1]

    # Actueel aantal steunpunten
    jy = 0
    for iy in range(1, ny[jd - 1] + 1):
        if dp[iy - 1, jd - 1] <= dw:
            jy = iy

    # Natte doorsnede
    so = 0.0
    for iy in range(1, jy):
        so = (dp[iy, jd - 1] - dp[iy - 1, jd - 1]) * 0.5 * (bp[iy, jd - 1] + bp[iy - 1, jd - 1]) + so

    b = brwopp(id, hw, dn_des, prof_des)
    so = so + (dw - dp[jy - 1, jd - 1]) * 0.5 * (b + bp[jy - 1, jd - 1])
    opperv = so

    return opperv

