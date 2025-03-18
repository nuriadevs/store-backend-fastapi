import secrets

def unique_string(byte: int = 8) -> str:
    """
    Genera una cadena única y aleatoria de longitud especificada, 
    utilizando el módulo `secrets` para garantizar que sea segura para su uso 
    en contextos como la generación de tokens o claves secretas.
    """
    return secrets.token_urlsafe(byte)