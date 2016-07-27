import plugins
import random
import re
import os
from titlecase import titlecase


def _initialise(bot):
    plugins.register_handler(_handle_hate)
    plugins.register_handler(_handle_bc)
    plugins.register_handler(_handle_wc)
    plugins.register_admin_command(['load_cards'])


def _handle_hate(bot, event, command):
    if event.text.startswith('.hate'):
        yield from bot.coro_send_message(event.conv, fill_black(random.choice(black)))


def _handle_bc(bot, event, command):
    if event.text.startswith('.bc'):
        yield from bot.coro_send_message(event.conv, fill_black(event.text[4:]))


def _handle_wc(bot, event, command):
    if event.text.startswith('.wc'):
        whites = event.text[4:].split(' # ')

        if len(whites) in (1, 2):
            card = random.choice(black)
            while card.count('_') != len(whites):
                card = random.choice(black)
            yield from bot.coro_send_message(event.conv, fill_black(card, whites))
        else:
            yield from bot.coro_send_message(event.conv, "One or two white cards only, please.")


def fill_black(card, whites=None):
    whiter = iter(whites) if whites else iter([])
    fragments = re.split('(_[CTAS]?)', card)
    for i, fragment in enumerate(fragments):
        if fragment.startswith('_'):
            fragments[i] = transform_white(next(whiter, random.choice(white)), fragment[1:])
    return "".join(fragments)


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


def load_cards(bot, event, *args):
    global white, black
    whitefile = os.path.join(os.path.dirname(__file__), 'cah-white-cards.txt')
    blackfile = os.path.join(os.path.dirname(__file__), 'cah-black-cards.txt')
    with open(whitefile, 'r') as f:
        white = tuple(x for x in f.read().splitlines() if not x.startswith('#'))
    with open(blackfile, 'r') as f:
        black = tuple(x for x in f.read().splitlines() if not x.startswith('#'))


load_cards(None, None)