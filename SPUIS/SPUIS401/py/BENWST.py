# Done
# TODO: CAN BE REDUCED TO ONE FUNCTION (BENWST, BOVWST, MINWSTt, REKNNR, REKNOP)
def benwst(id, ws, debiet, bm, dn_des, prof_des):
    """
    Berekend benedenwaterstand bij een critisch doorsnede

    Resultaat:
        float: Benedenstroom waterlevel.
    """
    from BCKWTR import bckwtr
    ar = dn_des['ar']
    if ar[id-1] == 0:
        return bckwtr(id, ws, debiet, 3, bm, dn_des, prof_des)
    else:
        print(' onbekende ar (routine BENWST) !')
        exit()

