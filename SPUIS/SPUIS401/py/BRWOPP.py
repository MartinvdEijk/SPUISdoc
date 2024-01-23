#     jd = actueel profielnummer
#     pn = profielnummer
#     id = actuele doorsnede
#     dw = waterdiepte
#     hw = niveau waterspiegel
#     zb = bodemniveau
#     dp = hoogte steunpunt boven bodem
#     ny = totaal aantal steunpunten in doorsnede
#     jy = hoogste steunpunt beneden waterspiegel
#     iy = teller steunpunten
#     bp = breedte tpv. steunpunt
#     brwopp = breedte wateroppervlak

#DONE
def brwopp(id, hw, dn_des, prof_des):
    """
    Bereken de breede van het water opppervlak
    for een gegeven doorsnede ID en water level HW.

    Resultaat:
        float: Breedte water oppervlak.
    """

    zb, pn = dn_des['zb'], dn_des['pn']
    ny, dp, bp = prof_des['ny'], prof_des['dp'], prof_des['bp']

    # Actueel profielnummer
    jd = int(pn[id - 1])

    # Actuele waterdiepte
    dw = hw - zb[id - 1]

    # Actueel aantal steunpunten
    jy = 0
    for iy in range(1, ny[jd-1] + 1):
        if dp[iy - 1][jd - 1] <= dw:
            jy = iy

    # Breedte wateroppervlak
    if jy == ny[jd - 1]:
        brwopp = bp[jy - 1][jd - 1]
    elif dp[jy][jd - 1] > dp[jy - 1][jd - 1]:
        brwopp = bp[jy - 1][jd - 1] + (dw - dp[jy - 1][jd - 1]) / (dp[jy][jd - 1] - dp[jy - 1][jd - 1]) * (
                bp[jy][jd - 1] - bp[jy - 1][jd - 1])
    else:
        brwopp = bp[jy - 1][jd - 1]

    return brwopp

