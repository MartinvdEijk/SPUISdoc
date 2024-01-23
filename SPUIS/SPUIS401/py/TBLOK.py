def tblok(ir):
    # Presenteert een string met de tekal blok aanduiding
    # met daarachter de symbolen der resultaatparameters
    tblok = 'A' + format(ir, '03d')
    tblok += ' id   xd       ws       zb     energh  froude  grensd    v     brwopp   regime\n'

    return tblok
