import os
import json
import datetime

class History :

    file_path = "System/history.dat"

    @classmethod
    def __load(cls):
        history = []
        if os.path.isfile(cls.file_path):
            try:
                with open(cls.file_path, "r") as f:
                    history = json.load(f)
            except:
                pass
        return history

    @classmethod
    def get(cls):
        """
        RETURN : content of file containing the previous games
        """
        history = cls.__load()
        return history

    @classmethod
    def save(cls, game_type, game_player, game_history):
        """
        Saves a game in the file containing the previous games
        """
        history = cls.__load()
        d = datetime.datetime.now()
        history.append({
            "title":f"{game_type} - {d.day}/{d.month}/{d.year} ({d.hour}h{d.minute})",
            "history":game_history,
            "players":game_player
        })
        if len(history) > 5:
            history.pop(0)

        try:
            with open(cls.file_path, "w") as f:
                json.dump(history, f)
        except:
            pass