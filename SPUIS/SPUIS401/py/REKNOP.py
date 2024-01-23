# Done
def reknop(id, ws, debiet, bm, dn_des, prof_des):
    # Opwaarts rekenen van bovenwaterstand
    from BCKWTR import bckwtr

    ar = dn_des['ar']
    if ar[id - 1] == 0:
        if bm == 0:
            return bckwtr(id, ws, debiet, 4, bm, dn_des, prof_des)
        elif bm == 1:
            return bckwtr(id, ws, debiet, 6, bm, dn_des, prof_des)
    else:
        print(' onbekende ar (routine REKNOP) !')
        exit()
