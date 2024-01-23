# Done
def froude(id, h, q, dn_des, prof_des):
    """
    Berekent Froudegetal bij doorsnede ID, waterstand H en debiet Q

    Resultaat:
        float: Froude getal.
    """
    g = 9.81  # Zwaartekracht

    #     id     : actuele doorsnede
    #     h      : niveau waterspiegel
    #     q      : debiet
    #     b      : breedte tpv wateroppervlak
    #     a      : natte doorsnede
    #     brwopp : breedte tpv wateroppervlak
    #     opperv : natte doorsnede

    from OPPERV import opperv
    from BRWOPP import brwopp

    opperv = opperv(id, h, dn_des, prof_des)  # You need to define the compute_opperv function
    brwopp = brwopp(id, h, dn_des, prof_des)  # You need to define the compute_brwopp function

    b = brwopp

    if b < 0.001:
        froude = 1.0E10
    else:
        a = opperv
        froude = q / a * (b / (g * a)) ** 0.5

    return froude
