class DifficultyLevel:
    Easy = 0
    Medium = 1
    Hard = 2

    @classmethod
    def get_name(cls, level):
        """Returns the name corresponding to the given difficulty level"""
        level_names = {
            cls.Easy: "easy",
            cls.Medium: "medium",
            cls.Hard: "hard",
        }
        return level_names.get(level, "N/A")


class CardType:
    Text = 0
    TrueFalse = 1
    MultipleChoice = 2

    @classmethod
    def get_name(cls, level):
        """Returns the name corresponding to the given card type"""
        card_type_names = {
            cls.Text: "Text",
            cls.TrueFalse: "True/False",
            cls.MultipleChoice: "Multiple Choice",
        }
        return card_type_names.get(level, "N/A")


class StudyMode:
    Flip = 0
    Quiz = 1


class StudyType:
    Random = 0
    Learn = 1
    Review = 2
