from tinydb import TinyDB


class Tournament:
    """Tournoi d'échecs avec règles suisses"""
    def __init__(self, t_id: int, name: str, place: str, date: str, time_control: str,
                 current_round: int, players: list, rounds=list, nb_rounds=4,
                 description=""):
        self.t_id = t_id
        self.name = name
        self.place = place
        self.date = date
        self.time_control = time_control
        self.current_round = current_round
        self.players = players
        self.rounds = rounds
        self.nb_rounds = nb_rounds
        self.description = description
        self.tournaments_db = TinyDB('database/tournaments.json')

    def serialize_tournament(self):
        """Return serialized tournament info"""
        return {
            "t_id": self.t_id,
            "name": self.name,
            "place": self.place,
            "date": self.date,
            "time_control": self.time_control,
            "current_round": self.current_round,
            "players": self.players,
            "rounds": self.rounds,
            "nb_rounds": self.nb_rounds,
            "description": self.description,
        }

    def sort_players_by_rang(self):
        """Tri des joueurs par rang (ascendant)"""
        self.players = sorted(self.players, key=lambda x: x.get('rank'))

    def sort_players_by_score(self):
        """Tri des joueurs par score (descendant)"""
        self.players = sorted(self.players, key=lambda x: x.get('score'), reverse=True)

    def split_players(self):
        """Sépare les joueurs en 2 moitiées (top and down) : cas round 1 par rangs """
        half = len(self.players) // 2
        return self.players[:half], self.players[half:]

    def merge_players(self, top_players, down_players):
        """Distribue les joueurs pour les matches
        Paramètres : - liste top (première moitiée)
                     - liste down (seconde moitiée)
        """
        merged_players = []
        for i in range(len(self.players) // 2):
            merged_players.append(top_players[i])
            merged_players.append(down_players[i])

        self.players = merged_players

    def save_tournament_db(self):
        """Sauvegarde nouveau tournoi en base
        """
        db = self.tournaments_db
        self.t_id = db.insert(self.serialize_tournament())
        db.update({'t_id': self.t_id}, doc_ids=[self.t_id])

    def update_tournament_db(self):
        """Update tournament info (after each round) in database"""
        db = self.tournaments_db
        db.update({'rounds': self.rounds}, doc_ids=[self.t_id])
        db.update({'players': self.players}, doc_ids=[self.t_id])
        db.update({'current_round': self.current_round}, doc_ids=[self.t_id])

    def update_timer(self, timer, info):
        """Update start or end timer of tournament

        @param timer: date and time info (str)
        @param info: start or end time (str)
        """
        db = self.tournaments_db
        db.update({info: timer}, doc_ids=[self.t_id])

    @staticmethod
    def load_tournament_db():
        """Load tournament database

        @return: list of tournaments
        """
        db = TinyDB('database/tournaments.json')
        db.all()
        tournaments_list = []
        for item in db:
            tournaments_list.append(item)
        return tournaments_list
