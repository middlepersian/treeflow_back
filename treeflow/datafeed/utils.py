
import unicodedata

def normalize_nfc(input_string):
    input_string = input_string.strip()
    return unicodedata.normalize('NFC', input_string)