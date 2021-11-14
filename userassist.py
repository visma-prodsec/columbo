import os
import pickle

import numpy as np
import pandas as pd
from colorama import Fore


def user_assist(user_assi):
    """
    In related to memory image. Search, identify and use machine learning of some paths.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    user_binary = dir_path + r'\csvFiles\userBinary.csv'


    dfff = pd.read_csv(user_assi, delimiter="\t", engine='python', error_bad_lines=False, header=None,
                       names=['Hive Offset', 'Hive Name', 'Path', 'Last Write Time', 'Type  Name', 'ID', 'Count',
                              'Focus Count', 'Time Focused', 'Last Updated', 'Raw Data'])


    df = dfff['Type  Name'].dropna(axis=0)

    if df.empty:
        print('\n')
        print(Fore.YELLOW + 'No information found.')
        print('\n')
        print(Fore.YELLOW + '-' * 110)
        print(Fore.WHITE)
    else:

        df.to_csv(user_binary, index=False, header=False)
        # pd.read_csv(user_binary, names=['ID'])
        my_list_path = []
        with open(user_binary, 'rt') as myfile:
            for myline in myfile:
                if "exe" in myline:
                    s = myline.replace('UEME_RUNPATH:', '').strip()
                    my_list_path.append(s)
        mypath = []
        prediction = []
        pred_pro = []
        filename = dir_path + r'\ML\cmdModel.sav'
        vectfile = dir_path + r'\ML\vecFile.sav'
        sec_modell = pickle.load(open(filename, 'rb'))
        load_vect = pickle.load(open(vectfile, 'rb'))
        for i in my_list_path:
            mypath.append(i)
            text = load_vect.transform([i])
            print_this = sec_modell.predict(text)
            print_prob = sec_modell.predict_proba(text) * 100
            prediction.append(print_this)
            pred_pro.append(print_prob)

        this_prediction = pd.DataFrame(prediction)
        if this_prediction.empty:
            print('\n')
            print(Fore.YELLOW + 'Empty DataFrame')
        else:

            this_pred_pro = pd.DataFrame(np.concatenate(pred_pro))
            this_path = pd.DataFrame(mypath)
            this_path = this_path.rename(columns={0: 'path'})
            this_prediction = this_prediction.rename(columns={0: 'ML-Output'})

            result = pd.concat([this_path, this_prediction, this_pred_pro], axis=1, sort=False)
            ree = result.sort_values(by='ML-Output', ascending=False)
            print('\n')
            print(
                Fore.YELLOW + 'Following observations are produced by the built-in Machine '
                              'Learning, please consider their percentage scores before further investigation')
            print('\n')
            print(Fore.WHITE)
            print(ree.to_string(index=False, header=True))
            print('\n')
            print(Fore.YELLOW + '-' * 110)
            print(Fore.WHITE)

    return 0
