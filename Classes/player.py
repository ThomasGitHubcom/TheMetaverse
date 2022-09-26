import time
import random

from Classes.config import Config

class Player :

    def __init__(self, name, life, money):
        """
        PARAM : - name : str
                - life : float
                - money : float
        initialisate team to empty list, game and direction to None
        """
        self.name = name
        self.life = life
        self.strength = 1
        self.money = money
        self.team = []
        self.game = None
        self.direction = None

    @property
    def is_alive(self):
        return self.life > 0


    def get_hit(self, damages):
        """
        PARAM : - damages : float
        Take the damage to life
        """
        if self.life-damages >= 0:
            self.life -= damages
        else:
            self.life = 0


    def new_character(self):
        """
        Ask to player choose and where add a new Character,
        check if enough monney
        and create the new one
        """
        line = ""
        if self.game.game_type == "solo" and self.game.player_turn == 1:
            targets = []
            lines_free = []
            lines_support = []
            lines_dangerous = []
            characters_available = {}
            for game_line in range(self.game.nb_lines):
                target = None
                line_free = True
                support_exist = False
                character_number_opp = 0
                character_number_me  = 0
                for game_col in range(self.game.nb_columns):
                    character = self.game.get_character_at((game_line,game_col))
                    if character is not None:
                        line_free = False
                        if character not in self.team:
                            target = character
                            character_number_opp += 1
                        else:
                            character_number_me += 1
                            if Config.AVAILABLE_CHARACTERS["H"] == character:
                                support_exist = True

                if line_free:
                    lines_free.append(str(game_line))
                if character_number_me > 0 and support_exist == False:
                    lines_support.append(str(game_line))
                if character_number_me-character_number_opp <= -3:
                    lines_dangerous.append(str(game_line))
                if character_number_opp-character_number_me == 0 and target != None:
                    targets.append(target)
            
            for key, value in Config.AVAILABLE_CHARACTERS.items():
                if self.money >= value.base_price and key != "H":
                    characters_available[key] = value
            
            if characters_available != {}:
                protect = False
                if lines_dangerous != []:
                    line = random.choice(lines_dangerous)
                    character = random.choice(list(characters_available))[0]
                if self.life-3 > self.game.players[1].life and self.money >= 9:
                    if lines_support != [] and random.randint(0, 1) == 1:
                        character = "H"
                        line = random.choice(lines_support)
                else:
                    protect = True
                if targets != [] and line == "" and protect == True:
                    target_current = None
                    target_position_from_base = self.game.nb_columns
                    for target in targets:
                        if target_current == None or (self.game.nb_columns-target.position[1] < target_position_from_base) :
                            target_current = target
                            target_position_from_base = self.game.nb_columns-target.position[1]
                    for key, value in characters_available.items():
                            if target_current.life == value.base_life:
                                line = str(target.position[0])
                                character = key
                if random.randint(0, 2) == 1 and line == "":
                    line = str(random.randint(0, self.game.nb_lines-1))
                    character = random.choice(list(characters_available))[0]
        elif self.game.game_type == "auto":
            if len(self.game.history) >= 1:
                action = self.game.history[0]
                if "," in action:
                    action_split = action.split(",")
                    character = action_split[0]
                    line = str(action_split[1])
                self.game.history.pop(0)
            time.sleep(0.3)
        else:
            print(f"\n {self.name}: Wich character do you want to add ? (enter if none) ")
            for key, character in Config.AVAILABLE_CHARACTERS.items():
                print(f"    {key}) ", character.summary())
            try:
                character = input("\n I want to add : ").upper()
                if character in Config.AVAILABLE_CHARACTERS:
                    line = input(f"\n {self.name}: Wich line would you place the new one (0-{self.game.nb_lines-1}) ? (enter if none) ")
            except KeyboardInterrupt:
                panel.main()
        current_action = ""
        if line != "" and line.isdecimal() and len(line) == 1:
            line = int(line)
            if 0<=line<=self.game.nb_lines-1 :
                if self.money >= Config.AVAILABLE_CHARACTERS[character].base_price :
                    column = 0 if self.direction == 1 else self.game.nb_columns-1
                    Config.AVAILABLE_CHARACTERS[character](self,(line,column))
                    current_action = f"{character},{line}"
        if self.game.game_type != "auto":
            self.game.history.append(current_action)