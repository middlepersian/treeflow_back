import unicodedata


def normalize( normalization_form: str, value:str) -> str:
    return unicodedata.normalize(normalization_form, value)


def strip_and_normalize(normalization_form:str, value) -> str:
    # strip leading and trailing whitespace
    value = value.strip()
    # normalize the string
    value = normalize(normalization_form, value)
    return value
