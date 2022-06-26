from tinydb import TinyDB


class Player:
    """Joueur d'un tournoi"""
    def __init__(self, player_id: int, last_name: str, first_name: str, birth_date: str, gender: str, rank=0):
        self.player_id = player_id
        self.last_name = last_name
        self.first_name = first_name
        self.birth_date = birth_date
        self.gender = gender
        self.rank = rank
        self.score = 0.0
        self.opponents = []
        self.player_db = TinyDB('database/players.json')

    def serialize_player(self):
        """Return serialized player info"""
        return {
            "id": self.player_id,
            "last_name": self.last_name,
            "first_name": self.first_name,
            "birth_date": self.birth_date,
            "gender": self.gender,
            "rank": self.rank,
            "score": self.score,
            "opponents": self.opponents
        }

    def save_player_db(self):
        """Sauvegarde un nouveau joueur dans la base de données
        """
        players_db = self.player_db
        self.player_id = players_db.insert(self.serialize_player())
        players_db.update({'id': self.player_id}, doc_ids=[self.player_id])

    def update_player_db(self, info, option):
        """Modifie info joueur depuis input user

        @param info: user input (str, or int pour "rank")
        @param option: update info category
        """
        db = self.player_db
        if option == "rank":
            db.update({option: int(info)}, doc_ids=[self.player_id])
        else:
            db.update({option: info}, doc_ids=[self.player_id])

    @staticmethod
    def load_player_db():
        """Chargement liste de joueurs

        @return : liste de joueurs
        """
        players_db = TinyDB('database/players.json')
        players_db.all()
        players = []
        for player in players_db:
            players.append(player)

        return players
