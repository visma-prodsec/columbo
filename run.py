import about
import autorun
import memo
import tools
import welcome
import threading
from colorama import init, Fore
from termcolor import colored

init()


def user_input():
    """Input from users when Columbo is executed"""

    print(Fore.RED + '\n\nSelect one of the options below.')
    print(colored('1) About, guidelines License.\n2) Live analysis -files and process traceability.\n3) Scan and '
                  'analyse Hard Disk Image File (.vhdx).\n4) Memory Forensics.\n11)Exit Columbo.', 'yellow'))
    lock = threading.Lock()

    try:
        keyboard = int(input('Select: '))
    except ValueError:
        keyboard = 9999
    if keyboard == 1:
        about.about_columbo()
    elif keyboard == 2:
        autorun.investigate()
    elif keyboard == 3:
        tools.input_path()
    elif keyboard == 4:
        with lock:
            memo.memory()
    elif keyboard == 11:
        welcome.goodbye()
    elif keyboard == "":
        print('\nInput is empty, please try again')
        user_input()
    else:
        print('\nWrong attempt, please try again')
        user_input()
    return
