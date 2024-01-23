
#DONE
def energh(id, hw, debiet, dn_des, prof_des):
    """
    Berekent energiehoogte ENERGH tov. referentieniveau
    voor doorsnede ID, waterstand HW en debiet DEBIET

    Resultaat:
        float: Energy hoogte relatief aan referentie.
    """
    from OPPERV import opperv
    g = 9.81  # zwaartekracht


    #     a  : natte doorsnede
    #     opperv : natte doorsnede
    #     id : actuele doorsnede
    #     hw : niveau waterspiegel
    #     debiet : debiet
    #     snelhd : stroomsnelheid
    #     snhdsh : snelheidshoogte
    #     energh : energiehoogte tov referentieniveau

    # Bereken nat doorsnede oppervlak
    a = opperv(id, hw, dn_des, prof_des)
    snelhd = debiet / a
    snhdsh = snelhd * snelhd / (2 * g)
    energh = hw + snhdsh

    return energh
