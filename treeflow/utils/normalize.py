import unicodedata


def to_nfc(to_normalize: str) -> str:
    return unicodedata.normalize('NFC', to_normalize)
