import numpy as np

#DONE
def hydstr(id, hw, dn_des, prof_des):
    #     Berekent hydraulische straal
    #     voor doorsnede ID en niveau waterspiegel HW
    # Functies
    from OPPERV import opperv

    zb, pn = dn_des['zb'], dn_des['pn']
    ny, dp, bp, op = prof_des['ny'], prof_des['dp'], prof_des['bp'], prof_des['op']

    # Actueel profielnummer
    jd = int(pn[id - 1])

    # Actuele waterdiepte
    dw = hw - zb[id - 1]

    # Actueel aantal steunpunten
    jy = 0
    for iy in range(1, ny[jd - 1] + 1):
        if dp[iy - 1, jd - 1] <= dw:
            jy = iy

    # Natte omtrek uit tabel
    if op[jy - 1, jd - 1] == 0:
        # Natte omtrek berekenen
        somper = 0.0
        plafnd = False
        for iy in range(1, jy):
            if iy == 1:
                x = bp[iy - 1, jd - 1]
                y = dp[iy - 1, jd - 1]
            elif not plafnd:
                if bp[iy - 1, jd - 1] == 0:
                    plafnd = True
                x = bp[iy - 1, jd - 1] - bp[iy - 2, jd - 1]
                y = dp[iy - 1, jd - 1] - dp[iy - 2, jd - 1]
            somper += np.sqrt(x * x + y * y)

        if jy == ny[jd - 1]:
            x = 0.0
            y = dw - dp[jy - 1, jd - 1]
        else:
            if dp[jy, jd - 1] > dp[jy - 1, jd - 1]:
                brwspl = bp[jy - 1, jd - 1] + (dw - dp[jy - 1, jd - 1]) / (dp[jy, jd - 1] - dp[jy - 1, jd - 1]) \
                         * (bp[jy, jd - 1] - bp[jy - 1, jd - 1])
            else:
                brwspl = bp[jy - 1, jd - 1]
            x = brwspl - bp[jy - 1, jd - 1]
            y = dw - dp[jy - 1, jd - 1]

        somper += np.sqrt(x * x + y * y)

    elif jy >= ny[jd - 1]:
        somper = op[jy - 1, jd - 1]
    elif dp[jy, jd - 1] > dp[jy - 1, jd - 1]:
        somper = op[jy - 1, jd - 1] + (dw - dp[jy - 1, jd - 1]) / (dp[jy, jd - 1] - dp[jy - 1, jd - 1]) \
                 * (op[jy, jd - 1] - op[jy - 1, jd - 1])
    else:
        somper = op[jy - 1, jd - 1]

    # Hydraulische straal
    return opperv(id, hw, dn_des, prof_des) / somper
