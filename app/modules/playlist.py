from collections import deque

from database_models import get_scoped_session


class Playlist:
    def __init__(self, deck_ids):
        self.flashcard_ids = deque()
        session = get_scoped_session()
        # get Flashcard sqlalchemy ojbects from db
        # self.cur_card

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
