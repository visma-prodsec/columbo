import os
from warnings import simplefilter
import pandas
import pandas as pd
import pickle
import run
import runningProcesses
from colorama import Fore


def investigate():
    """Data that is generated from autorun.exe is piped to a csv file where pre-processing, pattern identification
    and machine learning models are used for analysis """

    dir_path = os.path.dirname(os.path.realpath(__file__))
    """To show max columns and rows"""
    pandas.set_option('display.max_rows', 30000)
    pd.options.display.max_colwidth = 10000
    # ignore all future warnings
    simplefilter(action='ignore', category=FutureWarning)
    simplefilter(action='ignore', category=UserWarning)

    print(Fore.WHITE + 'Analysing file systems for possible infection ....')

    autorun1 = dir_path + r'\bin\autorunsc.exe ' + "/accepteula -a * -c -h -s '*' "

    no_banner = ' 2> $null '
    oput = dir_path + r'\csvFiles\autRun.csv'
    os.system(autorun1 + no_banner + ' > ' + oput)

    ml_path = dir_path + r'\ML'
    path = dir_path + r'\csvFiles\autRun.csv'
    file = pd.read_csv(path, delimiter=',', encoding='utf-16', engine='python', na_values=['#NAME?', '?', ''])

    null_columns = file.columns[file.isnull().any()]
    results = file[file["Signer"].isnull()][null_columns]
    this = results[['Launch String', 'Image Path']]
    remove_nan = this.dropna(how='any', axis=0)
    print(Fore.WHITE)
    print(remove_nan)
    print(Fore.YELLOW + '-' * 250)
    cmd_1 = file['Launch String']
    cmd_2 = file['Image Path']

    searchfor = ['cmd.exe', 'rar.exe', 'at.exe', 'schtasks.exe', 'wmic.exe',
                 'powershell.exe', 'winrm.vbs', 'net.exe', 'reg.exe', 'sc.exe', '.job']
    organise1 = cmd_1.loc[cmd_1.str.contains('|'.join(searchfor), na=False)]
    organise2 = cmd_2.loc[cmd_2.str.contains('|'.join(searchfor), na=False)]
    ocmd = pd.concat([organise1, organise2], axis=1, sort=False)
    print('\nOh, there is one more thing...., followings are other executable files that worth investigating :) ')
    print(Fore.WHITE + '\n')
    print(ocmd)
    print('\n')
    print(Fore.YELLOW + '-' * 250)
    print(Fore.WHITE + '\n')

    filename = ml_path + r'\cmdModel.sav'
    vectfile = ml_path + r'\vecFile.sav'

    df = pd.read_csv(path, delimiter=',', encoding='utf-16', engine='python')
    ipath = df[['Launch String']]
    ipath = ipath.dropna(axis=0)
    launch_string = dir_path + r'\csvFiles\launchString.csv'

    ipath.to_csv(launch_string, index=False)

    se_model = pickle.load(open(filename, 'rb'))
    load_vect = pickle.load(open(vectfile, 'rb'))

    with open(launch_string) as f:
        lines = f.readlines()
        text = load_vect.transform(lines)
        print_this = se_model.predict(text)
        print_prob = se_model.predict_proba(text) * 100
        listdf = pd.DataFrame(print_this)
        linesdf = pd.DataFrame(lines)
        line_pr = pd.DataFrame(data=print_prob)

    listdf = listdf.rename(columns={0: 'ML-Output'})
    linesdf = linesdf.rename(columns={0: 'path'})

    result = pd.concat([linesdf, listdf, line_pr], axis=1, sort=False)
    re = result.sort_values(by='ML-Output', ascending=False)

    re.to_csv(ml_path + r'\outputML.csv', index=False)
    ml_results = pd.read_csv(ml_path + r'\outputML.csv', sep=",", decimal=" ")
    dff2 = ml_results.loc[ml_results['ML-Output'] == 1]

    pd.DataFrame(dff2).to_excel(ml_path + r'\Step-2-results\suspicious_paths.xlsx', index=False)
    pd.DataFrame(ml_results).to_excel(ml_path + r'\Step-2-results\all_paths.xlsx', index=False)

    dff2 = dff2.to_string(index=False, header=True)

    print('\n')
    print(
        Fore.YELLOW + "Alright, I bothered you enough for today, but just one more thing, Machine Learning model "
                      "identifies following paths to be" + Fore.RED + ' suspicious')
    print(Fore.WHITE)
    print(dff2)
    print('\n')
    print(
        Fore.YELLOW + 'Machine Learning suspects above paths to be' + Fore.RED + ' suspicious.'
        + Fore.YELLOW + 'Please check under ' + Fore.GREEN + dir_path + '\ML\Step-2-results\suspicious_paths.xlsx '
        + Fore.YELLOW + 'if above results are not very clear.')
    print(
        Fore.YELLOW + r'Please note, both genuine and suspicious results can be found under '
        + Fore.GREEN + dir_path + r'\ML\Step-2-results\all_paths.xlsx ')
    print(
        Fore.YELLOW + '\nJust one more thing, make sure you consider the probability facts of both 1 and 0 before '
                      'selecting anything for more investigation. ')

    # Removing files that are not no longer required after the operation.
    os.remove(launch_string)
    os.remove(oput)
    os.remove(ml_path + r'\outputML.csv')

    # print ('\n')
    print(Fore.GREEN)
    process_running = str(input('\nWould you like to learn about running processes y/n: ')).lower().strip()
    if process_running == 'y':
        runningProcesses.live_process()
    else:
        run.user_input()

    return run.user_input()
