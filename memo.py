import processCheckingNu
import run
import subprocess
import userassist
import autoscan

from pandas import DataFrame
from userassist import *

dir_path = os.path.dirname(os.path.realpath(__file__))


def memory():
    """
    Output from volatility is used for the purpose of process grouping,
    traceability, detect suspicious or genuine paths or commands by calling
    other functions.

    """
    mypath = dir_path + r'\csvFiles\imgs'
    for filename in os.listdir(mypath):
        filepath = os.path.join(mypath, filename)
        os.remove(filepath)

    print(Fore.RED + '\nPlease remove white spaces before passing the path of the memory image.')
    print(Fore.GREEN)
    path = input(r'Provide absolute path of your memory image (e.g. G:\memory-files\memory.img):')
    if path == '':
        print(Fore.YELLOW + '\nError - empty path')
        memory()
    if not os.path.exists(path):
        print(Fore.YELLOW + '\nError - path could not be found. Please try again')
        memory()

    output = dir_path + r'\csvFiles\imgs\processTrace.csv'

    """ put  path of python.exe version 3.7+++ """
    py = 'python.exe'
    # print (py)
    cmd = dir_path + r'\bin\volatility3-master\vol.py -f'

    ps_scan = 'windows.psscan.PsScan'
    cmdps_scan = py + ' ' + cmd + ' ' + path + ' ' + ps_scan

    path_cmd = ' > ' + dir_path + r'\csvFiles\process_cmd.csv'
    user_assi = dir_path + r'\csvFiles\userAssist.csv'
    mal = py + ' ' + cmd + ' ' + path + ' ' + 'windows.malfind.Malfind'
    win_cmd = py + ' ' + cmd + ' ' + path + ' ' + 'windows.cmdline.CmdLine' + path_cmd
    error = dir_path + r'\csvFiles\err\err.txt'
    print(Fore.WHITE)
    key_selection= str(input('\nPress y for automatic analysis or n for manual analysis ? y/n: ')).lower().strip()
    print(Fore.GREEN)

    if key_selection == 'n':

        # Memory information
        key = str(input('Memory Information? y/n: ')).lower().strip()
        if key == 'y':
            imageinfo = 'windows.info'
            cmdmem_info = py + ' ' + cmd + ' ' + path + ' ' + imageinfo
            print(Fore.WHITE)

            try:

                proc = subprocess.check_output(cmdmem_info, shell=True, stderr=subprocess.STDOUT, encoding='utf-8', )
                print(proc)

            except subprocess.CalledProcessError:
                print(
                    Fore.YELLOW + r'Error- Volatility related. Maybe latest windows folder under '
                    + dir_path + r'\volatility3-master\volatility\symbols is required ')
                print(
                    Fore.YELLOW + '\nAlso check volatility3-master path to be like ' + dir_path + r'\bin\volatility3-master' + ' and not ' + Fore.WHITE + dir_path + r'\bin\volatility3-master\volatility3-master',
                    '\n')

        print(Fore.YELLOW)
        print('-' * 110)
        print(Fore.GREEN)

        # Process Scanning

        key = str(input('Processes Scan y/n: ')).lower().strip()
        if key == 'y':

            print(Fore.WHITE)
            try:

                proc_ps = subprocess.check_output(cmdps_scan, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                with open(output, 'w') as outputfile:
                    print(proc_ps, file=outputfile)

                file = open(output, 'r')
                dfp = pd.read_csv(file, delimiter="\t",
                                  names=["PID", "PPID", "ImageFileName", "Offset", "Threads", "Handles", "SessionId",
                                         "Wow64",
                                         "CreateTime", "ExitTime"], header=None)
                # print (dfp.head())
                dfp = dfp[['PPID', 'PID', 'ImageFileName', 'CreateTime', 'ExitTime']]
                file.close()
                # print (df.head())
                grouped = dfp.groupby(dfp['PPID'])
                to_file = dir_path + r'\csvFiles\imgs\processToFile.txt'
                fi = open(to_file, 'w')
                for name, group in grouped:
                    print('\n')
                    fi.write('\n')
                    fi.write(name)
                    fi.write('\n')
                    print(name)
                    print(DataFrame(group).to_string(index=False, header=True))
                    fi.write(DataFrame(group).to_string(index=False, header=True))
                    fi.write('\n')
                fi.close()
                print(Fore.GREEN)
                file_y = str(input(
                    '\nWould you like to see the above output on a notepad file for later use? y/n: ')).lower().strip()
                if file_y == 'y':
                    subprocess.Popen(['notepad.exe', to_file])

                print(
                    Fore.YELLOW + '\nOne more thing.... Getting dll-list and handles data if available -for later use in ' +
                    Fore.WHITE + 'Process Traceability\n')

                dll = 'windows.dlllist.DllList'
                handles = 'windows.handles.Handles'

                dllout = dir_path + r'\csvFiles\imgs\dll.csv'
                handlesout = dir_path + r'\csvFiles\imgs\handles.csv'

                cmd_dll = py + ' ' + cmd + ' ' + path + ' ' + dll + ' ' + ' > ' + dllout
                cmd_handles = py + ' ' + cmd + ' ' + path + ' ' + handles + ' > ' + handlesout + ' > ' + handlesout


                os.system(cmd_dll + ' 2> ' + error)
                os.system(cmd_handles + ' 2> ' + error)

            except subprocess.CalledProcessError:
                print(
                    Fore.YELLOW + r'Error- Volatility related. Maybe latest windows folder under '
                    + dir_path + r'\volatility3-master\volatility\symbols is required ')
                print(
                    Fore.YELLOW + '\nAlso check volatility3-master path to be like ' + dir_path + r'\bin\volatility3-master' + ' and not ' + Fore.WHITE + dir_path + r'\bin\volatility3-master\volatility3-master',
                    '\n')

        # Process Tree

        print(Fore.YELLOW)
        print('-' * 110)
        print(Fore.GREEN)
        key = str(input('Processes Tree  y/n: ')).lower().strip()
        if key == 'y':
            pstree = 'windows.pstree.PsTree'
            cmdps_tree = py + ' ' + cmd + ' ' + path + ' ' + pstree
            print(Fore.WHITE)

            try:
                proc_tree = subprocess.check_output(cmdps_tree, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
                print(proc_tree)

            except subprocess.CalledProcessError:
                print(
                    Fore.YELLOW + r'Error- Volatility related. Maybe latest windows folder under '
                    + dir_path + r'\volatility3-master\volatility\symbols is required ')
                print(
                    Fore.YELLOW + '\nAlso check volatility3-master path to be like ' + dir_path + r'\bin\volatility3-master' + ' and not ' + Fore.WHITE + dir_path + r'\bin\volatility3-master\volatility3-master',
                    '\n')

        print(Fore.YELLOW)
        print('-' * 110)
        print(Fore.GREEN)

        # Anomaly Detection and Process Traceability

        print(Fore.GREEN)
        key = str(input('Anomaly Detection and Process Traceability y/n: ')).lower().strip()
        if key == 'y':
            print(Fore.WHITE)

            try:

                if not os.listdir(dir_path + r'\csvFiles\imgs'):
                    print(
                        Fore.YELLOW + '\nYou need to run Process Scan to use process traceability option. Please try again')
                    memory()
                else:

                    users_path = py + ' ' + cmd + ' ' + path + ' ' + \
                                 ' windows.registry.userassist.UserAssist' + ' >  ' + user_assi
                    os.system(win_cmd)
                    to_file1 = dir_path + r'\csvFiles\imgs\MalAnomaly.txt'

                    os.system(mal + ' >' + to_file1)
                    print(Fore.WHITE)
                    os.system(users_path)
                    print(Fore.WHITE)
                    mal_file = open(to_file1, 'r')
                    print(mal_file.read())
                    mal_file.close()
                    print(Fore.GREEN)
                    file_y1 = str(input(
                        '\nWould you like to see the above output on a notepad file for later use? y/n: ')).lower().strip()

                    if file_y1 == 'y':
                        subprocess.Popen(['notepad.exe', to_file1])

                    userassist.user_assist(user_assi)
                    processCheckingNu.processes()

            except subprocess.CalledProcessError:
                print(
                    Fore.YELLOW + r'Error- Volatility related. Maybe latest windows folder under '
                    + dir_path + r'\volatility3-master\volatility\symbols is required ')

                print(
                    Fore.YELLOW + '\nAlso check volatility3-master path to be like ' + dir_path + r'\bin\volatility3-master' + ' and not ' + Fore.WHITE + dir_path + r'\bin\volatility3-master\volatility3-master',
                    '\n')
        else:
            run.user_input()


    if key_selection == 'y':

        print(Fore.WHITE)
        try:
            print ('\nChecking processes .... ')
            print('\nOne more thing.... sometimes analysis takes a bit of time!')

            proc_ps = subprocess.check_output(cmdps_scan, shell=True, stderr=subprocess.STDOUT, encoding='utf-8')
            with open(output, 'w') as outputfile:
                print(proc_ps, file=outputfile)

            file = open(output, 'r')
            dfp = pd.read_csv(file, delimiter="\t",
                              names=["PID", "PPID", "ImageFileName", "Offset", "Threads", "Handles", "SessionId",
                                     "Wow64",
                                     "CreateTime", "ExitTime"], header=None)
            # print (dfp.head())
            dfp = dfp[['PPID', 'PID', 'ImageFileName', 'CreateTime', 'ExitTime']]
            file.close()
            # print (df.head())
            grouped = dfp.groupby(dfp['PPID'])
            to_file = dir_path + r'\csvFiles\imgs\processToFile.txt'
            fi = open(to_file, 'w')
            for name, group in grouped:
                #print('\n')
                fi.write('\n')
                fi.write(name)
                fi.write('\n')
                fi.write(DataFrame(group).to_string(index=False, header=True))
                fi.write('\n')
            fi.close()
            print(Fore.WHITE)
            # Dll and handles
            dll = 'windows.dlllist.DllList'
            handles = 'windows.handles.Handles'

            dllout = dir_path + r'\csvFiles\imgs\dll.csv'
            handlesout = dir_path + r'\csvFiles\imgs\handles.csv'

            cmd_dll = py + ' ' + cmd + ' ' + path + ' ' + dll + ' ' + ' > ' + dllout
            cmd_handles = py + ' ' + cmd + ' ' + path + ' ' + handles + ' > ' + handlesout + ' > ' + handlesout

            print('\nStill checking....')
            print('\n')

            os.system(cmd_dll + ' 2> ' + error)
            os.system(cmd_handles + ' 2> ' + error)

            users_path = py + ' ' + cmd + ' ' + path + ' ' + \
                         ' windows.registry.userassist.UserAssist' + ' >  ' + user_assi
            os.system(win_cmd)
            to_file1 = dir_path + r'\csvFiles\imgs\MalAnomaly.txt'

            os.system(mal + ' >' + to_file1)
            #print(Fore.WHITE)
            os.system(users_path)
            userassist.user_assist(user_assi)
            autoscan.analysis()
            subprocess.Popen(['notepad.exe', to_file])

            print ( Fore.YELLOW + 'Use the following tool to trace and examine other processes')
            processCheckingNu.processes()


        except subprocess.CalledProcessError:
            print(
                Fore.YELLOW + r'Error- Volatility related. Maybe latest windows folder under '
                + dir_path + r'\volatility3-master\volatility\symbols is required ')
            print(
                Fore.YELLOW + '\nAlso check volatility3-master path to be like ' + dir_path + r'\bin\volatility3-master' + ' and not ' + Fore.WHITE + dir_path + r'\bin\volatility3-master\volatility3-master',
                '\n')
    else:

        print (Fore.YELLOW + 'Error - try again')
        memory()



    return run.user_input()
