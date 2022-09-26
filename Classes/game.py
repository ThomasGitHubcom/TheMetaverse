import os

from Classes.config import Config
from Classes.player import Player
from Classes.character import *

if 'colorama' not in Config.required_modules:
    from colorama import init, Back, Fore, Style
    init()

class Game :

    def __init__(self,player0, player1, nb_lines=6,nb_columns=15, game_type="multi", game_history=None):
        """
        PARAM : - player0 : Player
                - player1 : Player
                - nb_lines : float
                - nb_columns : float
                - game_type : string [solo / multi / auto]
        - update players' direction and game
        - initialisate player_turn to 0
        """
        self.game_type = game_type
        self.nb_lines = nb_lines
        self.nb_columns = nb_columns
        self.players = [player0,player1]
        self.player_turn = 0
        self.players[0].direction = 1
        self.players[1].direction = -1
        self.players[0].game = self
        self.players[1].game = self
        if self.game_type == "solo":
            self.players[0].score = 0
            self.players[1].score = 0
        if self.game_type == "auto":
            self.history = game_history
        else:
            self.history = []


    @property
    def current_player(self):
        return self.players[self.player_turn]

    @property
    def oponent(self):
        return self.players[1-self.player_turn]

    @property
    def all_characters(self):
        return self.players[0].team + self.players[1].team

    @property
    def winner(self):
        if self.players[0].is_alive and not self.players[1].is_alive:
            return self.players[0]
        elif self.players[1].is_alive and not self.players[0].is_alive:
            return self.players[1]
        else:
            return None

    @property
    def loser(self):
        if self.players[0].is_alive and not self.players[1].is_alive:
            return self.players[1]
        elif self.players[1].is_alive and not self.players[0].is_alive:
            return self.players[0]
        else:
            return None


    def get_character_at(self, position):
        """
        PARAM : - position : tuple
        RETURN : character at the position, None if there is nobody
        """
        for character in self.all_characters:
            if character.position == position:
                return character
        return None


    def place_character(self, character, position):
        """
        Place character to position if possible
        PARAM : - character : Character
                - position : tuple
        RETURN : bool to say if placing is done or not
        """
        if self.get_character_at(position) is None and not ((position[1] == -1 and character.direction == -1) or 
        (position[1] == self.nb_columns and character.direction == 1)) :
            character.position = position
            return True
        return False



    def draw(self):
        """
        print the board
        """
        lines_space = self.nb_lines*5
        self.clear()
        print("")
        print(" "*lines_space, end="")
        if 'colorama' not in Config.required_modules:
            print(f"{Style.BRIGHT}{Fore.RED}{self.players[0].life:<4}{'  '*self.nb_columns}{self.players[1].life:>4}{Fore.RESET}{Style.RESET_ALL}")
        else:
            print(f"{self.players[0].life:<4}{'  '*self.nb_columns}{self.players[1].life:>4}")
        print(" "*lines_space, end="")
        print("----"+self.nb_columns*"--"+"----")

        for line in range(self.nb_lines):
            print(" "*lines_space, end="")
            print(f"|{line:>2}|", end="")
            for col in range(self.nb_columns):
                character = self.get_character_at((line,col))
                if character is None:
                    print(".", end=" ")
                else:
                    if 'colorama' not in Config.required_modules:
                        if character.life == character.base_life:
                            print(f"{Fore.GREEN}{character.design} {Fore.RESET}", end="")
                        elif character.life > character.base_life/2:
                            print(f"{Fore.YELLOW}{character.design} {Fore.RESET}", end="")
                        else:
                            print(f"{Fore.RED}{character.design} {Fore.RESET}", end="")
                    else:
                        print(f"{character.design} ", end="")
            print(f"|{line:<2}|")
        print(" "*lines_space, end="")
        print("----"+self.nb_columns*"--"+"----")
        print(" "*lines_space, end="")
        if 'colorama' not in Config.required_modules:
            print(f"{Fore.YELLOW}${self.players[0].money}{'  '*(self.nb_columns+1)}${self.players[1].money}{Fore.RESET}")
        else:
            print(f"${self.players[0].money:<3}{'  '*self.nb_columns}${self.players[1].money:>3}")


    def play_turn(self):
        """
        play one turn :
            - current player can add a new character
            - current player's character play turn
            - oponent player's character play turn
            - draw the board
        """
        Player.new_character(self.current_player)
        for character in self.current_player.team:
            character.play_turn()
        for character in self.oponent.team:
            character.play_turn()
        self.draw()

    def clear(self):
        """
        clear the console
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def play(self):
        """
        play an entire game : while players is alive and have money or team , play a turn and change player turn
        """
        self.clear()
        self.draw()
        while self.players[0].is_alive and self.players[1].is_alive and (self.players[0].team != [] or
        self.players[1].team != [] or self.players[0].money > 1 or self.players[1].money > 1):
            self.play_turn()
            self.player_turn = 1-self.player_turn
        self.clear()