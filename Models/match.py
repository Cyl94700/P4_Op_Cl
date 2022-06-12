class Match:
    """Macth entre 2 joueurs"""
    def __init__(self, color_player_1, player_1, color_player_2, player_2,
                 score_player_1=0, score_player_2=0):
        self.color_player_1 = color_player_1
        self.player_1 = player_1
        self.color_player_2 = color_player_2
        self.player_2 = player_2
        self.score_player_1 = score_player_1
        self.score_player_2 = score_player_2
