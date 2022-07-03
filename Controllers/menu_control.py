from Views.menu import MenuViews
from Models.tournament import Tournament
from Models.player import Player
from Controllers.tournament_control import TournamentController
from Controllers.reports_control import ReportsController
import datetime


class MenuController:
    def __init__(self):
        # self.menu_view = MenuViews()
        self.tournament_controller = TournamentController()
        self.reports_control = ReportsController()

    def main_menu_start(self):
        """Menu principal qui renvoie vers les sous-menus"""
        MenuViews.application_title()
        menu_lines = ["Créer un tournoi",
                      "Charger un tournoi",
                      "Créer un joueur",
                      "Modifier un joueur",
                      "Rapport",
                      ]
        MenuViews.main_menu(menu_lines)
        MenuViews.input_option()
        user_input = input()
        length_menu = int(len(menu_lines))
        valid_strings = ["q"]
        # contrôle de saisie
        result = self.input_validation(user_input, length_menu, valid_strings)
        if result is True:
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
                MenuViews.sure_exit()
                user_input = input()
                valid_strings = ["o", "n"]
                length_menu = 0
                # contrôle de saisie
                result = self.input_validation(user_input, length_menu, valid_strings)
                while result is False:
                    MenuViews.input_error()
                    MenuViews.sure_exit()
                    user_input = input()
                    # contrôle de saisie
                    result = self.input_validation(user_input, length_menu, valid_strings)
                if user_input == "o":
                    exit()
                elif user_input == "n":
                    self.main_menu_start()

        else:
            MenuViews.input_error()
            self.main_menu_start()

    def new_tournament(self):
        """Création nouveau tournoi en base de données"""
        MenuViews.create_tournament_header()
        tournament_info = []
        options = [
            "le nom",
            "le lieu",
            "la description"
        ]

        for item in options:
            MenuViews.input_text(item)
            user_input = input()
            # Cohérence saisie
            response = self.input_control_required_data(user_input)
            while response is False:
                MenuViews.input_error()
                MenuViews.input_text(item)
                user_input = input()

            if user_input == "r":
                self.main_menu_start()

            else:
                tournament_info.append(user_input)

        tournament_info.append(self.input_time_control())
        tour_players = self.select_players(8)

        MenuViews.review_tournament(tournament_info, tour_players)
        user_input = input()
        length_menu = 0
        valid_strings = ["o", "n"]
        # saisie obligatoire et cohérence
        result = self.input_validation(user_input, length_menu, valid_strings)
        while result is False:
            MenuViews.input_error()
            MenuViews.review_tournament(tournament_info, tour_players)
            user_input = input()
            # contrôle de saisie
            result = self.input_validation(user_input, length_menu, valid_strings)
        if user_input == "o":
            tournament = Tournament(
                t_id=0,
                name=tournament_info[0],
                place=tournament_info[1],
                date="Non débuté",
                end_date="Non terminé",
                description=tournament_info[2],
                time_control=tournament_info[3],
                players=tour_players,
                current_round=1,
                rounds=[]
            )
            tournament.save_tournament_db()
            MenuViews.tournament_saved()

            MenuViews.start_tournament()
            user_input = input()
            # saisie obligatoire et cohérence
            result = self.input_validation(user_input, length_menu, valid_strings)
            while result is False:
                MenuViews.input_error()
                MenuViews.start_tournament()
                user_input = input()
                # contrôle de saisie
                result = self.input_validation(user_input, length_menu, valid_strings)
            if user_input == "o":
                self.tournament_controller.start_tournament(tournament)
            elif user_input == "n":
                self.main_menu_start()

        elif user_input == "n":
            self.main_menu_start()

    def input_time_control(self):
        """Selectionne le contrôle du temps d'un tournoi
        @return: time control (str)
        """
        MenuViews.time_control_option()
        MenuViews.input_option()
        user_input = input()

        if user_input == "1":
            return "Bullet"
        elif user_input == "2":
            return "Blitz"
        elif user_input == "3":
            return "Rapid"

        else:
            MenuViews.input_error()
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
            MenuViews.select_players(players, i+1)
            MenuViews.input_option()
            user_input = input()

            if user_input == "r":
                self.main_menu_start()

            elif not user_input.isdigit():
                MenuViews.input_error()

            elif int(user_input) in id_list:
                index = id_list.index(int(user_input))
                tour_players.append(players[index])
                id_list.remove(id_list[index])
                players.remove(players[index])
                i += 1

            else:
                MenuViews.player_out_of_bounds()

        return tour_players

    def load_tournament(self):
        """Choix d'un tournoi à charger"""
        tournament = Tournament.load_tournament_db()

        MenuViews.select_tournament(tournament)
        MenuViews.input_option()
        user_input = input()
        length_menu = int(len(tournament))
        valid_strings = ["r"]
        # contrôle de saisie
        result = self.input_validation(user_input, length_menu, valid_strings)
        while result is False:
            MenuViews.input_error()
            MenuViews.input_option()
            user_input = input()
            result = self.input_validation(user_input, length_menu, valid_strings)

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
                    t["end_date"],
                    t["time_control"],
                    t["current_round"],
                    t["players"],
                    t["rounds"],
                    t["nb_rounds"],
                    t["description"]
                )
                self.tournament_controller.start_tournament(t)

    def new_player(self):
        """Création d'un nouveau joueur en base"""
        MenuViews.create_new_player_header()
        player_info = []
        options = [
            "le nom",
            "le prénom",
            "la date de naissance (jj/mm/aaaa)",
            "le genre [M/F]",
            "le rang (entre 1 et 10 000)"
        ]
        i = 0
        for item in options:
            MenuViews.input_text(item)
            user_input = input()
            # Saisie obligaoire pour nom et prénom
            if i <= 1:
                response = self.input_control_required_data(user_input)
                while response is False:
                    MenuViews.input_error()
                    MenuViews.input_text(item)
                    user_input = input()
                    response = self.input_control_required_data(user_input)
            # controle de la date
            if i == 2:
                response = self.validate(user_input)
                while response is False and user_input != "r":
                    MenuViews.date_error()
                    MenuViews.input_text(item)
                    user_input = input()
                    response = self.validate(user_input)
            # Contrôle Genre
            if i == 3:
                length_menu = 0
                valid_strings = ["M", "F", "r"]
                result = self.input_validation(user_input, length_menu, valid_strings)
                while result is False:
                    MenuViews.input_error()
                    MenuViews.input_text(item)
                    user_input = input()
                    result = self.input_validation(user_input, length_menu, valid_strings)
            # contrôle Rang
            if i == 4:
                length_menu = 10000
                valid_strings = ["r"]
                result = self.input_validation(user_input, length_menu, valid_strings)
                while result is False:
                    MenuViews.input_error()
                    MenuViews.input_text(item)
                    user_input = input()
                    result = self.input_validation(user_input, length_menu, valid_strings)
            i += 1

            if user_input == "r":
                self.main_menu_start()
            else:
                player_info.append(user_input)

        MenuViews.review_player(player_info)
        user_input = input()
        # Controle réponse sauvegarde
        length_menu = 0
        valid_strings = ["o", "n"]
        result = self.input_validation(user_input, length_menu, valid_strings)
        while result is False:
            MenuViews.input_error()
            MenuViews.review_player(player_info)
            user_input = input()
            result = self.input_validation(user_input, length_menu, valid_strings)

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
            MenuViews.player_saved()
            self.main_menu_start()

        elif user_input == "n":
            self.main_menu_start()

    def update_player(self):
        """Modifier un joueur"""
        players = Player.load_player_db()

        MenuViews.select_players(players, "à modifier")
        MenuViews.input_option()
        user_input = input()
        length_menu = len(players)
        valid_strings = ["r"]
        result = self.input_validation(user_input, length_menu, valid_strings)
        while result is False:
            MenuViews.input_error()
            MenuViews.input_option()
            user_input = input()
            result = self.input_validation(user_input, length_menu, valid_strings)

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
            "rang [1, 10 000]"
        ]
        MenuViews.update_player(p, french_options)
        MenuViews.input_option()
        user_input = input()
        # Contrôle de saisie
        length_menu = len(french_options)
        valid_strings = ["r"]
        result = self.input_validation(user_input, length_menu, valid_strings)
        while result is False:
            MenuViews.input_error()
            MenuViews.input_option()
            user_input = input()
            result = self.input_validation(user_input, length_menu, valid_strings)

        if user_input == "r":
            self.main_menu_start()

        elif int(user_input) <= len(options):
            updated_info = (options[int(user_input) - 1])
            french_updated_info = (french_options[int(user_input) - 1])
            MenuViews.input_text(
                f"la nouvelle valeur {french_options[int(user_input) - 1]}")
            user_input = input()

            # Saisie obligaoire pour nom et prénom
            if updated_info == "last_name" or updated_info == "first_name":
                response = self.input_control_required_data(user_input)
                while response is False:
                    MenuViews.need_text()
                    MenuViews.input_text(f"la nouvelle valeur {french_updated_info}")
                    user_input = input()
                    response = self.input_control_required_data(user_input)
            # Contrôle date
            elif updated_info == "birth_date":
                response = self.validate(user_input)
                while response is False and user_input != "r":
                    MenuViews.date_error()
                    MenuViews.input_text(f"la nouvelle valeur {french_updated_info}")
                    user_input = input()
                    response = self.validate(user_input)
            # Contrôle genre
            elif updated_info == "gender":
                length_menu = 0
                valid_strings = ["M", "F", "r"]
                response = self.input_validation(user_input, length_menu, valid_strings)
                while response is False:
                    MenuViews.input_error()
                    MenuViews.input_text(f"la nouvelle valeur {french_updated_info}")
                    user_input = input()
                    response = self.input_validation(user_input, length_menu, valid_strings)
            # Contrôle rang
            elif updated_info == "rank":
                length_menu = 10000
                valid_strings = ["r"]
                response = self.input_validation(user_input, length_menu, valid_strings)
                while response is False:
                    MenuViews.input_error()
                    MenuViews.input_text(f"la nouvelle valeur {french_updated_info}")
                    user_input = input()
                    response = self.input_validation(user_input, length_menu, valid_strings)
            # Retour
            elif user_input == "r":
                self.main_menu_start()

            # Modification en base
            p.update_player_db(user_input, updated_info)
            MenuViews.player_saved()
            self.update_player()

    def reports_menu(self):
        """Menu des Rapports"""
        MenuViews.reports_menu()
        MenuViews.input_option()
        user_input = input()

        # Contrôle de saisie
        length_menu = 5
        valid_strings = ["r"]
        response = self.input_validation(user_input, length_menu, valid_strings)
        while response is False:
            MenuViews.input_error()
            MenuViews.input_option()
            user_input = input()
            response = self.input_validation(user_input, length_menu, valid_strings)

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

        MenuViews.other_report()
        user_input = input()
        # Contrôle de saisie
        length_menu = 0
        valid_strings = ["o", "n"]
        response = self.input_validation(user_input, length_menu, valid_strings)
        while response is False:
            MenuViews.input_error()
            MenuViews.other_report()
            user_input = input()
            response = self.input_validation(user_input, length_menu, valid_strings)

        if user_input == "o":
            self.reports_menu()
        elif user_input == "n":
            self.main_menu_start()

    def player_reports_sorting(self, players):
        """
        Sélectionne un tri des joueurs par nom ou par rang
        @paramètres "players" : liste des joueurs
        """
        MenuViews.reports_player_sorting()
        MenuViews.input_option()
        user_input = input()
        # saisie obligatoire et cohérence
        length_menu = [1, 2]
        valid_strings = ["r"]
        result = self.input_validation(user_input, length_menu, valid_strings)
        while result is False:
            MenuViews.input_error()
            MenuViews.input_option()
            user_input = input()
            result = self.input_validation(user_input, length_menu, valid_strings)
        # Joueurs triés par nom
        if user_input == "1":
            self.reports_control.all_players_name(players)
        # Joueurs triés par rang
        elif user_input == "2":
            self.reports_control.all_players_rank(players)
        # Retour
        elif user_input == "r":
            self.main_menu_start()
        """
        # else:
        if len(players) == 8:
            MenuViews.input_error()
            self.player_reports_sorting(players)
        else:
            MenuViews.input_error()
            self.player_reports_sorting(Player.load_player_db())
        """
    @staticmethod
    def input_control_required_data(user_input):
        """Saisie touche Entrée non autorisée
        """
        if user_input == '':
            response = False
        else:
            response = True
        return response

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

    @staticmethod
    def input_validation(user_input, len_limit, valid_strings):
        """
        Détermine si "user_input" est une valeur "numérique" ou "chaine" valide
        @return = "True" ou "False"
        """
        response = user_input.isdigit()
        if response is True:
            if type(len_limit) is not list:
                valid_int = []
                for i in range(len_limit):
                    i += 1
                    valid_int.append(i)
            else:
                valid_int = len_limit
            # saisie présente dans la liste des entiers autorisés ?
            if int(user_input) in valid_int:
                result = True
            else:
                result = False
        else:
            # saisie présente dans la liste des caractères autorisés ?
            if user_input in valid_strings:
                result = True
            else:
                result = False

        return result

    @staticmethod
    def validate(date):
        try:
            datetime.datetime.strptime(date, '%d/%m/%Y')
            response = True
        except ValueError:
            response = False
        return response
