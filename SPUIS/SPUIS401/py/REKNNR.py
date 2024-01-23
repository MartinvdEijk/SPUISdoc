def reknnr(id, ws, debiet, bm, dn_des, prof_des):
    # Neerwaarts rekenen van benedenwaterstand
    from BCKWTR import bckwtr

    ar = dn_des['ar']
    if ar[id - 1] == 0:
        if bm == 0:
            return bckwtr(id, ws, debiet, 5, bm, dn_des, prof_des)
        elif bm == 1:
            return bckwtr(id, ws, debiet, 7, bm, dn_des, prof_des)
    else:
        print(' onbekende ar (routine REKNNR) !')
        exit()
