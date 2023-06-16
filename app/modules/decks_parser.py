# from app.modules.database_models import Deck
from PyQt6.QtWidgets import QFileDialog, QMessageBox, QApplication

from .database_models import (
    Deck,
    get_universal_session,
    Flashcard,
)
import re
import json

from typing import List

# from app.modules.database_models import get_universal_session


class DeckParser:
    def __init__(self):
        pass

    def __import_flashcard(self, flashcard_dictionary, new_deck_id, session):
        new_flashcard = Flashcard(
            card_type=flashcard_dictionary["card_type"],
            question=flashcard_dictionary["question"],
            answer=flashcard_dictionary["answer"],
            difficulty_level=flashcard_dictionary["difficulty_level"],
            Deck_id=new_deck_id,
        )
        session.add(new_flashcard)
        session.commit()

    def __import_deck(self, deck_dictionary, session):
        new_deck = Deck(title=deck_dictionary["title"])
        session.add(new_deck)
        session.commit()
        for flashcard_dictionary in deck_dictionary["Flashcards"]:
            self.__import_flashcard(flashcard_dictionary, new_deck.id, session)

    def import_decks(self, decks_json: str) -> None:
        session = get_universal_session()
        deck_dictionaries = json.loads(decks_json)
        for deck_dictionary in deck_dictionaries:
            self.__import_deck(deck_dictionary, session)

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
                self.__map_flashcard_to_dictionary_with_necessery_data(flashcard)
            )
        deck_dictionary["Flashcards"] = flashcard_dictionaries
        return deck_dictionary

    def export_decks(self, decks: List[Deck]) -> str:
        decks_json = json.dumps(
            decks,
            default=lambda o: self.__map_deck_to_dictionary_with_necessary_data(o),
        )
        return decks_json

    @staticmethod
    def is_valid_json_dict(text):
        pattern = r'^\{\s*("[^"]*"\s*:\s*[01]\s*(?:,\s*|\s*\}\s*))*$'
        return re.match(pattern, text) is not None


if __name__ == "__main__":
    # Test examples
    correct_text1 = '{"HL": 0, "PL":0, "DmDo": 1}'
    correct_text2 = '{"Medium": 0, "Big": 0, "Small": 1}'
    incorrect_text1 = '{"HL: 0, "PL": 0, "DmDo": 1}'
    incorrect_text2 = '{"HL": 0", "PL": 0, "DmDo": 1'
    incorrect_text3 = '{"HL": 0, "PL", "DmDo": 1}'
    incorrect_text4 = '{"HL": 0, "PL"0, "DmDo": 1}'
    incorrect_text5 = '{"HL": 0, "PL":: 1}'

    print(DeckParser.is_valid_json_dict(correct_text1))  # True
    print(DeckParser.is_valid_json_dict(correct_text2))  # True
    print(DeckParser.is_valid_json_dict(incorrect_text1))  # False
    print(DeckParser.is_valid_json_dict(incorrect_text2))  # False
    print(DeckParser.is_valid_json_dict(incorrect_text3))  # False
    print(DeckParser.is_valid_json_dict(incorrect_text4))  # False
    print(DeckParser.is_valid_json_dict(incorrect_text5))  # False

# if __name__ == "__main__":


#     session = get_universal_session()
#     deck1 = session.query(Deck).get(51)
#     deck2 = session.query(Deck).get(66)
#     deck_parser = DeckParser()
#     exported_data = deck_parser.export_decks([deck1, deck2])
#     print(exported_data)
#     deck_parser.import_decks(exported_data)
#     # deck_parser.export_decks([deck])
#     # deck_parser.import_deck(json.loads(exported_data))
