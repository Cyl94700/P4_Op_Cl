from Views.menu import MenuViews
from Models.tournament import Tournament
from Models.player import Player
from Controllers.tournament_control import TournamentController
from Controllers.reports_control import ReportsController


class MenuController:

    def __init__(self):
        self.menu_view = MenuViews()
        self.tournament_control = TournamentController()
        self.reports_control = ReportsController()

    def main_menu_start(self):
        """Menu principal qui renvoie vers les sous-menus"""

        self.menu_view.main_menu()
        self.menu_view.input_option()
        user_input = input().lower()

        if user_input == "1":
            self.new_tournament()

        elif user_input == "2":
            self.load_tournament()

        elif user_input == "3":
            self.new_player()

        elif user_input == "4":
            self.update_player()

        elif user_input == "5":
            self.reports_menu()

        elif user_input == "q":
            self.menu_view.sure_exit()
            user_input = input().lower()

            if user_input == "o":
                exit()
            elif user_input == "n":
                self.main_menu_start()

        else:
            self.menu_view.input_error()
            self.main_menu_start()

    def new_tournament(self):
        """Création nouveau tournoi en base de données"""
        self.menu_view.create_tournament_header()
        tournament_info = []
        options = [
            "le nom",
            "le lieu",
            "la description"
        ]

        for item in options:
            self.menu_view.input_text(item)
            user_input = input()
            # Cohérence saisie
            user_input = self.not_enter_input(user_input, item)

            if user_input == "r":
                self.main_menu_start()

            else:
                tournament_info.append(user_input)

        tournament_info.append(self.input_time_control())
        tour_players = self.select_players(8)

        self.menu_view.review_tournament(tournament_info, tour_players)
        user_input = input().lower()
        # saisie obligatoire et cohérence
        while user_input == '' or user_input not in (["o", "n"]):
            self.menu_view.review_tournament(tournament_info, tour_players)
            user_input = input().lower()
        if user_input == "o":
            tournament = Tournament(
                t_id=0,
                name=tournament_info[0],
                place=tournament_info[1],
                date="Non débuté",
                description=tournament_info[2],
                time_control=tournament_info[3],
                players=tour_players,
                current_round=1,
                rounds=[]
            )
            tournament.save_tournament_db()
            self.menu_view.tournament_saved()

            self.menu_view.start_tournament()
            user_input = input()
            # saisie obligatoire
            while user_input == '' or user_input not in (["o", "n"]):
                self.menu_view.start_tournament()
                user_input = input()
            if user_input == "o":
                self.tournament_control.start_tournament(tournament)
            elif user_input == "n":
                self.main_menu_start()

        elif user_input == "n":
            self.main_menu_start()

    def input_time_control(self):
        """Select le contrôle du temps d'un tournoi
        @return: time control (str)
        """
        self.menu_view.time_control_option()
        self.menu_view.input_option()
        user_input = input()

        if user_input == "1":
            return "Bullet"
        elif user_input == "2":
            return "Blitz"
        elif user_input == "3":
            return "Rapid"

        else:
            self.menu_view.input_error()
            self.input_time_control()

    def select_players(self, players_total):
        """Choix des joueurs d'un Tournoi
        @paramètres : "players_total" : nombre de joueurs à selectionner
        @return : liste des joueurs selectionnés
        """
        players = Player.load_player_db()
        id_list = []
        for i in range(len(players)):
            id_list.append(players[i]["id"])

        tour_players = []

        i = 0
        while i < players_total:
            self.menu_view.select_players(players, i+1)
            self.menu_view.input_option()
            user_input = input()

            if user_input == "r":
                self.main_menu_start()

            elif not user_input.isdigit():
                self.menu_view.input_error()

            elif int(user_input) in id_list:
                index = id_list.index(int(user_input))
                tour_players.append(players[index])
                id_list.remove(id_list[index])
                players.remove(players[index])
                i += 1

            else:
                self.menu_view.player_already_selected()

        return tour_players

    def load_tournament(self):
        """Choix d'un tournoi à charger"""
        tournament = Tournament.load_tournament_db()

        self.menu_view.select_tournament(tournament)
        self.menu_view.input_option()
        user_input = input()
        int_user_input = int(user_input)
        # Total des lignes de tournament
        t_id = len(tournament)
        # Cohérence saisie :
        while user_input == '' or int_user_input > t_id or int_user_input == 0:
            self.menu_view.select_tournament(tournament)
            self.menu_view.input_option()
            user_input = input()
            int_user_input = int(user_input)
        if user_input == "r":
            self.main_menu_start()

        for i in range(len(tournament)):
            if user_input == str(tournament[i]["t_id"]):
                t = tournament[i]
                t = Tournament(
                    t["t_id"],
                    t["name"],
                    t["place"],
                    t["date"],
                    t["time_control"],
                    t["current_round"],
                    t["players"],
                    t["rounds"],
                    t["nb_rounds"],
                    t["description"]
                )
                self.tournament_control.start_tournament(t)

    def new_player(self):
        """Création d'un nouveau joueur en base"""
        self.menu_view.create_new_player_header()
        player_info = []
        options = [
            "le nom",
            "le prénom",
            "la date de naissance (jj/mm/aaaa)",
            "le genre [M/F]",
            "la rang"
        ]
        for item in options:
            self.menu_view.input_text(item)
            user_input = input()
            # Cohérence saisie
            user_input = self.not_enter_input(user_input, item)
            if user_input == "r":
                self.main_menu_start()
            else:
                player_info.append(user_input)

        MenuViews.review_player(player_info)
        user_input = input().lower()
        # saisie obligatoire
        while user_input == '' or user_input not in (["o", "n"]):
            MenuViews.review_player(player_info)
            user_input = input().lower

        if user_input == "o":
            player = Player(
                player_id=0,
                last_name=player_info[0],
                first_name=player_info[1],
                birth_date=player_info[2],
                gender=player_info[3],
                rank=int(player_info[4])
            )

            player.save_player_db()
            self.menu_view.player_saved()
            self.main_menu_start()

        elif user_input == "n":
            self.main_menu_start()

    def update_player(self):
        """Modifier un joueur"""
        players = Player.load_player_db()

        self.menu_view.select_players(players, "à modifier")
        self.menu_view.input_option()
        user_input = input()
        # Nombre de lignes de la liste "players"
        p_id = len(players)
        # "user_input" numérique ?
        result = self.numeric(user_input)
        if result is True:
            int_user_input = int(user_input)
        else:
            int_user_input = -1
        # Cohérence saisie :
        while result is False and user_input != 'r' or result is True and int_user_input > p_id \
                or result is True and int_user_input == 0:
            self.menu_view.input_error()
            self.menu_view.input_option()
            user_input = input()
            result = self.numeric(user_input)
            if result is True:
                int_user_input = int(user_input)

        if user_input == "r":
            self.main_menu_start()

        p = players[int(user_input) - 1]
        p = Player(
            p['id'],
            p['last_name'],
            p['first_name'],
            p['birth_date'],
            p['gender'],
            p['rank']
        )

        options = [
            "last_name",
            "first_name",
            "birth_date",
            "gender",
            "rank"
        ]
        french_options = [
            "nom",
            "prénom",
            "date de naissance (jj/mm/aaaa)",
            "genre [M/F]",
            "rang"
        ]
        self.menu_view.update_player(p, french_options)
        self.menu_view.input_option()
        user_input = input()
        # user_input numérique ?
        result = self.numeric(user_input)
        if result is True:
            int_user_input = int(user_input)
        else:
            int_user_input = -1
        # Cohérence saisie :
        while result is False and user_input != 'r' or result is True and int_user_input > len(options) \
                or result is True and int_user_input == 0:
            self.menu_view.input_error()
            self.menu_view.input_option()
            user_input = input()
            result = self.numeric(user_input)
            if result is True:
                int_user_input = int(user_input)
        if user_input == "r":
            self.main_menu_start()

        elif int(user_input) <= len(options):
            updated_info = (options[int(user_input) - 1])
            self.menu_view.input_text(
                f"la nouvelle valeur {french_options[int(user_input) - 1]}")
            user_input = input()
            # Saisie obligatoire :
            while user_input == '':
                self.menu_view.input_error()
                self.menu_view.input_text(
                    f"la nouvelle valeur {options[int(user_input) - 1]}")
            if user_input == "r":
                self.main_menu_start()

            else:
                p.update_player_db(user_input, updated_info)
                self.menu_view.player_saved()
                self.update_player()

    def reports_menu(self):
        """Menu des Rapports"""
        self.menu_view.reports_menu()
        self.menu_view.input_option()
        user_input = input()

        if user_input == "1":
            self.player_reports_sorting(Player.load_player_db())

        elif user_input == "2":
            self.player_reports_sorting(self.reports_control.tournament_players())

        elif user_input == "3":
            self.reports_control.all_tournaments()

        elif user_input == "4":
            self.reports_control.tournament_rounds()

        elif user_input == "5":
            self.reports_control.tournament_matches()

        elif user_input == "r":
            self.main_menu_start()

        else:
            self.menu_view.input_error()
            self.reports_menu()

        self.menu_view.other_report()
        user_input = input()
        while user_input not in (["o", "n"]):
            self.menu_view.input_error()
            self.menu_view.other_report()
            user_input = input()

        if user_input == "o":
            self.reports_menu()

        elif user_input == "n":
            self.main_menu_start()

    def player_reports_sorting(self, players):
        """
        Sélectionne un tri des joueurs par nom ou par rang
        @paramètres "players" : liste des joueurs
        """
        self.menu_view.reports_player_sorting()
        self.menu_view.input_option()
        user_input = input()

        if user_input == "1":
            self.reports_control.all_players_name(players)

        elif user_input == "2":
            self.reports_control.all_players_rank(players)

        elif user_input == "r":
            self.main_menu_start()
        else:
            if len(players) == 8:
                self.menu_view.input_error()
                self.player_reports_sorting(players)

            else:
                self.menu_view.input_error()
                self.player_reports_sorting(Player.load_player_db())

    def not_enter_input(self, user_input, item):
        """Saisie touche Entrée non autorisée
        """
        while user_input == '':
            self.menu_view.need_text()
            self.menu_view.input_text(item)
            user_input = input()
        return user_input

    @staticmethod
    def numeric(user_input):
        """Détermine si "user_input" est une valeur numérique
        """
        try:
            int(user_input)
            result = True
        except ValueError:
            result = False
        return result
