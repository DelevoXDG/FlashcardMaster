from collections import deque

from . import (
    Deck,
    Flashcard,
    get_scoped_session,
    get_session, FlashcardAnswer,
)


class Playlist:
    # Define difficulty levels
    difficulties = {
        "Easy": [0, 1, 2],
        "Hard": [2, 1, 0],
    }

    def __init__(self, deck_ids, difficulty=None, study_type=None):
        self.flashcard_queue = deque()
        #MAYBE WRONG. I do not know !!!
        self.session = get_session()

        # Get flashcards from database
        flashcards = (
            self.session.query(Flashcard).filter(Flashcard.Deck_id.in_(deck_ids)).all()
        )

        # Sort flashcards by given difficulty level
        if difficulty in self.difficulties:
            order = self.difficulties[difficulty]
            flashcards.sort(key=lambda x: order.index(x.difficulty_level))

        self.flashcard_queue.extend(flashcards)
        self.cur_card = None

    def next(self):
        if self.has_next():
            self.cur_card = self.flashcard_queue.popleft()
            return self.cur_card
        else:
            return None

    def has_next(self):
        return len(self) > 0

    def record_flashcard_answer(self, is_correct: bool):
        flashcard_answer = FlashcardAnswer()
        flashcard_answer.is_correct = is_correct
        flashcard_answer.Flashcard = self.cur_card
        self.session.add(flashcard_answer)
        self.session.commit()


    def handle_cur(self, is_correct):
        # TODO add entry to flashcard answers
        self.record_flashcard_answer(is_correct)

        if self.cur_card is None:
            return
        if not is_correct:
            self.flashcard_queue.append(self.cur_card)
        self.cur_card = None

    def __len__(self):
        return len(self.flashcard_queue)
