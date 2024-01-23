#!python

#================== Hoofdprogramma SPUIS =========================
#
#     SPUIS, VERSIE 4.01
#
#     Doel: Berekening van de waterstanden en afvoeren in spuisluizen
#     Waterloopkundig Laboratorium Delft
#     Oorspr. auteur: E.A. van Kleef
#
#     Aanpassing en uitbreiding: A. Vrijburcht
#     16 sept. 1994
#
#     Aanpassing en uitbreiding: M. Witteveen
#     02 mrt. 1995
#
#     Vertaald naar Python: M. van der Eijk
#     jan. 2024
#
import os
import numpy as np
import shutil
import sys

def spuis401():
# ===================== DATASTRUCTUUR ================================
    sys.path.insert(2, os.getcwd()+'\\py')
    from py.BOVWST import bovwst
    from py.GETCOD import getcod
    from py.MINWST import minwst
    from py.BENWST import benwst
    from py.WSPRNG import wsprng
    from py.REKNOP import reknop
    from py.TRACE import trace
    from py.ERROR import error
    from py.REKNNR import reknnr
    from py.TBLOK import tblok
    """
    fileDir:        location of input file
    outputName:     name output
    """
    outputName = 'work'
    # VERWIJDER FILES WANNEER AL BESTAAT
    # if os.path.exists(outputName + ".in"):
    #     os.remove(outputName + ".in")
    if os.path.exists(outputName + ".uin"):
        os.remove(outputName + ".uin")
    if os.path.exists(outputName + ".uws"):
        os.remove(outputName + ".uws")
    if os.path.exists(outputName + ".uqh"):
        os.remove(outputName + ".uqh")

    # AFMETINGEN VAN ARRAYS
    mb, mr, md, mp, my = 10, 100, 50, 20, 20

    # DOORSNEDEBESCHRIJVING
    pn = np.zeros(md, dtype=int)
    rg = np.zeros(md, dtype=int)
    ar = np.zeros(md, dtype=int)
    xd = np.zeros(md)
    zb = np.zeros(md)

    # WATERSTAND BESCHRIJVING
    ws = np.zeros(md)
    ww = np.zeros(md)

    # PROFIELBESCHRIJVING
    ny = np.zeros(mp, dtype=int)
    rb = np.zeros(mp)
    dp = np.zeros((my, mp))
    bp = np.zeros((my, mp))
    op = np.zeros((my, mp))

    # --- WAARDEN VAN DE CONSTANTEN
    opwrts = 18
    nrwrts = 74
    undefd = 1.0e10
    strmnd = 42
    crtsch = 56
    schtnd = 13

    # --- FORMAT PRINTS
    format_99001 = 'Berekeningsmethode is backwatercurves\n'
    format_99002 = 'Berekeningsmethode is Bernoulli/impulsvergelijking\n'

    format_99003 = 'Aantal runs    =  %d \n'
    format_99004 = '{:10}   {:5}\n'
    format_990041 = '{:10.3f}   {:5.3f}\n'
    format_99005 = 'Aantal doorsneden = %d \n'
    format_99006 = '    {:10}{:10}{:10}{:10}{:10}\n'
    format_990061 = '{:10d}{:10.3f}{:10.3f}{:10d}{:10d}\n'
    format_99007 = 'Aantal profielen = %d\n'
    format_99008 = '    Profnr = %d   Aantal y-waarden = %d \n'
    format_99009 = '      {:10}{:10}{:5}\n'
    format_99010 = ' {:10.3f}{:10.3f}{:10.3f}\n'
    format_99011 = '      Ruwheid bodem = %0.3f\n'
    format_99013 = '%.2d\n'
    format_99014 = '{:10}{:10}{:10}{:10}{:10}{:10}\n'
    format_99015 = '{:5}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10d}\n'


    # --- MOGELIJKE STROOMREGIMES
    #     De drie mogelijke stroomregimes (stromend, schietend en
    #     critisch) worden door integers gerepresenteerd, de waarden van
    #     de integers zijn niet van belang
    #       STRMND : stromend
    #       CRTSCH : critisch
    #       SCHTND : schietend

    # --- MOGELIJKE REKENRICHTINGEN
    #     Mogelijke rekenrichtingen zijn (stroom)opwaarts en neerwaarts
    #       OPWRTS : opwaarts
    #       NRWRTS : neerwaarts
    #       RCHTNG : lopende richting

    # --- DOORSNEDEN
    #       nx : aantal doorsneden
    #       id : lopende doorsnede
    #       laatst : laatste berekende doorsnede

    # --- PROFIELEN
    #       npp : aantal profielen
    #       ip : lopende variabele voor profiel
    #       iy : lopende variabele voor steunpunt

    # --- RANDVOORWAARDEN
    #       bm     : berekeningsmethode
    #                0 = berekeningmethode backwatercurves
    #                1 = ber. methode Bernoulli/impulsvgl.
    #       nr     : aantal runs
    #       ir     : teller voor runs
    #       wsbe   : benedenwaterstand in run i
    #       qt     : debiet in run i
    #       debiet : debiet in lopende run

    # --- FUNCTIONS
    #       minwst  : Minimale waterstand bij critsiche doorsnede
    #       bovwst  : Bovenwaterstand bij critische doorsnede
    #       benwst  : Benedenewaterstand bij critische doorsnede
    #       wsprng  : Watersprongrelatie voor horizontale bodem !
    #       tblok   : Characterstring met gegevens tekal blok

    # ======================== Invoer ================================
    #
    # --- Open bestanden voor lezen en schrijven
    #       file 2 : *.IN  ---> invoerbestand met randvoorwaarden en
    #                           geometrie van de sluis
    #       file 3 : *.UIN ---> uitvoerbestand waarin :
    #                           echo van de invoerbestanden en resultaten
    #       file 4 : *.UWS ---> uitvoerbestand waarin :
    #                           tabellen (tekalblokken) per Q-H combinatie
    #                           de waterstand, energiehoogte, froude,
    #                           grensdiepte, stroomsnelheid, breedte
    #                           wateroppervlak en stroomregime als functie
    #                           van x
    #       file 5 : *.UQH ---> uitvoerbestand waarin :
    #                           QH-relatie , waterstanden aan beide zijden
    #                           van de sluis, het verval en de critische
    #                           doorsnede
    #       file 6 : betreft het beeldscherm
    #
    # Open files
    file = open(outputName + ".in", "r")
    lines = [n for n in file.readlines() if not n.startswith('**')]
    lines = [x.replace('\n', '') for x in lines]

    # Lees invoergegevens randvoorwaarden
    bm = int(lines[0])
    lines.remove(lines[0])
    nr = int(lines[0])
    lines.remove(lines[0])

    if bm < 0 or bm > 1:
        print('invoerfout: berekeningsmethode foutief')
    if bm == 0:
        print('Berekeningsmethode is backwatercurves')
    elif bm == 1:
        print('Berekeningsmethode is Bernoulli/impulsvergelijking')

    if nr < 1:
        print('invoerfout: aantal runs foutief')
    print('Aantal runs    =  %d' %(nr))
    wsbe = np.zeros(nr)
    qt = np.zeros(nr)

    for ir in range(1, nr + 1):
        wsbe[ir - 1], qt[ir - 1] = list(map(float, lines[0].split()))
        lines.remove(lines[0])

    # print('BenedenWL     Debiet')
    # for ir, (w, q) in enumerate(zip(wsbe, qt), 1):
    #     print(f'{w:.3f}   {q:.3f}')

    # --- Lees gegevens geometrie van de sluis
    #     nx   : aantal doorsneden
    #     xd   : x-waarde doorsnede
    #     zb   : bodemhoogte doorsnede
    #     pn   : profiel nummer
    #     ar   : afvoerrelatie
    #     npp  : aantal profielen
    #     ny   : aantal steunpunten
    #     dp   : hoogte van steunpunt
    #     bp   : breedte tpv. steunpunt
    #     op   : natte omtrek onder steunpunt
    #     rb   : k-waarde

    nx = int(lines[0])
    lines.remove(lines[0])
    if nx < 2:
        print('invoerfout: aantal doorsneden foutief')
    print('Aantal doorsneden = %d' %(nx))

    xd = np.zeros(nx)
    zb = np.zeros(nx)
    pn = np.zeros(nx)
    for id in range(1, nx + 1):
        doorsnede, xafstand, zbodem, profiel = list(map(float, lines[0].split()))
        lines.remove(lines[0])
        if doorsnede != id:
            print('invoerfout: doorsnedenummer foutief')
        if id > 1 and xafstand <= xd[id - 2]:
            print('invoerfout: x-afstanden moeten in oplopende volgorde')
        xd[id - 1] = xafstand
        zb[id - 1] = zbodem
        pn[id - 1] = profiel
    # print('Doorsnede   X-waarde   Bodemhoogte   Profielnummer')
    # for id, (x, z, p) in enumerate(zip(xd, zb, pn), 1):
    #     print(f'{id}   {x:.3f}   {z:.3f}   {p}')

    id = 1
    ar = np.zeros(nx)
    ar[1:nx] = list(map(float, lines[0].split()))
    lines.remove(lines[0])
    # print('Afvoerrelatie:', ar)

    npp = int(lines[0])
    lines.remove(lines[0])
    print('Aantal profielen = %d' %(npp))

    # Doe voor elk profiel
    for ip in range(1, npp + 1):
        profiel, aanty, ruwheid = int(lines[0].split()[0]), int(lines[0].split()[1]), float(lines[0].split()[2])
        lines.remove(lines[0])

        if profiel != ip:
            error(' invoerfout: profielnummer foutief')

        if aanty < 2 or aanty > my:
            error(' invoerfout: aantal steunpunten foutief')

        ny[ip-1] = aanty
        rb[ip-1] = ruwheid

        for iy in range(1, ny[ip-1] + 1):
            dp[iy-1][ip-1], bp[iy-1][ip-1], op[iy-1][ip-1] = list(map(float, lines[0].split()))
            lines.remove(lines[0])

            if bp[iy-1][ip-1] < 0.0:
                error(' invoerfout: bodemhoogte steunpunt foutief')

    # DATA STRUCTUUR
    dn_des = {'pn': pn, 'rg': rg, 'ar': ar, 'xd': xd, 'zb': zb}
    prof_des = {'ny': ny, 'rb': rb, 'dp': dp, 'bp': bp, 'op': op}
    # print('Einde invoer')
    # Sluit invoerbestanden

    # ================== Shrijf data weg  =========================

    # Schrijf initialisatie
    file3 = open(outputName + ".uin", 'a')
    if bm == 1:
        file3.write(format_99002)
    elif bm == 0:
        file3.write(format_99001)
    else:
        print("Input BM niet goed")
        exit()
    file3.write(format_99003 %(nr))
    file3.write(format_99004.format('Benedenws', 'Debiet'))
    for iy in range(0, nr):
        file3.write(format_990041.format(wsbe[iy], qt[iy]))
    file3.write(format_99005 %(nx))
    file3.write(format_99006.format('Drsnnr', 'Xdrsn', 'Bodemh', 'Prfnr', 'Afvrel'))
    for iy in range(0, nx):
        file3.write(format_990061.format(int(iy+1), xd[iy], zb[iy], int(pn[iy]), int(ar[iy])))
    file3.write(format_99007 %(npp))
    for iy in range(0, npp):
        file3.write(format_99008 %(iy+1, ny[iy]))
        file3.write(format_99009.format('Hoogte', 'Breedte', 'Natomtrek'))
        for ix in range(0, ny[iy]):
            file3.write(format_99010.format(dp[ix][iy], bp[ix][iy], op[ix][iy]))
        file3.write(format_99011 %(rb[iy]))

    # Schrijf parameters output
    file5 = open(outputName + ".uqh", 'a')
    file5.write(format_99014.format('code', 'ws(1)', 'ws(nx)', 'verval', 'debiet', 'icrit'))

    # ================== Initialisatie  =========================

    #     Doe voor alle (nr) runs
    for ir in range(1, nr + 1):
        for id in range(1, nx + 1):
            rg[id - 1] = strmnd
            ws[id - 1] = undefd
            ww[id - 1] = undefd

        icrit = 0
        id = nx
        rchtng = opwrts
        debiet = qt[ir - 1]
        ws[nx - 1] = wsbe[ir - 1]

        # ======================== REKENEN =========================
        print(' ')
        print(f' RUN            {ir}  VAN           {nr}')
        while id >= 1:
            # Doorsnede
            print(f' doorsnede {id}')
            # Rekenrichting stroomopwaarts:
            if rchtng == opwrts:
                # Bereken voor drsn. ID waterstand bij grensdiepte:
                # Diepte wanneer krtisiche stroming verwacht kan worden.
                w1 = minwst(id, ws, debiet, bm, dn_des, prof_des)

                # Als voor drsn. ID waterstand hoger dan waterst. bij grensdiepte dan is sprake van stromend water,
                # bereken WS(ID-1) en maak ID=ID-1:
                if ws[id - 1] >= w1:
                    ws[id - 2] = reknop(id, ws, debiet, bm, dn_des, prof_des)
                    id -= 1
                else:
                    print('Critische doorsnede')
                    rg[id - 2] = crtsch
                    icrit = id - 1

                    # Bereken bovenwaterstand WS(ID-1) als critische doorsnede (JFN=2):
                    ws[id - 2] = bovwst(id, ws, debiet, bm, dn_des, prof_des)

                    # Bereken benedenwaterstand W1 bij schietend water:
                    w1 = benwst(id, ws, debiet, bm, dn_des, prof_des)

                    # Controleer of watersprong optreedt:
                    if not wsprng(id, id, w1, ws[id - 1], debiet, dn_des, prof_des):

                        # Als er geen watersprong is, wordt rekenrichting stroomafwaarts (JFN=3) en maak
                        # LAATST=ID-1 en ID=ID+1:
                        print('Geen watersprong')
                        ws[id - 1] = w1
                        rg[id - 1] = schtnd
                        laatst = id - 1
                        rchtng = nrwrts
                        id += 1

                    else:
                        # Als er verdronken watersprong is, dan blijft rekenrichting stroomopwaarts en maak ID=ID-1:
                        print('Verdronken watersprong')
                        id -= 1
            #        Rekenrichting stroomafwaarts:
            elif id > nx:
                # Als laatste doorsnede bereikt wordt, ga dan terug door
                # stroomopwaarts te gaan rekenen en maak ID=LAATST:
                # Schietend water is wanneer watersnelheid hoger is dan voorplantingsnelheid golf.
                print('Schietend water benedenstrooms')
                id = laatst
                rchtng = opwrts
            elif wsprng(id - 1, id, ws[id - 2], ws[id - 1], debiet, dn_des, prof_des):
                # Als watersprong optreedt ga dan terug door
                # stroomopwaarts te gaan rekenen en maak ID=ID:
                # Watersprong is wanneer superkritisch naar subkritsch gaat (overturning)
                print('Watersprong')
                id = laatst
                rchtng = opwrts
            else:
                # Bereken benedenwaterstand WS(ID) met schietend water
                # (JFN=5) en maak ID=ID+1:
                ws[id-1] = reknnr(id, ws, debiet, bm, dn_des, prof_des)
                rg[id-1] = schtnd
                id += 1

            # Tussenresultaten afdrukken
            with open(outputName + ".in", 'a') as file6:
                stri = tblok(ir)
                file6.write(stri)
                trace(file6, ws, rg, nx, debiet, dn_des, prof_des)

        # ===================== Schrijf resultaten========================
        with open(outputName + ".uin", 'a') as file3, open(outputName + ".uws", 'a') as file4, \
                open(outputName + ".uqh", 'a') as file5:
            stri = tblok(ir)
            file3.write(f'RUN            {ir}  VAN           {nr}\n')
            file3.write(stri)
            file4.write(stri)
            file4.write(format_99013 %(nx))
            trace(file3, ws, rg, nx, debiet, dn_des, prof_des)
            trace(file4, ws, rg, nx, debiet, dn_des, prof_des)

            code = getcod(ir)
            file5.write(format_99015.format(code, ws[0], ws[nx - 1], ws[0] - ws[nx - 1], debiet, icrit))

    # Sluit uitvoerbestanden
    file3.close(), file4.close(), file5.close(), file6.close()
    print('Einde berekening')

# Voorbeeld gebruikt:
if __name__ == "__main__":
    spuis401()