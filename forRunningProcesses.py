import os
import pickle
import run
import runningProcesses

import pandas as pd
from colorama import Fore


def loop_through(process, df):
    """
    Search and find processes number asked by the user in the DataFrame and return it
    """

    data = df.loc[df['ProcessId'] == process]
    return data


def forward_process(process, df):
    """
    Search, identify and print  the processes - if applicable,  generated by the process that is requested by the
    user in the DatFrame
    """
    data = df.loc[df['ParentProcessId'].isin([process])]
    forward = data[['Services', 'ParentProcessId', 'ProcessId']]
    forwardp = forward.to_string(index=False, header=True)
    if forward.empty:
        print('\n')
        print(Fore.YELLOW + process + ' Does not execute other process(es) - i.e. not a parent process.')
    else:
        print('\n')
        print(Fore.YELLOW + process + ' is a parent process of the following process(es):')
        print('\n')
        print(Fore.WHITE)
        print(forwardp)
    return 0


def process_ml(process_path):
    """
    Once a path/command of a process is identified, it will be piped to the ML model for investigation. 

    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pml = pd.DataFrame(process_path['CommandLine']).to_string(index=False, header=False)

    filename = dir_path + r'\ML\cmdModel.sav'
    vectfile = dir_path + r'\ML\vecFile.sav'
    se_model = pickle.load(open(filename, 'rb'))
    load_vect = pickle.load(open(vectfile, 'rb'))

    if pd.DataFrame(process_path['CommandLine']).isnull().values.any():
        print('\nNo command(s) found -NaN')
    elif pd.DataFrame(process_path['CommandLine']).empty:
        print('\nDataFrame -Commands not found')
    else:
        text = load_vect.transform([pml])
        print_this = se_model.predict(text)
        print_prob = se_model.predict_proba(text) * 100
        print(Fore.WHITE + '\n')

        if print_this == 1:
            print(
                'Machine Learning model classifies ' + Fore.GREEN + ' ' + pml + Fore.WHITE + ' to be ' + Fore.RED
                + 'suspicious.' + Fore.WHITE + ' Please consider its percentage scores shown below: ')
            print(pd.DataFrame(print_prob).to_string(index=False, header=True))
        elif print_this == 0:
            print(
                Fore.WHITE + 'Machine Learning model classifies' + Fore.GREEN + ' ' + pml + Fore.WHITE + ' to be ' +
                Fore.GREEN + 'genuine' + Fore.WHITE + ' Please consider its percentage scores shown below: ')
            print(pd.DataFrame(print_prob).to_string(index=False, header=True))
        else:
            print('No command to learn about')
    return 0


def more_processes():
    """
    Asking user to continue finding more processes 
    """
    m_process = str(input('\nMore processes to trace y/n: ')).lower().strip()
    if m_process == 'y':
        runningProcesses.live_process()
    elif m_process == 'n':
        run.user_input()
    else:
        more_processes()
    return 0


def dll(process, df_dll):
    """
    Extract dll-s files from the DataFrame for the requested process
    """
    dll_data = df_dll[['PID', 'Size', 'Path']]
    dlls = dll_data.loc[dll_data['PID'] == process]
    dll_paths = dlls[['Path', 'Size']]
    dll_paths = pd.DataFrame(dll_paths).to_string(index=False, header=True)

    if dlls.empty:
        print('\n')
        print(Fore.YELLOW + process + ' DLLs or relevant data cannot be found.')
        #print('\n')
        #print(Fore.YELLOW + '-' * 110)
        print(Fore.WHITE)
    else:
        print(Fore.YELLOW + 'Process ' + process + ' and its Dll association ')
        print(Fore.WHITE)
        print(dll_paths)

    return 0


def handles(process, df_handles):
    """
    Extract dll-s files from the DataFrame for the requested process
    """
    data_handles = df_handles.loc[df_handles['PID'] == process]
    data_handles = pd.DataFrame(data_handles).dropna()
    handle_s = data_handles[['PID', 'Offset', 'HandleValue', 'Type', 'GrantedAccess', 'Name']]
    handles_p = handle_s.to_string(index=False, header=True)
    if handle_s.empty:
        print('\n')
        print(Fore.YELLOW + '-' * 110)
        print(Fore.YELLOW + 'Process ' + process + ' Handles cannot be found.')
        print('\n')
        print(Fore.YELLOW + '-' * 110)
        print(Fore.WHITE)
    else:
        print('\n')
        print(Fore.YELLOW + 'Process ' + process + ' associates with the followings handles')
        print('\n')
        print(Fore.WHITE)
        print(handles_p)
        print('\n')
        print(Fore.YELLOW + '-' * 110)
        print(Fore.WHITE)
    return 0
