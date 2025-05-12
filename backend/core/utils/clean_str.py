# utils.py


def clean_string(value: str, unwanted_chars: str = " \"'\n") -> str:
    """
    Cleans a string by stripping unwanted characters from the beginning and end.

    :param value: The string to clean.
    :param unwanted_chars: A string containing all characters to strip (default: ' "\'\n').
    :return: The cleaned string.
    """
    if not isinstance(value, str):
        raise ValueError("The value to clean must be a string.")

    return value.strip(unwanted_chars)
