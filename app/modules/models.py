from sqlalchemy import create_engine, inspect, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

global dbNames


class dbNames:
    DB_Name = "flashcard_app"
    Decks = "Decks"
    FlashCards = "Flashcards"
    Categories = "Categories"
    FlashcardAnswers = "FlashcardAnswers"


class Deck(Base):
    __tablename__ = dbNames.Decks
    id = Column(Integer, primary_key=True)
    title = Column(String)
    cover_image = Column(String)

    Flashcards = relationship("Flashcard", back_populates=dbNames.Decks)

    def __repr__(self):
        return f"<Deck(id={self.id}, title='{self.title}', cover_image='{self.cover_image}')>"


class Flashcard(Base):
    __tablename__ = dbNames.Flashcards
    id = Column(Integer, primary_key=True)
    card_type = Column(Integer)
    question = Column(String)
    answer = Column(String)
    difficulty_level = Column(Integer)
    deck_id = Column(Integer, ForeignKey(f"{dbNames.Decks}.id"))

    deck = relationship("Deck", back_populates=dbNames.Flashcards)

    def __repr__(self):
        return f"<Flashcard(id={self.id}, card_type={self.card_type}, question='{self.question}', answer='{self.answer}', difficulty_level={self.difficulty_level}, deck_id={self.deck_id})>"


class Category(Base):
    __tablename__ = dbNames.Categories
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


class FlashcardAnswer(Base):
    __tablename__ = dbNames.FlashcardAnswers
    id = Column(Integer, primary_key=True)
    flashcard_id = Column(Integer, ForeignKey(f"{dbNames.Flashcards}.id"))
    is_correct = Column(Integer)

    flashcard = relationship("Flashcard")

    def __repr__(self):
        return f"<FlashcardAnswer(id={self.id}, flashcard_id={self.flashcard_id}, is_correct={self.is_correct})>"


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
        engine = create_engine("sqlite:///app/flashcard_app.db")

    def _populate_engine(self):
        inspector = inspect(engine)
        if not inspector.has_table(dbNames.Decks):
            Base.metadata.create_all(engine)


global engine
engine = EngineSingleton().engine
# engine = create_engine('sqlite:///app/flashcard_app.db')

# Session = sessionmaker(bind=engine)
# session = Session()
# inspector = inspect(engine)
# if not inspector.has_table('decks'):
#     Base.metadata.create_all(engine)

# session.close()
