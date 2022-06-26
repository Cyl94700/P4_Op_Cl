from Models.match import Match


"""
class Round:
#Ronde d'un tournoi
def __init__(self, name, matches):
self.name = name
self.matches = matches
"""


class Round:

    def __init__(
            self,
            round_name: str,
            start_datetime: str,
            end_datetime: str
    ):
        self.round_name = round_name
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.matches = []

    def set_round(self):
        """Return round info as list"""
        return [
            self.round_name,
            self.start_datetime,
            self.end_datetime,
            self.matches
        ]

    def get_match_pairing(self, player_1, player_2):
        """Set match paring as tuple"""
        # colors = []
        colors = Match.assign_colors(self)
        color_player1 = colors[0]
        color_player2 = colors[1]

        match = (
            f"{player_1['last_name']}, {player_1['first_name']}",
            player_1["rank"],
            player_1["score"],
            color_player1,
            f"{player_2['last_name']}, {player_2['first_name']}",
            player_2["rank"],
            player_2["score"],
            color_player2
        )

        self.matches.append(match)
