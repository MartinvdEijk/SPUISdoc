def error(melding: str) -> None:
    """
    presenteert een errorstring naar de uitvoerbestanden
    en naar het scherm, daarna stopt de executie.

    Parameters:
        melding (str): Error nerocjt.
    """
    with open('work.uin', 'a') as file3, open('work.uws', 'a') as file4, \
            open('work.uqh', 'a') as file5, open('work.in', 'a') as file6:
        file3.write(f"{melding}\n")
        file4.write(f"{melding}\n")
        file5.write(f"{melding}\n")
        file6.write(f"{melding}\n")

    # Stop the execution
    raise SystemExit(melding)
