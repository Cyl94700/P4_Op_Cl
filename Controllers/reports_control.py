from Models.tournament import Tournament
from Views.menu import MenuViews
from Views.reports import Reports


class ReportsController:

    def __init__(self):
        # MenuViews = MenuViews()
        self.reports_view = Reports()

    def all_players_name(self, players):
        """ Rapport joueurs (triés par nom)
        @paramètres "players" : liste des joueurs
        """
        players = sorted(players, key=lambda x: x.get('last_name'))
        self.reports_view.display_players(players, "par nom")

    def all_players_rank(self, players):
        """Rapport joueurs (tri par rang)
        @paramètres "players" : liste des joueurs
        """
        players = sorted(players, key=lambda x: x.get('rank'))
        self.reports_view.display_players(players, "par rang")

    def tournament_players(self):
        """Affiche les joueurs d'un tournoi
        Selectionne un tournoi puis affiche ses joueurs
        @return : liste des joueurs d'un tournoi
        """
        user_input, tournaments = self.tournament_select()

        for i in range(len(tournaments)):
            if user_input == str(tournaments[i]['t_id']):
                return tournaments[i]["players"]

    def all_tournaments(self):
        """Rapport des tournois"""
        self.reports_view.display_tournaments_report(Tournament.load_tournament_db())

    def tournament_rounds(self):
        """Rapport des rounds d'un tournoi"""
        user_input, tournaments = self.tournament_select()

        self.reports_view.report_header(tournaments[int(user_input) - 1])
        self.reports_view.display_rounds_report(tournaments[int(user_input) - 1]["rounds"])

    def tournament_matches(self):
        """Rapport des matches d'un tournoi"""
        user_input, tournaments = self.tournament_select()

        self.reports_view.report_header(tournaments[int(user_input) - 1])

        rounds = tournaments[int(user_input) - 1]["rounds"]
        round_matches = []
        for i in range(len(rounds)):
            round_matches.append(rounds[i][3])

        matches = []
        for i in range(len(round_matches)):
            for k in range(4):
                matches.append(round_matches[i][k])

        self.reports_view.display_matches_report(matches)

    def tournament_select(self):
        """Charge tous les tournois pour sélection

        @return : Sélection utilisateur, liste info tournoi
        """
        from Controllers.menu_control import MenuController
        tournaments = Tournament.load_tournament_db()
        MenuViews.select_tournament(tournaments)
        MenuViews.input_option()
        user_input = input()
        # Contrôle de saisie
        length_menu = len(tournaments)
        valid_strings = ["r"]
        response = MenuController.input_validation(user_input, length_menu, valid_strings)
        while response is False:
            MenuViews.input_error()
            user_input = input()
            response = MenuController.input_validation(user_input, length_menu, valid_strings)
        if user_input == "r":
            self.back_to_menu()
        else:
            return user_input, tournaments

    @staticmethod
    def back_to_menu():
        from Controllers.menu_control import MenuController
        MenuController().main_menu_start()
