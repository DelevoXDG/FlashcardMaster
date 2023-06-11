class DifficultyLevel:
    EASY = 0
    MEDIUM = 1
    HARD = 2

    @classmethod
    def get_name(cls, level):
        """Returns the name corresponding to the given difficulty level"""
        level_names = {cls.EASY: "easy", cls.MEDIUM: "medium", cls.HARD: "hard"}
        return level_names.get(level, "N/A")
