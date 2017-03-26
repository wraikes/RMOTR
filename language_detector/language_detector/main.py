"""This is the entry point of the program."""

from .languages import LANGUAGES
from functools import reduce

def text_count(text, words):
    return reduce(lambda x, y: x + (y in text.lower().split()), words, 0)

def detect_language(text, languages=LANGUAGES):
    """Returns the detected language of given text."""
    if text_count(text, LANGUAGES[0]['common_words']) > text_count(text, LANGUAGES[1]['common_words']):
        return 'Spanish'
    else:
        return 'German'




