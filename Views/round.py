from prettytable import PrettyTable


class RoundViews:

    def __init__(self):
        self.table = PrettyTable()

        self.round_field_names = [
            "Match #",
            "Name P1",
            "rank P1",
            "Score P1",
            "Color P1",
            " ",
            "Name P2",
            "rank P2",
            "Score P2",
            "Color P2"
        ]

        self.results_field_names = [
            "Classement",
            "Nom",
            "Score final",
            "Rang"
        ]

    def display_matches(self, matches):
        """
        Affiche les matches de la ronde sélectionnée sous forme de tableau
        Paramètres = matches : liste tuple des matches
        """
        self.table.clear()
        self.table.field_names = self.round_field_names

        for i in range(len(matches)):
            row = list(matches[i])
            row.insert(0, str(i+1))
            row.insert(5, "vs.")

            self.table.add_row(row)

        print(self.table)

    def display_results(self, t):
        """
        Affiches les résultats d'un tournoi terminé
        Paramètres = t : tournoi sélectionné
        """
        self.table.clear()
        self.table.field_names = self.results_field_names

        for i in range(len(t.players)):
            self.table.add_row([
                i+1,
                t.players[i]["last_name"] + ", " + t.players[i]["first_name"],
                t.players[i]["score"],
                t.players[i]["rank"],
            ])

        print("\n\n- RESULTATS -\n")
        print(f"{t.name.upper()}, {t.place.title()} | Description : {t.description}")
        print(f"Start : {t.date} | Contrôle du temps : {t.time_control}\n")

        print(self.table)

    @staticmethod
    def round_header(t, start_time):
        """
        Affiche les infos générales d'un tournoi en entête
        Paramètres = t : Tournoi selectionné
        Paramètres = start_time : Date de début de tournoi
        """
        print("\n\n")

        h_1 = f"{t.name.upper()}, {t.place.title()} | Description : {t.description}"
        h_2 = f"Débuté : {t.date} | Contrôle du temps : {t.time_control}\n"
        h_3 = f"- ROUND {t.current_round}/{t.nb_rounds} | {start_time} -"

        print(h_1.center(100, " "))
        print(h_2.center(100, " "))
        print(h_3.center(100, " "))

    @staticmethod
    def round_over():
        print("\nRound terminé ? [o=ok]")
        print("Retour au menu principal ? [r]")

    @staticmethod
    def score_options(match_number):
        print("\nMatch ", match_number)
        print('[0] Match nul')
        print('[1] Player 1 gagne')
        print('[2] Player 2 gagne')
        print("\n[r] Retour au menu principal")

    @staticmethod
    def score_input_option():
        print('\nVotre choix  :', end=' ')
