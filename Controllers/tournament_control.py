from datetime import datetime
from Models.player import Player
from Models.round import Round
from Views.round import RoundViews
from Views.menu import MenuViews


class TournamentController:

    def __init__(self):
        self.menu_view = MenuViews()
        self.round_view = RoundViews()
        self.timer = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def start_tournament(self, tournament):
        """Tournoi (t) = données du tournoi
        Débute par le premier round ou par le chargement du round en cours
        Enregistre le temps (y/m/d-h-m-s) des débuts et fin de rounds.
        """
        if tournament.current_round == 1:
            tournament.date = self.timer
            tournament.update_timer(tournament.date, 'date')

            self.first_round(tournament)
            tournament.current_round += 1
            tournament.update_tournament_db()

            while tournament.current_round <= tournament.nb_rounds:
                self.next_round(tournament)
                tournament.current_round += 1
                tournament.update_tournament_db()

        elif 1 < tournament.current_round <= tournament.nb_rounds:
            while tournament.current_round <= tournament.nb_rounds:
                self.next_round(tournament)
                tournament.current_round += 1
                tournament.update_tournament_db()

            tournament.end_date = self.timer
            tournament.update_timer(tournament.end_date, 'end_date')
            self.tournament_end(tournament)

        elif tournament.current_round > tournament.nb_rounds:
            self.tournament_end(tournament)

    def first_round(self, tournament):
        """
            Premier round : top players contre down players
            Construction des matches par rangs
        """
        round_x = Round("Round 1", self.timer, "Non terminé")
        tournament.sort_players_by_rang()
        top_players, down_players = tournament.split_players()
        self.round_view.round_header(tournament, round_x.start_datetime)

        for i in range(tournament.nb_rounds):
            round_x.get_match_pairing(top_players[i], down_players[i])
            top_players[i], down_players[i] = self.update_opponents(top_players[i], down_players[i])

        self.round_view.display_matches(round_x.matches)

        self.round_view.round_over()
        self.menu_view.input_option()
        user_input = input().lower()
        scores_list = []
        # cohérence saisie
        while user_input not in str(["o", "r"]) or user_input == '':
            self.round_view.round_over()
            self.menu_view.input_option()
            user_input = input().lower()
        if user_input == "o":
            round_x.end_datetime = self.timer
            tournament.rounds.append(round_x.set_round())
            tournament.merge_players(top_players, down_players)

            self.end_round(scores_list, tournament)

        elif user_input == "r":
            self.back_to_menu()

    def next_round(self, tournament):
        """
        Rounds suivants et construction des matches par scores
        """
        round_x = Round(("Round " + str(tournament.current_round)), self.timer, "Non terminé")
        tournament.sort_players_by_score()
        self.round_view.round_header(tournament, round_x.start_datetime)

        players_without_match = tournament.players
        players_with_match = []

        n = 0
        while n < tournament.nb_rounds:
            if players_without_match[1]["id"] in players_without_match[0]["opponents"]:
                try:
                    players_without_match, players_with_match = self.match_other_option(players_without_match,
                                                                                        players_with_match, round_x)
                    tournament.players = players_with_match

                except IndexError:
                    players_without_match, players_with_match = self.match_main_option(players_without_match,
                                                                                       players_with_match, round_x)
                    tournament.players = players_with_match

            elif players_without_match[1]["id"] not in players_without_match[0]["opponents"]:
                players_without_match, players_with_match = self.match_main_option(players_without_match,
                                                                                   players_with_match, round_x)
                tournament.players = players_with_match

            n += 1

        self.round_view.display_matches(round_x.matches)

        self.round_view.round_over()
        self.menu_view.input_option()
        user_input = input().lower()
        scores_list = []
        # cohérence saisie
        while user_input not in str(["o", "r"]) or user_input == '':
            self.round_view.round_over()
            self.menu_view.input_option()
            user_input = input().lower()
        if user_input == "o":
            round_x.end_datetime = self.timer
            tournament.rounds.append(round_x.set_round())
            self.end_round(scores_list, tournament)

        elif user_input == "r":
            self.back_to_menu()

    def match_main_option(self, players_without_match, players_with_match, round_x):
        """Option de match par défaut
        Paramètre players_without_match : liste de joueurs sans match attribué dans le round courant
        Paramètre players_with_match : liste de joueurs avec match attribué dans le round courant
        Paramètres r : round courant
        Retour : listes modifiées
        """
        round_x.get_match_pairing(players_without_match[0], players_without_match[1])
        players_without_match[0], players_without_match[1] = self.update_opponents(players_without_match[0],
                                                                                   players_without_match[1])

        players_without_match, players_with_match = self.update_player_lists(
            players_without_match[0],
            players_without_match[1],
            players_without_match,
            players_with_match
        )

        return players_without_match, players_with_match

    def match_other_option(self, players_without_match, players_with_match, round_x):
        """Option alternative de match
        Paramètre players_without_match : liste de joueurs sans match attribué dans le round courant
        Paramètre players_with_match : liste de joueurs avec match attribué dans le round courant
        Paramètres r : round courant
        Retour : listes modifiées
        """
        round_x.get_match_pairing(players_without_match[0], players_without_match[2])
        players_without_match[0], players_without_match[2] = self.update_opponents(players_without_match[0],
                                                                                   players_without_match[2])

        players_without_match, players_with_match = self.update_player_lists(
            players_without_match[0],
            players_without_match[2],
            players_without_match,
            players_with_match
        )

        return players_without_match, players_with_match

    def end_round(self, scores_list: list, tournament):
        """Fin de round : récuoères les scores

        @paramètres tournament : liste infos tournoi
        @paramètres scores_list : liste des scores
        @return : liste joueurs avec scores
       """
        for i in range(tournament.nb_rounds):
            self.round_view.score_options(i + 1)

            response = self.input_scores_verification()
            scores_list = self.get_score(response, scores_list)

        tournament.players = self.update_scores(tournament.players, scores_list)

        return tournament.players

    def get_score(self, response, scores_list: list):
        """Saisie des scores pour chaque match du round courant

        @paramètres "response" : saisie score du match (0, 1 ou 2)
        @paramètres "scores_list": liste des scores
        @return : Liste des scores saisis
        """
        if response == "0":
            scores_list.extend([0.5, 0.5])
            return scores_list
        elif response == "1":
            scores_list.extend([1.0, 0.0])
            return scores_list
        elif response == "2":
            scores_list.extend([0.0, 1.0])
            return scores_list
        elif response == "r":
            self.back_to_menu()

    @staticmethod
    def update_scores(players, scores_list: list):
        """Mise à jour des scores de la liste joueur

        @paramètres "players" : liste des joueurs
        @paramètres "scores_list" : liste des scores
        @return : liste des joueurs avec scores mis à jour
        """
        for i in range(len(players)):
            players[i]["score"] += scores_list[i]

        return players

    @staticmethod
    def update_player_lists(player_1, player_2, players_without_match, players_with_match):
        """Mise à jour des listes de joueurs avec ou sans match atrribué:
        Paramètre "player_1" : joueur 1 (dict)
        Paramètre "player_2" : joueur 2 (dict)
        Paramètre "players_without_match" : liste de joueurs sans match attribué dans le round courant
        Paramètre "players_with_match" : liste de joueurs avec match attribué dans le round courant
        @Return : listes modifiées
        """
        players_with_match.extend([player_1, player_2])
        players_without_match.remove(player_1)
        players_without_match.remove(player_2)

        return players_without_match, players_with_match

    @staticmethod
    def update_opponents(player_1, player_2):
        player_1["opponents"].append(player_2["id"])
        player_2["opponents"].append(player_1["id"])

        return player_1, player_2

    def tournament_end(self, tournament):
        """Fin de tournoi : Affiche le résultat final
        Possibilité de modifier les rangs
        @paramètre "tournament" : tournoi courant (dict)
        """
        tournament.sort_players_by_rang()
        tournament.sort_players_by_score()

        self.round_view.display_results(tournament)

        self.menu_view.update_rank()
        user_input = input()

        players = tournament.players
        # Cohérence saisie
        while user_input not in str(["o", "n", "r"]) or user_input == '':
            self.menu_view.update_rank()
            user_input = input()

        if user_input == "n":
            self.back_to_menu()

        elif user_input == "o":
            while True:
                self.update_ranks(players)

    def update_ranks(self, players):
        """Modifie les rangs

        @paramètres "players": Liste des joueurs du tournoi
        """
        self.menu_view.select_players(players, "à modifier")
        self.menu_view.input_option()
        user_input = input()
        # Cohérence saisie
        id_players = []
        for i in range(len(players)):
            id_players.append(players[i]['id'])
            if isinstance(user_input, (int, float)):
                int_user_input = int(user_input)
                while int_user_input not in id_players or int_user_input == 0:
                    self.menu_view.input_option()
                    user_input = input()
                    int_user_input = int(user_input)
        if user_input == "r":
            self.back_to_menu()

        for i in range(len(players)):
            if int(user_input) == players[i]["id"]:
                p = players[players.index(players[i])]
                p = Player(
                    p['id'],
                    p['last_name'],
                    p['first_name'],
                    p['birth_date'],
                    p['gender'],
                    p['rank']
                )

                self.menu_view.rank_update_header(p)
                self.menu_view.input_text("un nouveau rang")
                user_input = input()

                if user_input == "r":
                    self.back_to_menu()

                else:
                    p.update_player_db(int(user_input), "rank")
                    players[i]["rank"] = int(user_input)

                    return players

    @staticmethod
    def back_to_menu():
        from Controllers.menu_control import MenuController
        MenuController().main_menu_start()

    def input_scores_verification(self):
        """
        Verifie la cohérence de la saisie scores
        retour response : réponse saisie utilisateur
        """
        self.round_view.score_input_option()
        response = input()
        while response not in str([0, 1, 2, "r"]) or response == '':
            self.menu_view.input_error()
            self.round_view.score_input_option()
            response = input()
        return response
