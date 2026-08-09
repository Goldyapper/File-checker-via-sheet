import re

def normaliser(name):
    return re.sub(r'\s+', ' ', name).strip().lower()


def extract_digits(value):
    """Pull the first digits out of a value (e.g. 'S06' -> 6,
    '08' -> 8). Returns None if there's nothing to extract."""
    if value is None:
        return None
    match = re.search(r'\d+', str(value))
    return int(match.group()) if match else None

