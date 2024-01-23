def getcod(ir: int) -> str:
    """
    Bepaalt de code van een blok met resultaatgegevens

    Parameters:
        ir (int): Run index.

    Resultaat:
        str: Block code.
    """
    block_code = 'A'
    block_code += f"{ir:03d}"

    return block_code
