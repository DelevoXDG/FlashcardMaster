from sqlalchemy import create_engine, inspect, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, scoped_session
from sqlalchemy import create_engine
import os

Base = declarative_base()

global dbNames


class dbNames:
    # DB_PATH = "sqlite:///app/flashcard_app.db"
    upper_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    DB_PATH = "sqlite:///" + os.path.join(upper_dir, "flashcard_app.db")
    Decks = "Decks"
    Flashcards = "Flashcards"
    Categories = "Categories"
    FlashcardAnswers = "FlashcardAnswers"
    SingleDeck = "Deck"
    SingleFlashcard = "Flashcard"
    SingleCategory = "Category"
    SingleFlashcardAnswer = "FlashcardAnswer"


class Deck(Base):
    __tablename__ = dbNames.Decks
    id = Column(Integer, autoincrement=True, primary_key=True)
    title = Column(String)
    Category_id = Column(Integer, ForeignKey(f"{dbNames.Categories}.id"))

    Flashcards = relationship(
        dbNames.SingleFlashcard,
        back_populates=dbNames.SingleDeck,
        cascade="all, delete-orphan",
    )
    Category = relationship(
        dbNames.SingleCategory,
        back_populates=dbNames.Decks,
    )

    def default_title(self):
        return f"Deck #{self.id}"

    def __repr__(self):
        return f"<Deck(id={self.id}, title='{self.title}')>"


class Flashcard(Base):
    __tablename__ = dbNames.Flashcards
    id = Column(Integer, autoincrement=True, primary_key=True)
    card_type = Column(Integer)
    question = Column(String)
    answer = Column(String)
    difficulty_level = Column(Integer)
    Deck_id = Column(Integer, ForeignKey(f"{dbNames.Decks}.id"))

    Deck = relationship(
        dbNames.SingleDeck,
        back_populates=dbNames.Flashcards,
    )
    # TODO Add relationship to FlashcardAnswer
    FlashcardAnswers = relationship(
        dbNames.SingleFlashcardAnswer,
        back_populates=dbNames.SingleFlashcard,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Flashcard(id={self.id}, card_type={self.card_type}, question='{self.question}', answer='{self.answer}', difficulty_level={self.difficulty_level}, Deck_id={self.Deck_id})>"


class Category(Base):
    __tablename__ = dbNames.Categories
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    Decks = relationship(dbNames.SingleDeck, back_populates=dbNames.SingleCategory)

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class FlashcardAnswer(Base):
    __tablename__ = dbNames.FlashcardAnswers
    id = Column(Integer, autoincrement=True, primary_key=True)
    Flashcard_id = Column(Integer, ForeignKey(f"{dbNames.Flashcards}.id"))
    is_correct = Column(Integer)

    # TODO Add relationship to Flashcard
    Flashcard = relationship(
        dbNames.SingleFlashcard,
        back_populates=dbNames.FlashcardAnswers,
    )

    def __repr__(self):
        return f"<FlashcardAnswer(id={self.id}, Flashcard_id={self.Flashcard_id}, is_correct={self.is_correct})>"


class EngineSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._engine = None
        return cls._instance

    @property
    def engine(self):
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    def _create_engine(self):
        engine = create_engine(dbNames.DB_PATH, pool_size=20, max_overflow=10)
        self._init_db(engine)
        return engine

    def _init_db(self, engine):
        inspector = inspect(engine)
        if not inspector.has_table(dbNames.Decks):
            Base.metadata.create_all(engine)


def get_scoped_session():
    engine = EngineSingleton().engine
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    return Session


class SessionSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._session = None
        return cls._instance

    @property
    def session(self):
        if self._session is None:
            self._session = self._create_session()
        return self._session

    def _create_session(self):
        engine = EngineSingleton().engine
        session_factory = sessionmaker(bind=engine)
        return session_factory()


# def get_session():
#     engine = EngineSingleton().engine
#     session_factory = sessionmaker(bind=engine)
#     Session = session_factory()
#     return Session


def get_universal_session():
    return SessionSingleton().session


global engine
engine = EngineSingleton().engine
