# This Python file uses the following encoding: utf-8

import plugins
import random
import re
from titlecase import titlecase


def _initialise(bot):
    plugins.register_handler(_handle_hate)
    plugins.register_handler(_handle_bc)
    plugins.register_handler(_handle_wc)


def _handle_hate(bot, event, command):
    if event.text.startswith('.hate'):
        yield from bot.coro_send_message(event.conv, fill_black(random.choice(black)))


def _handle_bc(bot, event, command):
    if event.text.startswith('.bc'):
        yield from bot.coro_send_message(event.conv, fill_black(event.text[4:]))


def fill_black(card):
    fragments = re.split('(_[CTAS]?)', card)
    for i, fragment in enumerate(fragments):
        if fragment.startswith('_'):
            fragments[i] = transform_white(random.choice(white), fragment[1:])
    return "".join(fragments)


def _handle_wc(bot, event, command):
    if event.text.startswith('.wc'):
        whites = event.text[4:].split(' # ')

        if len(whites) in (1, 2):
            card, modifiers = random.choice(black)
            while len(modifiers) != len(whites):
                card, modifiers = random.choice(black)
            yield from bot.coro_send_message(event.conv, 
                card % tuple(transform_white(x, y) for x, y in zip(whites, modifiers)))
        else:
            yield from bot.coro_send_message(event.conv, "One or two white cards only, please.")


def transform_white(whitecard, modifier):
    if modifier is 'C':    # Capitalizes the first letter
        return whitecard[0].capitalize() + whitecard[1:]
    elif modifier is 'T':  # Capitalizes the First Letter of Each Word
        return titlecase(whitecard)
    elif modifier is 'A':  # CAPITALIZES ALL LETTERS OH MY GOD
        return whitecard.upper()
    elif modifier is 'S':  # lowercaseandspacelesswithoutpunctuation
        return re.sub("\W", "", whitecard).lower()
    else:
        return whitecard


def load_cards():
    global white, black
    with open('cah-white-cards.txt', 'r') as f:
        white = tuple(x for x in f.read().splitlines() if not x.startswith('#'))
    with open('cah-black-cards.txt', 'r') as f:
        black = tuple(x for x in f.read().splitlines() if not x.startswith('#'))

load_cards()