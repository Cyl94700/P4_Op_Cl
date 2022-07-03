import random


class Match:

    """
    Classe qui représente un match entre 2 joueurs
    ...
    """

    def __init__(self, player1, rank_player1, score_player1, color_player1,
                 player2, rank_player2, score_player2, color_player2):
        """
        Constructeur objet match

        Paramètres
        ----------
        """
        self.player1 = player1
        self.rank_player1 = rank_player1
        self.score_player1 = score_player1
        self.color_player1 = color_player1
        self.player2 = player2
        self.rank_player2 = rank_player2
        self.score_player2 = score_player2
        self.color_player2 = color_player2

        self.assign_colors()

    def __getitem__(self, key):
        return self.player1, self.rank_player1, self.score_player1, self.color_player1, \
                self.player2, self.rank_player2, self.score_player2, self.color_player2

    def assign_colors(self):
        if random.choice([True, False]):
            self.color_player1 = "Blancs"
            self.color_player2 = "Noirs"
        else:
            self.color_player1 = "Noirs"
            self.color_player2 = "Blancs"

        return [self.color_player1, self.color_player2]
