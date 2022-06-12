class Player:
    """Joueur d'un tournoi"""
    def __init__(self, name, first_name, date_of_birth, gender, total_score, rank=0):
        self.name = name
        self.first_name = first_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.total_score = total_score
        self.tournament_score = 0
        self.rank = rank
        self.played_with = []
