import os

class Config :

    file_path = "config.ini"
    required_modules = []
    AVAILABLE_CHARACTERS = {}

    @classmethod
    def __load(cls):
        config = {}
        if os.path.isfile(cls.file_path):
            try:
                with open(cls.file_path, "r") as f:
                    for line in f.readlines():
                        if line[0] != "[" and line[0] != ";" and line != "\n":
                            line = line.replace("\n", "")
                            line = line.split("=")
                            config[line[0]] = line[1]
            except:
                pass
        return config

    @classmethod
    def get(cls, name, default=None):
        """
        PARAM : - name : string
                - default : None or string
        RETURN : value of the configuration key
        """
        config = cls.__load()
        if name in config:
            return config[name]
        else:
            if default not in ['', None]:
                cls.save(name, default)
            return default

    @classmethod
    def save(cls, name, value):
        """
        Save in the configuration file
        PARAM : - name : string
                - value
        """
        change = False
        config = cls.__load()
        if name not in config or config[name] != value :
            config[name] = value
            change = True
        
        if change:
            try:
                with open(cls.file_path, "w") as f:
                    f.write("[config]\n")
                    f.write("; Manual modification may cause malfunctions\n")
                    for key in config:
                        f.write(f"{key}={config[key]}\n")
            except:
                pass
        return value