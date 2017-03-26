"""This is the entry point of the program."""

from .languages import LANGUAGES


def detect_language(text, languages=LANGUAGES):
    """Returns the detected language of given text."""
    #loop through languages, and count, return largest counted language
    spanish_count = 0
    german_count = 0
    for lang in languages: 
        if lang['name'] == 'Spanish':
            spanish_count = sum([1 for x in lang['common_words'] if x in text.lower().split()])
            print(spanish_count)
        else:
            german_count = sum([1 for x in lang['common_words'] if x in text.lower().split()])
            print(german_count)
    return 'Spanish' if spanish_count > german_count else 'German'

