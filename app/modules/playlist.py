from collections import deque

from . import (
    Deck,
    Flashcard,
    get_scoped_session,
)

class Playlist:
    difficulties = {
        "Easy": [1, 2, 3],
        "Medium": [2, 1, 3],
        "Hard": [3, 2, 1],
    }

    def __init__(self, deck_ids, difficulty=None, study_type=None):
        # Warto wnieść pewność na temat study_type
        self.flashcard_ids = deque()
        session = get_scoped_session()

        flashcards = session.query(Flashcard).filter(Flashcard.Deck_id.in_(deck_ids)).all()

        if difficulty in self.difficulties:
            order = self.difficulties[difficulty]
            flashcards.sort(key=lambda x: order.index(x.difficulty))

        self.flashcard_ids.extend(flashcard.id for flashcard in flashcards)
        self.cur_card = None

    def next(self):
        self.cur_card = self.flashcard_ids.popleft()
        return self.cur_card

    def has_next(self):
        return len(self) > 0

    def handle_cur(self, is_correct):
        if self.cur_card is None:
            return
        if not is_correct:
            self.flashcard_ids.append(self.cur_card)
        self.cur_card = None

    def __len__(self):
        return len(self.flashcard_ids)
