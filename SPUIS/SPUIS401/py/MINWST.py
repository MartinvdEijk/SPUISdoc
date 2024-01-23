import numpy as np
# TODO: CAN BE REDUCED TO ONE FUNCTION (BENWST, BOVWST, MINWSTt, REKNNR, REKNOP)
#done
def minwst(id, ws, debiet, bm, dn_des, prof_des):
    # Benoeming parameters
    # Min. benedenst. waterstand bij critische doorsnede
    from BCKWTR import bckwtr

    ar = dn_des['ar']
    if ar[id - 1] == 0:
        return bckwtr(id, ws, debiet, 1, bm, dn_des, prof_des)
    else:
        print(' onbekende ar (routine MINWST) !')
        exit()

