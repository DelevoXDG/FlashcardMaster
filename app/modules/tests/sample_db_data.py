from .. import (
    get_scoped_session,
    Deck,
)


def add_sample_decks():
    """Just a function to add sample decks"""
    session = get_scoped_session()
    deck1 = Deck(title="Mathematics")
    deck2 = Deck(title="History")
    deck3 = Deck(title="Science")
    session.add_all([deck1, deck2, deck3])
    session.commit()
