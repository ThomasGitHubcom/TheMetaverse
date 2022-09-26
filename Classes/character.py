from Classes.sound import Sound
from Classes.config import Config

AVAILABLE_CHARACTERS = {}

class Character :

    base_price = 1
    base_life = 5
    base_strength = 1 
    base_characters = [">","<"]

    def __init__(self, player, position):
        """
        PARAM : - player : Player
                - position : tuple
        Set player to player in param.
        Set life, strength and price to base_life, base_strength and base_price.
        Place th character at the position
        If OK : add the current character to the player's team and take the price
        """
        self.player = player
        self.life = self.base_life
        self.strength = self.base_strength
        self.price = self.base_price
        self.characters = self.base_characters

        ok = self.game.place_character(self, position)
        if ok :
            self.player.team.append(self)
            self.player.money -= self.price


    @property
    def direction(self):
        return self.player.direction

    @property
    def game(self):
        return self.player.game

    @property
    def enemy(self):
        if self.game.players.index(self.player) == 1:
            return self.game.players[0]
        else:
            return self.game.players[1]

    @property
    def design(self):
        if self.direction == 1 :
            return self.characters[0]
        else :
            return self.characters[1]

    @classmethod
    def summary(cls):
        name = cls.__name__.replace("Character_", "")
        return f'{"A" if name[0] not in "aeiouy" else "An"} {name} '+" "*(9-len(name))+f' ({cls.base_price}$) - Life : '+" "*(2-len(str(cls.base_life)))+f'{cls.base_life} Strength: {cls.base_strength}'

    def move(self):
        """
        the character move one step front
        """
        self.game.place_character(self,(self.position[0], self.position[1]+self.direction))


    def get_hit(self, damages):
        """
        Take the damage to life. If dead, the character is removed from his team and return reward
        PARAM : damages : float
        RETURN : the reward due to hit (half of price if the character is killed, 0 if not)
        """
        self.life -= damages
        if self.life <= 0 :
            self.player.team.remove(self)
            return self.price/2
        return 0


    def attack(self):
        """
        Make an attack :
            - if in front of ennemy's base : hit the base and get damages from it
            - if in front of character : hit him (and get reward)
        """
        if (self.position[1] == 0 and self.direction == -1) or (self.position[1] == self.game.nb_columns-1 and self.direction == 1) :
            self.enemy.get_hit(self.strength)
            self.get_hit(self.enemy.strength)
            if self.player.game.game_type == "solo":
                self.player.score += self.strength
            Sound.play("attack")
        else :
            character = self.game.get_character_at((self.position[0], self.position[1]+self.direction))
            if character is not None and character.player != self.player :
                self.player.money += character.get_hit(self.strength)
                if self.player.game.game_type == "solo":
                    self.player.score += self.strength
                Sound.play("punch")


    def play_turn(self):
        """
        play one turn : move and attack
        """
        self.move()
        self.attack()


    def __str__(self):
        """
        return a string represent the current object
        """
        return f"{self.design} ({self.price:>2}$) - vie : {self.life:>2} - force : {self.strength:>2}"
AVAILABLE_CHARACTERS["C"] = Character

class Character_Fighter(Character):
    base_price = 2
    base_life = 5
    base_strength = 2
    base_characters = [")","("]
AVAILABLE_CHARACTERS["F"] = Character_Fighter

class Character_Tank(Character):
    base_price = 3
    base_life = 10
    base_strength = 1
    base_characters = ["]","["]

    def __init__(self, player, position):
        super().__init__(player, position)
        self.turn_to_move = False

    def move(self):
        """
        the character move one step front in 1 of 2 rounds
        """
        if self.turn_to_move :
            super().move()
            self.turn_to_move = False
        else :
            self.turn_to_move = True
AVAILABLE_CHARACTERS["T"] = Character_Tank

class Character_Duck(Character):
    base_price = 5
    base_life = 2
    base_strength = 5
    base_characters = ["/","\ ".replace(" ","")]
AVAILABLE_CHARACTERS["D"] = Character_Duck

class Character_Healer(Character):
    base_price = 2
    base_life = 2
    base_strength = 1
    base_characters = ["#","#"]

    def move(self):
        """
        the character move one step front and heal a character if behind him
        """
        super().move()
        character = self.game.get_character_at((self.position[0], self.position[1]+self.direction))
        if character is not None and character.player == self.player:
            base_life = character.__class__.base_life
            if base_life > character.life :
                character.life += round((base_life/100)*20)
                self.get_hit(1)
AVAILABLE_CHARACTERS["H"] = Character_Healer

Config.AVAILABLE_CHARACTERS = AVAILABLE_CHARACTERS