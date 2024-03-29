from .. import (
    get_scoped_session,
    Deck,
    Flashcard,
    Category,
    FlashcardAnswer,
    enums,
)
import sqlalchemy
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


def print_correct_answers():
    """Prints the number of correct answers for each flashcard ID"""
    session = get_scoped_session()

    # Join Flashcard and FlashcardAnswer tables to get the correct answers count
    query = (
        session.query(
            Flashcard.id,
            sqlalchemy.func.count(FlashcardAnswer.id).label("correct_answers"),
        )
        .join(FlashcardAnswer, Flashcard.id == FlashcardAnswer.Flashcard_id)
        .filter(FlashcardAnswer.is_correct == True)
        .group_by(Flashcard.id)
    )

    result = query.all()

    for flashcard_id, correct_answers in result:
        print(f"Flashcard ID: {flashcard_id}, Correct Answers: {correct_answers}")

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
        card_type=enums.CardType.Text,
        question="What is 2 + 2?",
        answer="4",
        difficulty_level=1,
        Deck=mathematics_deck,
    )
    flashcard2 = Flashcard(
        card_type=enums.CardType.Text,
        question="What is the square root of 16?",
        answer="4",
        difficulty_level=2,
        Deck=mathematics_deck,
    )
    flashcard3 = Flashcard(
        card_type=enums.CardType.Text,
        question="What is 5 x 5?",
        answer="25",
        difficulty_level=1,
        Deck=mathematics_deck,
    )


def add_more_sample_flashcards():
    session = get_scoped_session()

    # Retrieve the Mathematics deck
    mathematics_deck = session.query(Deck).filter_by(title="Basic Facts").first()

    # Create and add more sample flashcards for the Mathematics deck
    flashcard4 = Flashcard(
        card_type=enums.CardType.TrueFalse,
        question="Is the Earth round?",
        answer="True",
        difficulty_level=enums.DifficultyLevel.Easy,
        Deck=mathematics_deck,
    )
    flashcard5 = Flashcard(
        card_type=enums.CardType.MultipleChoice,
        question="What is the capital of France?",
        answer='{"Paris": 1, "London": 0, "Berlin": 0, "Rome": 0}',
        difficulty_level=enums.DifficultyLevel.Medium,
        Deck=mathematics_deck,
    )
    flashcard6 = Flashcard(
        card_type=enums.CardType.Text,
        question="Solve the equation: 2x + 5 = 15",
        answer="x = 5",
        difficulty_level=enums.DifficultyLevel.Hard,
        Deck=mathematics_deck,
    )

    session.add_all([flashcard4, flashcard5, flashcard6])

    # Retrieve the History deck
    history_deck = session.query(Deck).filter_by(title="History").first()

    # Create and add more sample flashcards for the History deck
    flashcard7 = Flashcard(
        card_type=enums.CardType.TrueFalse,
        question="Did Christopher Columbus discover America?",
        answer="False",
        difficulty_level=enums.DifficultyLevel.Easy,
        Deck=history_deck,
    )
    flashcard8 = Flashcard(
        card_type=enums.CardType.Text,
        question="When was rome founded?",
        answer="753 BC",
        difficulty_level=enums.DifficultyLevel.Medium,
        Deck=history_deck,
    )
    flashcard9 = Flashcard(
        card_type=enums.CardType.MultipleChoice,
        question="When the US were founded?",
        answer='{"1776": 1, "1779": 0, "1797": 0, "1767": 0}',
        difficulty_level=enums.DifficultyLevel.Hard,
        Deck=history_deck,
    )

    session.add_all([flashcard7, flashcard8, flashcard9])

    session.commit()
    session.close()

    # session.add_all([flashcard1, flashcard2, flashcard3])
    # Retrieve the History deck
    history_deck = session.query(Deck).filter_by(title="History").first()

    # Create and add sample flashcards for the History deck
    flashcard4 = Flashcard(
        card_type=enums.CardType.Text,
        question="Who was the first President of the United States?",
        answer="George Washington",
        difficulty_level=2,
        Deck=history_deck,
    )
    flashcard5 = Flashcard(
        card_type=enums.CardType.Text,
        question="In which year did World War II end?",
        answer="1945",
        difficulty_level=0,
        Deck=history_deck,
    )
    flashcard6 = Flashcard(
        card_type=enums.CardType.Text,
        question="Who painted the Mona Lisa?",
        answer="Leonardo da Vinci",
        difficulty_level=1,
        Deck=history_deck,
    )

    session.add_all([flashcard4, flashcard5, flashcard6])

    session.commit()
    # session.remove()
