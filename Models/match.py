import random


class Match:
    """
    Classe qui représente un match entre 2 joueurs
    ...
    """

    def __init__(self, name, players_pair):
        """
        Constructeur objet match

        Paramètres
        ----------


        """
        self.name = name
        self.player1 = players_pair[0]
        self.score_player1 = 0.0
        self.color_player1 = ""
        self.player2 = players_pair[1]
        self.score_player2 = 0.0
        self.color_player2 = ""

    def assign_colors(self):
        if random.choice([True, False]):
            self.color_player1 = "Blancs"
            self.color_player2 = "Noirs"
        else:
            self.color_player1 = "Noirs"
            self.color_player2 = "Blancs"

        return [self.color_player1, self.color_player2]

    def color_shuffle(self):
        pass
