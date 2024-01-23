def wrrgme(rg):
    # Definieert de mogelijke regimetypen
    strmnd = 42
    crtsch = 56
    schtnd = 13

    if rg == strmnd:
        return 'STROMEND'
    elif rg == crtsch:
        return 'CRITISCH'
    elif rg == schtnd:
        return 'SCHIETEND'
    else:
        # Niet gedefinieerd
        return 'ONBEKEND'

# Voorbeeld vraag:
if __name__ == "__main__":
    rg_val = 42
    result = wrrgme(rg_val)
    print(result)
