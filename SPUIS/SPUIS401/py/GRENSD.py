#     id : actuele doorsnede
#     zb : bodemniveau
#     debiet : debiet
#     energh : energiehoogte
#     energ1 : 1e energiehoogte
#     energ2 : 2e energiehoogte
#     schatt : schatting
#     grensd : grensdiepte

#DONE
def grensd(debiet, id, dn_des, prof_des):
    # Berekent grensdiepte bij bepaald debiet DEBIET
    # voor doorsnede ID
    from ENERGH import energh

    zb = dn_des['zb']

    schatt = zb[id - 1] + 10.0
    energ2 = energh(id, schatt, debiet, dn_des, prof_des)
    factor = 0.25

    while factor >= 1.0E-5:
        energ1 = 1.0E10

        while energ2 < energ1:
            schatt += factor * (schatt - zb[id - 1])
            energ1 = energ2
            energ2 = energh(id, schatt, debiet, dn_des, prof_des)

        factor *= 0.25

        energ1 = 1.0E10

        while energ2 < energ1:
            schatt -= factor * (schatt - zb[id - 1])
            energ1 = energ2
            energ2 = energh(id, schatt, debiet, dn_des, prof_des)

        factor *= 0.25

    grensd = schatt - zb[id - 1]

    return grensd

# Voorbeeld gebruik:
# Assuming you have the required functions and variables (zb, energh) defined
if __name__ == "__main__":
   debiet_val = 100.0
   id_val = 1
   result = grensd(debiet_val, id_val)
   print(result)
