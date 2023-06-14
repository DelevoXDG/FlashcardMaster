#from app.modules.database_models import Deck
from database_models import Deck, get_session, Flashcard

import json
#from app.modules.database_models import get_session

class DeckParser():
    def __init__(self):
        pass
    def import_deck(self, deck_json: str) -> Deck:
        pass
    def export_deck(self, deck: Deck) -> str:
        # deck_json = json.dumps(deck.as_dict())
        dict = deck.as_dict()
        dict["Flashcards"] = deck.Flashcards
        deck_json = json.dumps(dict, default=lambda o: o.as_dict())
        return deck_json
    
if __name__ == "__main__":
    session = get_session()
    deck = session.query(Deck).get(51)
    deck_parser = DeckParser()
    print(deck_parser.export_deck(deck))