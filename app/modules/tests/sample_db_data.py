from .. import (
    get_scoped_session,
    Deck,
    Flashcard,
    Category,
)

import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def print_all_flashcards():
    """Prints all flashcards in the database to the log"""
    session = get_scoped_session()
    flashcards = session.query(Flashcard).all()

    for flashcard in flashcards:
        print(flashcard)
        # log.debug(flashcard)

    session.remove()


def delete_flashcards_with_invalid_difficulty():
    session = get_scoped_session()
    flashcard = session.query(Flashcard).filter_by(difficulty_level="medium").first()
    session.delete(flashcard)
    session.commit()

    session.remove()


def add_sample_decks():
    """Just a function to add sample decks"""
    session = get_scoped_session()
    deck1 = Deck(title="Mathematics")
    deck2 = Deck(title="History")
    deck3 = Deck(title="Science")
    session.add_all([deck1, deck2, deck3])
    session.commit()
    # session.remove()


def add_sample_decks_with_categories():
    category1 = Category(name="Math")
    category2 = Category(name="History")
    category3 = Category(name="Science")
    session = get_scoped_session()
    session.add_all([category1, category2, category3])
    session.commit()
    # Retrieve the created categories
    category1 = session.query(Category).filter_by(name="Math").first()
    category2 = session.query(Category).filter_by(name="History").first()
    category3 = session.query(Category).filter_by(name="Science").first()

    # Create sample decks associated with the categories
    deck1 = Deck(title="Algebra", Category=category1)
    deck2 = Deck(title="World Wars", Category=category2)
    deck3 = Deck(title="Chemistry", Category=category3)

    session.add_all([deck1, deck2, deck3])
    session.commit()
    # session.remove()


def add_sample_flashcards():
    """Just a function to add sample flashcards"""
    session = get_scoped_session()

    # Retrieve the Mathematics deck
    mathematics_deck = session.query(Deck).filter_by(title="Mathematics").first()

    # Create and add sample flashcards for the Mathematics deck
    flashcard1 = Flashcard(
        card_type=1,
        question="What is 2 + 2?",
        answer="4",
        difficulty_level=1,
        Deck=mathematics_deck,
    )
    flashcard2 = Flashcard(
        card_type=1,
        question="What is the square root of 16?",
        answer="4",
        difficulty_level=2,
        Deck=mathematics_deck,
    )
    flashcard3 = Flashcard(
        card_type=1,
        question="What is 5 x 5?",
        answer="25",
        difficulty_level=1,
        Deck=mathematics_deck,
    )

    session.add_all([flashcard1, flashcard2, flashcard3])
    # Retrieve the History deck
    history_deck = session.query(Deck).filter_by(title="History").first()

    # Create and add sample flashcards for the History deck
    flashcard4 = Flashcard(
        card_type=1,
        question="Who was the first President of the United States?",
        answer="George Washington",
        difficulty_level=2,
        Deck=history_deck,
    )
    flashcard5 = Flashcard(
        card_type=1,
        question="In which year did World War II end?",
        answer="1945",
        difficulty_level=0,
        Deck=history_deck,
    )
    flashcard6 = Flashcard(
        card_type=1,
        question="Who painted the Mona Lisa?",
        answer="Leonardo da Vinci",
        difficulty_level=1,
        Deck=history_deck,
    )

    session.add_all([flashcard4, flashcard5, flashcard6])

    session.commit()
    # session.remove()
