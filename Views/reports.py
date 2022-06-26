from prettytable import PrettyTable


class Reports:

    def __init__(self):

        self.table = PrettyTable()

        self.player_report_field_names = [
            "ID",
            "Nom",
            "Prénom",
            "Genre",
            "Date de naissance",
            "Rang"
        ]

        self.tournament_report_field_names = [
            "ID",
            "Nom",
            "Lieu",
            "Description",
            "Début",
            "Fin",
            "Conrôle du temps",
            "Dernier round joué",
            "Joueurs (ID : last_name)",
        ]

        self.matches_report_field_names = [
            "Nom P1",
            "Rang P1",
            "Score P1",
            "Couleur P1",
            " vs",
            "Nom P2",
            "Rang P2",
            "Score P2",
            "Couleur P2"
        ]

        self.rounds_report_field_names = [
            "Round #",
            "Début",
            "fin",
            "Matches"
        ]

    def display_players(self, players, sorting):
        """Affiche le rapport des joueurs par type de tri (nom ou rang)"""
        self.table.clear()
        self.table.field_names = self.player_report_field_names
        self.table.align = "l"

        for i in range(len(players)):
            self.table.add_row([
                players[i]["id"],
                players[i]["last_name"],
                players[i]["first_name"],
                players[i]["gender"],
                players[i]["birth_date"],
                players[i]["rank"]
            ])

        print(f"\n\n\n- Joueurs ({sorting}) -\n")
        print(self.table)

    def display_tournaments_report(self, tournaments):
        """Display tournament reports"""
        self.table.clear()
        self.table.field_names = self.tournament_report_field_names
        self.table.align = "l"

        for i in range(len(tournaments)):
            participants = []
            players = tournaments[i]["players"]
            for k in range(len(players)):
                participants.append(
                    str(players[k]["id"]) + " : " + players[k]["last_name"])

            self.table.add_row([
                tournaments[i]["t_id"],
                tournaments[i]["name"],
                tournaments[i]["place"],
                tournaments[i]["description"],
                tournaments[i]["date"],
                # tournaments[i]["end_date"],
                tournaments[i]["time_control"],
                str(tournaments[i]["current_round"]-1) + "/" + str(tournaments[i]["nb_rounds"]),
                tournaments[i]["rounds"],
                tournaments[i]["players"]
            ])

        print("\n\n\n- Tournois -\n")
        print(self.table)

    def display_matches_report(self, matches):
        """Affiche les matches d'un tournoi"""
        self.table.clear()
        self.table.field_names = self.matches_report_field_names
        self.table.align = "l"

        for i in range(len(matches)):
            matches[i].insert(4, "vs.")
            self.table.add_row(matches[i])

        print(f"\n\n- Matches joués ({len(matches)} total) -\n")
        print(self.table)

    def display_rounds_report(self, rounds):
        """Affiche les rounds d'un tournoi"""
        self.table.clear()
        self.table.field_names = self.rounds_report_field_names
        self.table.align = "l"

        for i in range(len(rounds)):
            for j in range(4):
                if j == 0:
                    self.table.add_row([
                        rounds[i][0],
                        rounds[i][1],
                        rounds[i][2],
                        rounds[i][3][j]
                    ])
                else:
                    self.table.add_row([
                        ' ',
                        ' ',
                        ' ',
                        rounds[i][3][j]
                    ])

        print("\n\n- Round(s) joué(s) -\n")
        print(self.table)

    @staticmethod
    def report_header(info):
        """Entête de du rapport Tournoi
        @paramètres "info": tournoi (dict)
        """
        print("\n\n")

        h_1 = f"{info['name'].upper()}, {info['place'].title()} | Description : {info['description']}"
        h_2 = \
            f"Start date : {info['date']} | " \
            f"Time control : {info['time_control']} | " \
            f"Rounds played : {info['current_round']-1}/{info['nb_rounds']}"

        print(h_1)
        print(h_2)
