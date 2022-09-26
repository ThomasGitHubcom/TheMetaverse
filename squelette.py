import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

try:
    from Classes.config import Config
except ModuleNotFoundError:
    clear()
    input("Please unzip the archive to play the game")
    exit()

def module_test(modules):
    for module in modules[:]:
        try:
            __import__(module)
            modules.remove(module)
        except ModuleNotFoundError:
            pass
    return modules

if __name__ == "__main__":
    clear()
    print("Loading...")
    answer = "N"
    required_modules = ['requests', 'colorama', 'pygame']

    required_modules = module_test(required_modules)

    if len(required_modules) != 0:
        answer = "I"

    while answer not in ["Y", "N", "y", "n"]:
        clear()
        answer = input("Do you want to install the additional content for a maximum gaming experience ? (Y/N) : ")

    if answer in ["Y", "y"]:
        for module in required_modules:
            if os.name == 'nt':
                os.system('pip install ' + module)
            else:
                os.system('pip3 install ' + module)

    required_modules = module_test(required_modules)

    clear()
    if len(required_modules) > 0 and (answer == "Y" or answer == "y"):
        space = 24
        print(" "*(space+5) +"  ______________________________    . \  | / .")
        print(" "*(space+5) +" /                            / \     \ \ / /")
        print(" "*(space+5) +"|                            | ==========  - -")
        print(" "*(space+5) +" \____________________________\_/     / / \ \ ") # from asciiart.eu
        print("")
        print("Unable to install additional content. Have you tried to connect to the internet ?")
        print("Restarting the program may also be the solution.")
        print("")
        input(" "*space +"Press a key to start the game without additional content")

    Config.required_modules = required_modules

    from Classes.gui import Gui
    panel = Gui()
    try:
        panel.main()
    except KeyboardInterrupt:
        panel.main()
    else:
        pass