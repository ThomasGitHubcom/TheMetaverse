import os
import json
import datetime

from Classes.game import Game
from Classes.sound import Sound
from Classes.player import Player
from Classes.config import Config
from Classes.history import History

if 'requests' not in Config.required_modules:
    import requests

if 'colorama' not in Config.required_modules:
    from colorama import init, Back, Fore, Style
    init()

class Gui :

    def __init__(self):
        """
        Initialize the menu
        """
        self.nb_lines = int(Config.get("nb_lines", 30))
        self.nb_columns = int(Config.get("nb_columns", 120))

    @classmethod
    def title(cls, text):
        if os.name == 'nt':
            os.system(f'title {text}')

    @classmethod
    def clear(cls):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def logo(self):
        """
        Prints the game logo
        """
        lines_space = ((self.nb_columns-65)//2)-2
        Gui.clear()
        print((" "*lines_space)+"  _______ _                           _                                 ")
        print((" "*lines_space)+" |__   __| |                         | |                                ")
        print((" "*lines_space)+"    | |  | |__   ___   _ __ ___   ___| |_ __ ___   _____ _ __ ___  ___  ")
        print((" "*lines_space)+"    | |  | '_ \ / _ \ | '_ ` _ \ / _ \ __/ _` \ \ / / _ \ '__/ __|/ _ \ ")
        print((" "*lines_space)+"    | |  | | | |  __/ | | | | | |  __/ || (_| |\ V /  __/ |  \__ \  __/ ")
        print((" "*lines_space)+"    |_|  |_| |_|\___| |_| |_| |_|\___|\__\__,_| \_/ \___|_|  |___/\___| ")
        print("")

    def create_selection(self, options, space_at_last_line=False, sound="button"):
        """
        Ask the player to choose an option
        PARAM : - options : array
                - space_at_last_line : boolean
                - sound : string
        RETURN : a number corresponding to an option
        """
        for i in range(len(options)):
            if space_at_last_line and len(options) == i+1 :
                print("")
            if 'colorama' in Config.required_modules:
                print((" "*((self.nb_columns-(3+len(options[i])))//2))+f"{i+1}) {options[i]}")
            else:
                if Fore.RESET in options[i]:
                    print((" "*((self.nb_columns-(3+len(options[i])-10))//2))+f"{i+1}) {options[i]}")
                else:
                    print((" "*((self.nb_columns-(3+len(options[i])))//2))+f"{i+1}) {options[i]}")
        if options != ['Play again', 'Return to menu']:
            print("\n"*(((5-len(options))-space_at_last_line)+self.nb_lines//5))
        print(" "*((self.nb_columns-65)//2), end="")
        choice = input("I want to ")
        if sound != None and choice != "":
            if sound == "button":
                if options[-1] == "Back" and choice.isdecimal():
                    if int(choice) == len(options):
                        Sound.play("button_back")
                    else:
                        Sound.play("button")
                else:
                    Sound.play("button")
            else:
                Sound.play(sound)
        return choice


    def main(self):
        """
        Display the main menu
        """
        Gui.title('The Metaverse')
        os.system(f'mode con:cols={self.nb_columns} lines={self.nb_lines}')
        Sound.play("main")
        self.logo()

        history = History.get()

        if history == []:
            choice = self.create_selection(['Start a new game', 'Option', 'Quit'], True)
        else:
            choice = self.create_selection(['Start a new game', 'Show History', 'Option', 'Quit'], True)

        if choice == "1" :
            self.game()
        elif choice == "2" :
            if history == []:
                self.setting()
            else:
                self.auto()
        elif choice == "3":
            if history == []:
                exit()
            else:
                self.setting()
        elif choice == "4" and history != []:
            exit()
        else :
            self.main()

    def setting(self):
        """
        Displays the available settings
        """
        Gui.title('The Metaverse - Settings')
        self.logo()
        try:
            selection = ['Game Size']
            if 'pygame' not in Config.required_modules:
                selection.append('Game Sound')
            if Config.get("username", "") != "":
                selection.append('Change Username')
            selection.append('Back')

            choice = self.create_selection(selection, True)
            if choice.isdecimal():
                choice = int(choice)-1
                if choice >= 0 and choice <= len(selection)-1:
                    if selection[choice] == 'Game Size':
                        self.setting_size()
                    elif selection[choice] == 'Game Sound':
                        self.setting_sound()
                    elif selection[choice] == 'Change Username':
                        self.setting_username()
                    elif selection[choice] == 'Back':
                        self.main()
            self.setting()
        except KeyboardInterrupt:
            self.main()

    def setting_username(self, setting=True):
        """
        PARAM : - setting : Boolean
        - Request the user's pseudo and save it in the configuration file
        """
        if setting:
            Gui.title('The Metaverse - Settings - Username')

        username = Config.get("username", "")
        if username == "":
            text = "Your username : "
        else:
            text = f"Username ({username}) : "

        new_username=""
        while new_username == "" :
            Gui.clear()
            self.logo()
            new_username = input((" "*((self.nb_columns-(len(text)+4))//2))+text).replace(" ", "")

        Config.save("username", new_username)

        if setting:
            self.setting()

    def setting_sound(self):
        """
        Displays the parameters related to the sounds
        """
        Gui.title('The Metaverse - Settings - Sound')
        self.logo()

        sound_status = Config.get("sound", "On")
        sound_theme_status = Config.get("sound_theme", "On")
        if 'colorama' not in Config.required_modules:
            choice = self.create_selection(
                [
                    f'Theme Song [{f"{Fore.GREEN}" if sound_theme_status == "On" else f"{Fore.RED}"}{sound_theme_status}{Fore.RESET}]',
                    f'Sound Effect [{f"{Fore.GREEN}" if sound_status == "On" else f"{Fore.RED}"}{sound_status}{Fore.RESET}]',
                    'Back'
                ], True, None
                )
        else:
            choice = self.create_selection([f'Theme Song [{sound_theme_status}]',f'Sound Effect [{sound_status}]','Back'], True, None)

        if choice == "1" :
            if sound_theme_status == "On":
                Config.save("sound_theme", "Off")
                Sound.fadeout(1000)
            else:
                Config.save("sound_theme", "On")
                Sound.play("main")
        elif choice == "2" :
            if sound_status == "On":
                Config.save("sound", "Off")
            else:
                Config.save("sound", "On")
                Sound.play("on")
        elif choice == "3" :
            Sound.play("button_back")
            self.setting()
        self.setting_sound()
        Sound.play("button")

    def setting_size(self):
        """
        Displays the parameters related to the size
        """
        Gui.title('The Metaverse - Settings - Size')
        self.logo()

        choice = self.create_selection(['Small', 'Medium', 'Large', 'Back'], True)

        if choice == "1" :
            self.nb_lines=Config.save("nb_lines", 20)
            self.nb_columns=Config.save("nb_columns", 80)
        elif choice == "2" :
            self.nb_lines=Config.save("nb_lines", 30)
            self.nb_columns=Config.save("nb_columns", 120)
        elif choice == "3" :
            self.nb_lines=Config.save("nb_lines", 40)
            self.nb_columns=Config.save("nb_columns", 130)
        elif choice == "4" :
            self.setting()
        os.system(f'mode con:cols={self.nb_columns} lines={self.nb_lines}')
        self.setting_size()

    def game(self):
        """
        Displays the game selection
        """
        Gui.title('The Metaverse - Game mode')
        self.logo()

        choice = self.create_selection(['Solo', 'Multi', 'Back'])

        if choice == "1" :
            self.solo()
        elif choice == "2" :
            self.multi()
        elif choice == "3" :
            self.main()
        else:
            self.game()

    def leaderboard(self):
        """
        Displays the leaderboard
        """
        if 'requests' not in Config.required_modules:
            data = []
            print("")
            try:
                uuid = Config.get("uuid", "")
                r = requests.get('https://themetaverseapi.pages.dev/?uuid='+uuid, timeout=5)
                if r.status_code == 200:
                    data = json.loads(r.text)
                    if data['status'] == 'success':
                        data = data['data']
                        for player in data:
                            text = player['username']+" : "+str(player['score'])
                            if 'colorama' not in Config.required_modules and player['you'] == True:
                                text = f"{Style.BRIGHT}{text}{Style.RESET_ALL}"
                                print((" "*((self.nb_columns-(len(text)-8))//2))+text)
                            else:
                                print((" "*((self.nb_columns-len(text))//2))+text)
            except:
                pass
            print("\n"*(4-len(data)))
    
    def solo(self, p1=""):
        """
        Start a single player game
        """
        Gui.title('The Metaverse - Solo mode')
        if Config.get("username", "") == "":
            self.setting_username(False)
        p1 = Config.get("username")
        p2 = "Computer"
        if 'pygame' not in Config.required_modules:
            Sound.fadeout(500)
        Gui.title(f'The Metaverse - {p1} vs {p2}')
        game = Game(Player(p1, 20, 20), Player(p2, 20, 20), self.nb_lines//5,self.nb_columns//5, "solo")
        Sound.play("start")
        game.play()
        self.result(game)

    def multi(self, p1="", p2=""):
        """
        Start a multiplayer game
        """
        Gui.title('The Metaverse - Multi mode')
        while p1 == "" :
            Gui.clear()
            self.logo()
            p1 = input((" "*((self.nb_columns-20)//2))+"Player 1 name : ").replace(" ", "")
        while p2 == "" :
            Gui.clear()
            self.logo()
            p2 = input((" "*((self.nb_columns-20)//2))+"Player 2 name : ").replace(" ", "")
        if 'pygame' not in Config.required_modules:
            Sound.fadeout(500)
        Gui.title(f'The Metaverse - {p1} vs {p2}')
        game = Game(Player(p1, 20, 15), Player(p2, 20, 15), self.nb_lines//5,self.nb_columns//5)
        Sound.play("start")
        game.play()
        self.result(game)

    def auto(self):
        """
        Starts an automatic game
        """
        Gui.title('The Metaverse - History')
        self.logo()

        history = History.get()
        menu = []
        for game in history:
            menu.append(game['title'].capitalize())
        menu.append('Back')
        choice = self.create_selection(menu, True)
        if choice != "" and choice.isnumeric():
            if menu[int(choice)-1] != "Back":
                history = history[int(choice)-1]
                players = history['players']
                Sound.fadeout(500)
                Gui.title(f'The Metaverse - {players[0]} vs {players[1]}')
                lines = self.nb_lines//5
                columns = self.nb_columns//5
                game = Game(Player(players[0], 20, 10), Player(players[1], 20, 10), lines, columns, "auto", history['history'])
                game.play()
                Sound.play("main")
            else:
                self.main()
        self.auto()

    def result(self, game, first=True):
        """
        Displays the game result
        """
        Gui.clear()
        Gui.title('The Metaverse - Result')
        self.logo()
        if game.winner is None :
            print((" "*((self.nb_columns-10)//2))+"Equality !")
        else:
            if game.game_type != "auto" and first:
                History.save(game.game_type, (game.players[0].name,game.players[1].name), game.history)
            if game.game_type == "solo" :
                if game.winner == game.players[0]:
                    if first:
                        Sound.play("win")
                    print((" "*((self.nb_columns-9)//2))+"You win !")
                    if 'requests' not in Config.required_modules and first:
                        uuid = Config.get("uuid", "")
                        if uuid == "":
                            import uuid
                            uuid = str(uuid.uuid4())
                            Config.save("uuid", uuid)
                        try:
                            requests.post('https://themetaverseapi.pages.dev/',
                                data={
                                    'username':game.winner.name,
                                    'score':game.winner.score,
                                    'uuid':uuid,
                                    'lines':Config.get("nb_lines"),
                                    'columns':Config.get("nb_columns", 120)
                                }
                            )
                        except:
                            pass
                else:
                    if first:
                        Sound.play("lose")
                    print((" "*((self.nb_columns-10)//2))+"You lost !")
                
                self.leaderboard()
            else:
                print((" "*((self.nb_columns-(7+len(game.winner.name)))//2))+f"{game.winner.name} wins !")
        print("")

        choice = self.create_selection(['Play again', 'Return to menu'])

        if choice == "1" :
            if game.game_type == "solo":
                self.solo(game.players[0].name)
            else:
                self.multi(game.players[0].name, game.players[1].name)
        elif choice == "2" :
            self.main()
        else:
            self.result(game, False)