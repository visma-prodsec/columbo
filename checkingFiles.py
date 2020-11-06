import sys
import os
import re
import pyfiglet
from colorama import Fore


def checks():
    dir_path = os.path.dirname(os.path.realpath(__file__))

    match = ['_', '-', ' ']

    for x in match:
        if re.search(x, dir_path):
            print('\n')
            ascii_banner = pyfiglet.figlet_format("    Columbo")
            print(Fore.GREEN + ascii_banner)
            print(
                Fore.YELLOW + '\nHello: Before you proceed, please check absolute path of Columbo -> ' + Fore.GREEN + dir_path + Fore.YELLOW +
                ' Remove ( _  or  - ) characters or white spaces from the path. ')
            print('\n')
            os.system('pause')
            sys.exit(0)

    list_files = os.listdir(dir_path + r'\bin')
    # print (list_files)

    """Checking for sigcheck.exe, Volatility 3 and Autorunsc.exe"""

    check_files = []
    for file in list_files:
        if file == "autorunsc.exe":
            check_files.append(file)
        elif file == 'volatility3-master':
            check_files.append(file)
        elif file == 'sigcheck.exe':
            check_files.append(file)

    if len(check_files) != 3:
        print('\n')
        ascii_banner = pyfiglet.figlet_format("    Columbo")
        print(Fore.GREEN + ascii_banner)
        print('\n')
        print(Fore.RED + 'Please Make sure you Read and Understand the license agreement of Volatility 3, '
                         'sigcheck.exe and autorunsc.exe before you download them.\n')
        print(Fore.YELLOW + '1) It is users responsibility and not Columbos to download and use third party tools '
                            'required by Columbo.\n'
                            '2) It is also the users responsibility and not Columbos to agree or disagree on the '
                            'license agreement provided by the third party tools.\n'
                            '3) In relation to MS SysInternal tools. Columbo passes option/argument -accepteula on '
                            'the command lines in order to operate non-interactively. It is also the users '
                            'responsibility and not Columbos to agree or disagree on the license agreement provided '
                            'by MS SysInternal tools.')
        print(Fore.YELLOW + '\nPlease read the license file for more information.')
        # print('\n')
        print(Fore.RED + '\n')
        print(
            r'You need to place the following files under ' + Fore.YELLOW + dir_path + r'\bin' + Fore.RED + ' folder\n')
        print(Fore.WHITE)
        print('1) Volatility as in volatility3-master')
        print('2) sigcheck.exe')
        print('3) autorunsc.exe')
        print('\nPlease read the README.md file for more information')
        print(Fore.YELLOW)
        print('Current available files are:', check_files, '\n')
        # print(list)
        os.system('pause')
        sys.exit(0)

    list_vol = os.listdir(dir_path + r'\bin\volatility3-master')
    out_str = " "
    for _ in list_vol:
        if out_str.join(list_vol) == 'volatility3-master':
            print('\n')
            ascii_banner = pyfiglet.figlet_format("    Columbo")
            print(Fore.GREEN + ascii_banner)
            print('\n')
            print(Fore.YELLOW + '\nError -Please check volatility3-master path  ')
            print(
                Fore.YELLOW + '\nThe path of volatility3-master has to be like ' + dir_path + r'\bin\volatility3-master' + ' and not ' + Fore.WHITE + dir_path + r'\bin\volatility3-master\volatility3-master',
                '\n')
            os.system('pause')
            sys.exit(0)

    return 0
