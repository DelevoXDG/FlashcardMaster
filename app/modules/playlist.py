from collections import deque

from . import (
    Deck,
    Flashcard,
    get_scoped_session,
    get_universal_session,
    FlashcardAnswer,
)
from .enums import (
    DifficultyLevel,
    StudyType,
)

import random


class Playlist:
    # Define difficulty levels
    difficulties = {
        "Easy": [DifficultyLevel.Easy, DifficultyLevel.Medium, DifficultyLevel.Hard],
        "Hard": [DifficultyLevel.Hard, DifficultyLevel.Medium, DifficultyLevel.Easy],
    }

    def __init__(self, deck_ids, difficulty=None, study_type=None):
        self.flashcard_queue = deque()
        # MAYBE WRONG. I do not know !!!
        self.session = get_universal_session()

        # Get flashcards from database
        flashcards = (
            self.session.query(Flashcard).filter(Flashcard.Deck_id.in_(deck_ids)).all()
        )

        self.sort_flascalrds(flashcards, difficulty, study_type)

        self.flashcard_queue.extend(flashcards)
        self.cur_card = None

    def sort_flascalrds(self, flashcards, difficulty, study_type):
        random.shuffle(flashcards)
        if difficulty in self.difficulties:
            order = self.difficulties[difficulty]
            flashcards.sort(key=lambda x: order.index(x.difficulty_level))

        # if study_type == StudyType.Learn:
        #     flashcards.sort(
        #         key=lambda x: (
        #             1
        #             if x.FlashcardAnswers
        #             and any(answer.is_correct for answer in x.FlashcardAnswers)
        #             else 0,
        #             self.difficulties[difficulty].index(x.difficulty_level)
        #             if difficulty in self.difficulties
        #             else 0,
        #         )
        #     )
        # elif study_type == StudyType.Review:
        #     flashcards.sort(
        #         key=lambda x: (
        #             0
        #             if x.FlashcardAnswers
        #             and any(answer.is_correct for answer in x.FlashcardAnswers)
        #             else 1,
        #             self.difficulties[difficulty].index(x.difficulty_level)
        #             if difficulty in self.difficulties
        #             else 0,
        #         )
        #     )
        if study_type == StudyType.Learn:
            reverse = False
        elif study_type == StudyType.Review:
            reverse = True
        else:
            return
        flashcards.sort(
            key=lambda x: (
                sum(1 for answer in x.FlashcardAnswers if answer.is_correct),
                self.difficulties[difficulty].index(x.difficulty_level)
                if difficulty in self.difficulties
                else 0,
            ),
            reverse=reverse,
        )

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
