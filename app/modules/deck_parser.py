# from app.modules.database_models import Deck
from database_models import (
    Deck,
    get_session,
    Flashcard,
)

import json

# from app.modules.database_models import get_session


class DeckParser:
    def __init__(self):
        pass

    def import_deck(self, deck_json) -> Deck:
        session = get_session()
        new_deck = Deck(title=deck_json["title"])
        session.add(new_deck)
        session.commit()
        new_deck_id = new_deck.id

        for flashcard in deck_json["Flashcards"]:
            new_flashcard = Flashcard(
                card_type=flashcard["card_type"],
                question=flashcard["question"],
                answer=flashcard["answer"],
                difficulty_level=flashcard["difficulty_level"],
                Deck_id=new_deck_id,
            )
            session.add(new_flashcard)
            session.commit()
        # pass

    def export_deck(self, deck: Deck) -> str:
        dict = deck.as_dict()
        dict["Flashcards"] = deck.Flashcards
        deck_json = json.dumps(dict, default=lambda o: o.as_dict())
        return deck_json


if __name__ == "__main__":
    session = get_session()
    deck = session.query(Deck).get(51)
    deck_parser = DeckParser()
    exported_data = deck_parser.export_deck(deck)
    print(exported_data)
    deck_parser.import_deck(json.loads(exported_data))
