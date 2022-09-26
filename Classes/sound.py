import os
import random

from Classes.config import Config

if 'pygame' not in Config.required_modules:
    from pygame import mixer
    mixer.init()



class Sound :


    file_dir = "Sounds/"

    @classmethod
    def play(cls, name):
        """
        PARAM : - name : string
        Play a sound
        """

        if 'pygame' not in Config.required_modules:

            sound_loop = 0
            sound_name = ""
            sound_channel = 1

            file_dir = cls.file_dir

            if Config.get("sound_theme", "On") == "On" and name == "main":
                if not mixer.Channel(0).get_busy():
                    sound_loop = -1
                    sound_name = name
                    sound_channel = 0
            elif Config.get("sound", "On") == "On" and name != "main":
                if os.path.isfile(f"{cls.file_dir}{name}.wav"):
                    sound_name = name
                elif os.path.isdir(f"{cls.file_dir}{name}") and os.listdir(f"{cls.file_dir}{name}") != []:
                    file_dir = cls.file_dir + f"{name}/"
                    if os.path.isfile(f"{cls.file_dir}{name}/easter.wav") and random.randint(0, 10) == 6 and not mixer.Channel(3).get_busy():
                        sound_name = "easter"
                        sound_channel = 3
                    else:
                        sound_list = os.listdir(f"{file_dir}")
                        sound_name = random.choice(sound_list).replace(".wav", "")
                        if mixer.Channel(1).get_busy():
                            sound_channel = 2

            if sound_name != "":
                sound = mixer.Sound(f"{file_dir}{sound_name}.wav")
                mixer.Channel(sound_channel).play(sound, loops=sound_loop)

    @classmethod
    def fadeout(cls, time):
        """
        Fadeout theme song
        """
        if 'pygame' not in Config.required_modules:
            if mixer.Channel(0).get_busy():
                mixer.Channel(0).fadeout(time)