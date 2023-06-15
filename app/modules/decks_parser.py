# from app.modules.database_models import Deck
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication

from database_models import (
    Deck,
    get_session,
    Flashcard,
)

import json
from typing import List

# from app.modules.database_models import get_session


class DeckParser:
    def __init__(self):
        pass

    def __import_flashcard(self, flashcard_dictionary, new_deck_id):
        new_flashcard = Flashcard(
            card_type=flashcard_dictionary["card_type"],
            question=flashcard_dictionary["question"],
            answer=flashcard_dictionary["answer"],
            difficulty_level=flashcard_dictionary["difficulty_level"],
            Deck_id=new_deck_id,
        )
        session.add(new_flashcard)
        session.commit()

    def __import_deck(self, deck_dictionary):
        new_deck = Deck(title=deck_dictionary["title"])
        session.add(new_deck)
        session.commit()
        for flashcard_dictionary in deck_dictionary["Flashcards"]:
            self.__import_flashcard(flashcard_dictionary, new_deck.id)



    def import_decks(self, decks_json: str) -> None:
        session = get_session()
        deck_dictionaries = json.loads(decks_json)
        for deck_dictionary in deck_dictionaries:
            self.__import_deck(deck_dictionary)

    def __map_flashcard_to_dictionary_with_necessery_data(self, flashcard: Flashcard):
        flashcard_dict = flashcard.as_dict()
        del flashcard_dict["id"]
        del flashcard_dict["Deck_id"]
        return flashcard_dict

    def __map_deck_to_dictionary_with_necessary_data(self, deck: Deck):
        deck_dictionary = deck.as_dict()
        del deck_dictionary["id"]  # usuwam id
        del deck_dictionary["Category_id"]  # usuwam category
        flashcard_dictionaries = []
        for flashcard in deck.Flashcards:
            flashcard_dictionaries.append(
                self.__map_flashcard_to_dictionary_with_necessery_data(flashcard))
        deck_dictionary["Flashcards"] = flashcard_dictionaries
        return deck_dictionary



    def export_decks(self, decks: List[Deck]) -> str:
        decks_json = json.dumps(decks, default=lambda o: self.__map_deck_to_dictionary_with_necessary_data(o))
        return decks_json


if __name__ == "__main__":
    session = get_session()
    deck1 = session.query(Deck).get(51)
    deck2 = session.query(Deck).get(66)
    deck_parser = DeckParser()
    exported_data = deck_parser.export_decks([deck1, deck2])
    print(exported_data)
    deck_parser.import_decks(exported_data)
    # deck_parser.export_decks([deck])
    #deck_parser.import_deck(json.loads(exported_data))
