from colorama import init, Fore
import pyfiglet
import sys
import os

init()


def welcome():
    print('\n')
    ascii_banner = pyfiglet.figlet_format("    Columbo")
    print(Fore.GREEN + ascii_banner)
    print(Fore.GREEN + '\n                                                       Simplify your Computer Forensics')
    print(
        Fore.YELLOW + '                                                    Alan Saied, Product Security -Visma')
    print('                                                                 Version: Beta')
    print('                                                               Platform: Windows\n')


def goodbye():
    custom_fig = pyfiglet.Figlet(font='bulbhead')
    print(custom_fig.renderText('See you'))
    os.system('pause')
    sys.exit(0)
