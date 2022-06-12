class Tournament:
    """Tournoi d'échecs avec règles suisses"""
    def __init__(self, name, place, start_date, end_date, time_control, players, nb_rounds=4, description=""):
        self.name = name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.time_control = time_control
        self.players = players
        self.nb_rounds = nb_rounds
        self.rounds = []
        self.desccription = description
