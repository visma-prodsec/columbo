import forRunningProcesses

import os
import pandas
import pickle
import re
import run
from warnings import simplefilter

import pandas as pd
from colorama import Fore


dir_path = os.path.dirname(os.path.realpath(__file__))
simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=UserWarning)
pandas.set_option('display.max_rows', 300000)
pd.options.display.max_colwidth = 1000000
path_to_process = dir_path + r'\csvFiles\process_cmd.csv'
filename = dir_path + r'\ML\cmdModel.sav'
vectfile = dir_path + r'\ML\vecFile.sav'
handlesout = dir_path + r'\csvFiles\imgs\handles.csv'
dllout = dir_path + r'\csvFiles\imgs\dll.csv'
path2 = dir_path + r'\csvFiles\imgs\processTrace.csv'


def processes():
    """
    In relation to memory image. Identify processes, traceability, Machine Learning and execution of other processes

    """
    file = open(path2, 'r')
    df = pd.read_csv(file, delimiter="\t",
                     names=["PID", "PPID", "ImageFileName", "Offset", "Threads", "Handles", "SessionId", "Wow64",
                            "CreateTime", "ExitTime"], header=None)
    file.close()

    d_frame = pd.read_csv(path_to_process, delimiter="\t", names=["PID", "Process", "Argu"], encoding='cp1252' ,header=None)
    df_handles = pd.read_csv(handlesout, delimiter="\t",
                             names=['PID', 'Process', 'Offset', 'HandleValue', 'Type', 'GrantedAccess', 'Name'],
                             header=None)
    df_dll = pd.read_csv(dllout, delimiter="\t", encoding='cp1252' ,names=['PID', 'Process', 'Base', 'Size', 'Name', 'Path'],
                         header=None)

    # print('\n')

    print(Fore.GREEN)
    print('Select process ID (PID) for process traceability')
    process = input('Enter  process ID : ')

    if process.isdigit():

        s = scan_through(process, df)
        data = s[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False, header=False)
        data = list(data.split())
        # print (data)
        s0 = scan_through(data[2], df)
        lis = list()
        lis.append(data[1])

        if s0.empty or data[2] == '4' or data[2] == data[1]:

            process_cmd_find(d_frame, process)

            print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
            print(Fore.WHITE)
            print('Process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                4] + '\n' + ' has a root process of ' + ' ' + data[2])
            forward_p(process, df)
            forRunningProcesses.dll(process, df_dll)
            forRunningProcesses.handles(process, df_handles)
            print(Fore.GREEN)
            processes_more()

        else:
            data1 = data[2]
            # print (data1)
            s1 = scan_through(data1, df)
            data1 = s1[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False, header=False)
            data1 = list(data1.split())
            s1 = scan_through(data1[2], df)
            # print(data1)
            lis.append(data1[1])
            if s1.empty or data1[2] == '4' or data1[2] in lis:

                process_cmd_find(d_frame, process)

                print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
                print(Fore.WHITE)
                print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                    4] + ' executed by  ' + '\n' + data1[0] + '(' + data1[1] + ')' + '/' +
                      data1[3] + '-' + data1[4] + ' root process is ' + ' ' + data1[2])
                forward_p(process, df)
                forRunningProcesses.dll(process, df_dll)
                forRunningProcesses.handles(process, df_handles)

                print(Fore.GREEN)
                processes_more()

            else:
                data2 = data1[2]
                # print(data2)
                s2 = scan_through(data2, df)
                data2 = s2[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False,
                                                                                                 header=False)
                data2 = list(data2.split())
                s2 = scan_through(data2[2], df)
                # print(data2)
                lis.append(data2[1])
                if s2.empty or data2[2] == '4' or data2[2] in lis:

                    process_cmd_find(d_frame, process)

                    print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
                    print(Fore.WHITE)

                    print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                        4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                          data1[3] + '-' + data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[3] + '-' +
                          data2[4] + ' root process is ' + '  ' + data2[2])
                    forward_p(process, df)
                    forRunningProcesses.dll(process, df_dll)
                    forRunningProcesses.handles(process, df_handles)

                    print(Fore.GREEN)
                    processes_more()

                else:
                    data3 = data2[2]
                    # print(data3)
                    s3 = scan_through(data3, df)
                    data3 = s3[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False,
                                                                                                     header=False)
                    data3 = list(data3.split())
                    s3 = scan_through(data3[2], df)
                    # print(data3)
                    lis.append(data3[1])
                    if s3.empty or data3[2] == '4' or data3[2] in lis:

                        process_cmd_find(d_frame, process)

                        print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
                        print(Fore.WHITE)
                        print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                            4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                              data1[3] + '-' + data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                                  3] + '-' +
                              data2[4] + ' <- ' + data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' + data3[4]
                              + ' root process is ' + ' ' + data3[2])

                        forward_p(process, df)
                        forRunningProcesses.dll(process, df_dll)
                        forRunningProcesses.handles(process, df_handles)

                        print(Fore.GREEN)
                        processes_more()

                    else:
                        data4 = data3[2]
                        # print(data4)
                        s4 = scan_through(data4, df)
                        data4 = s4[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False,
                                                                                                         header=False)
                        data4 = list(data4.split())
                        s4 = scan_through(data4[2], df)
                        # print(data4)
                        lis.append(data4[1])
                        if s4.empty or data4[2] == '4' or data4[2] in lis:

                            process_cmd_find(d_frame, process)

                            print(
                                Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
                            print(Fore.WHITE)
                            print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                                4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                                  data1[3] + '-' + data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                                      3] + '-' + data2[4] + ' <- ' + data3[0] + '(' + data3[1] + ')' + '/' + data3[
                                      3] + '-' + data3[
                                      4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' + data4[
                                      3] + '-' + data4[4]
                                  + ' ' + ' root process is ' + ' ' + data4[2])

                            forward_p(process, df)
                            forRunningProcesses.dll(process, df_dll)
                            forRunningProcesses.handles(process, df_handles)

                            print(Fore.GREEN)
                            processes_more()

                        else:
                            data5 = data4[2]
                            # print(data5)
                            s5 = scan_through(data5, df)
                            data5 = s5[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                index=False,
                                header=False)
                            data5 = list(data5.split())
                            s5 = scan_through(data5[2], df)
                            # print(data5)
                            lis.append(data5[1])
                            if s5.empty or data5[2] == '4' or data5[2] in lis:

                                process_cmd_find(d_frame, process)

                                print(
                                    Fore.YELLOW + '\n\nProcess traceability '
                                                  'coupled with time executions of each process\n')
                                print(Fore.WHITE)
                                print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                                    4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                                      data1[3] + '-' + data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' +
                                      data2[
                                          3] + '-' + data2[4] + ' <- ' + data3[0] + '(' + data3[1] + ')' + '/' + data3[
                                          3] + '-' + data3[
                                          4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' + data4[
                                          3] + '-' + data4[4] + ' <- ' + data5[0] + '(' + data5[1] + ')' + '/' + data5[
                                          3] + '-' + data5[4]
                                      + ' root process is ' + ' ' + data5[2])

                                forward_p(process, df)
                                forRunningProcesses.dll(process, df_dll)
                                forRunningProcesses.handles(process, df_handles)

                                print(Fore.GREEN)
                                processes_more()

                            else:
                                data6 = data5[2]
                                # print(data6)
                                s6 = scan_through(data6, df)
                                data6 = s6[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                    index=False, header=False)
                                data6 = list(data6.split())
                                s6 = scan_through(data6[2], df)
                                # print(data6)
                                lis.append(data6[1])
                                if s6.empty or data6[2] == '4' or data6[2] in lis:

                                    process_cmd_find(d_frame, process)

                                    print(
                                        Fore.YELLOW + '\n\nProcess traceability coupled '
                                                      'with time executions of each process\n')
                                    print(Fore.WHITE)
                                    print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                                        4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                                          data1[3] + '-' + data1[
                                              4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                                              3] + '-' + data2[4] + ' <- ' +
                                          data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' + data3[
                                              4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' + data4[
                                              3] + '-' + data4[4] + ' <- ' +
                                          data5[0] + '(' + data5[1] + ')' + '/' + data5[3] + '-' + data5[
                                              4] + ' <- ' + data6[0] + '(' + data6[1] + ')' + '/' + data6[
                                              3] + '-' + data6[4]
                                          + ' root process is ' + ' ' + data6[2])

                                    forward_p(process, df)
                                    forRunningProcesses.dll(process, df_dll)
                                    forRunningProcesses.handles(process, df_handles)

                                    print(Fore.GREEN)
                                    processes_more()

                                else:
                                    data7 = data6[2]
                                    # print(data7)
                                    s7 = scan_through(data7, df)
                                    data7 = s7[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                        index=False, header=False)
                                    data7 = list(data7.split())
                                    s7 = scan_through(data7[2], df)
                                    # print(data7)
                                    lis.append(data7[1])
                                    if s7.empty or data7[2] == '4' or data7[2] in lis:

                                        process_cmd_find(d_frame, process)

                                        print(
                                            Fore.YELLOW + '\n\nProcess traceability coupled'
                                                          ' with time executions of each process\n')
                                        print(Fore.WHITE)
                                        print(
                                            'process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                                                4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[
                                                1] + ')' + '/' + data1[3] + '-' + data1[
                                                4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                                                3] + '-' + data2[4] + ' <- ' +
                                            data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' + data3[
                                                4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' + data4[
                                                3] + '-' + data4[4] + ' <- ' +
                                            data5[0] + '(' + data5[1] + ')' + '/' + data5[3] + '-' + data5[
                                                4] + ' <- ' + data6[0] + '(' + data6[1] + ')' + '/' + data6[
                                                3] + '-' + data6[4] + ' <- ' + data7[0] + '(' +
                                            data7[1] + ')' + '/' + data7[3] + '-' + data7[4]
                                            + ' root process is ' + ' ' +
                                            data7[2])

                                        forward_p(process, df)
                                        forRunningProcesses.dll(process, df_dll)
                                        forRunningProcesses.handles(process, df_handles)
                                        # print ('\n')
                                        print(Fore.GREEN)
                                        processes_more()

                                    else:
                                        data8 = data7[2]
                                        # print(data8)
                                        s8 = scan_through(data8, df)
                                        data8 = s8[
                                            ['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                            index=False, header=False)
                                        data8 = list(data8.split())
                                        s8 = scan_through(data8[2], df)
                                        # print(data8)
                                        lis.append(data8[1])
                                        if s8.empty or data8[2] == '4' or data8[2] in lis:

                                            process_cmd_find(d_frame, process)

                                            print(
                                                Fore.YELLOW + '\n\nProcess traceability coupled '
                                                              'with time executions of each process\n')
                                            print(Fore.WHITE)
                                            print(
                                                'process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                                                    4] + ' executed by  ' + '\n' + ' ' +
                                                data1[0] + '(' + data1[1] + ')' + '/' + data1[3] + '-' + data1[
                                                    4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                                                    3] + '-' + data2[4] + ' <- ' +
                                                data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' + data3[
                                                    4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' + data4[
                                                    3] + '-' + data4[4] + ' <- ' +
                                                data5[0] + '(' + data5[1] + ')' + '/' + data5[3] + '-' + data5[
                                                    4] + ' <- ' + data6[0] + '(' + data6[1] + ')' + '/' + data6[
                                                    3] + '-' + data6[4] + ' <- ' + data7[0] + '(' +
                                                data7[1] + ')' + '/' + data7[3] + '-' + data7[4] + ' <- ' + data8[
                                                    0] + '(' + data8[1] + ')' + '/' + data8[3] + '-' + data8[4]
                                                + ' root process is ' +
                                                data8[2])

                                            forward_p(process, df)
                                            forRunningProcesses.dll(process, df_dll)
                                            forRunningProcesses.handles(process, df_handles)
                                            # print ('\n')
                                            print(Fore.GREEN)
                                            processes_more()

                                        else:
                                            data9 = data8[2]
                                            # print(data9)
                                            s9 = scan_through(data9, df)
                                            data9 = s9[
                                                ['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                                index=False, header=False)
                                            data9 = list(data9.split())
                                            s9 = scan_through(data9[2], df)
                                            # print(data9)
                                            lis.append(data9[1])
                                            if s9.empty or data9[2] == '4' or data9[2] in lis:

                                                process_cmd_find(d_frame, process)

                                                print(
                                                    Fore.YELLOW + '\n\nProcess traceability coupled'
                                                                  ' with time executions of each process\n')
                                                print(Fore.WHITE)
                                                print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' +
                                                      data[4] + ' executed by  ' + '\n' + ' ' +
                                                      data1[0] + '(' + data1[1] + ')' + '/' + data1[3] + '-' + data1[
                                                          4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                                                          3] + '-' + data2[4] + ' <- ' +
                                                      data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' + data3[
                                                          4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' + data4[
                                                          3] + '-' + data4[4] + ' <- ' +
                                                      data5[0] + '(' + data5[1] + ')' + '/' + data5[3] + '-' + data5[
                                                          4] + ' <- ' + data6[0] + '(' + data6[1] + ')' + '/' + data6[
                                                          3] + '-' + data6[4] + ' <- ' + data7[0] + '(' +
                                                      data7[1] + ')' + '/' + data7[3] + '-' + data7[4] + ' <- ' + data8[
                                                          0] + '(' + data8[1] + ')' + '/' + data8[3] + '-' + data8[
                                                          4] + ' <- ' + data9[0] + '(' + data9[1] + ')' + '/' + data9[
                                                          3] + '-' + data9[4] + ' root process is ' + ' ' +
                                                      data9[2])

                                                forward_p(process, df)
                                                forRunningProcesses.dll(process, df_dll)
                                                forRunningProcesses.handles(process, df_handles)

                                                # print ('\n')
                                                print(Fore.GREEN)
                                                processes_more()

                                            else:
                                                data10 = data9[2]
                                                # print(data10)
                                                s10 = scan_through(data10, df)
                                                data10 = s10[['ImageFileName', 'PID', 'PPID', "CreateTime",
                                                              "ExitTime"]].to_string(index=False, header=False)
                                                data10 = list(data10.split())
                                                s10 = scan_through(data10[2], df)
                                                # print(data10)
                                                lis.append(data10[1])
                                                if s10.empty or data10[2] == '4' or data10[2] in lis:

                                                    process_cmd_find(d_frame, process)
                                                    print(
                                                        Fore.YELLOW + '\n\nProcess traceability coupled '
                                                                      'with time executions of each process\n')
                                                    print(Fore.WHITE)

                                                    print('\n')
                                                    print('process ' + data[0] + '(' + process + ')' + '/' + data[
                                                        3] + '-' + data[4] + ' excuted by  ' + '\n' + ' ' +
                                                          data1[0] + '(' + data1[1] + ')' + '/' + data1[3] + '-' +
                                                          data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' +
                                                          data2[3] + '-' + data2[4] + ' <- ' +
                                                          data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' +
                                                          data3[4] + ' <- ' + data4[0] + '(' + data4[1] + ')' + '/' +
                                                          data4[3] + '-' + data4[4] + ' <- ' +
                                                          data5[0] + '(' + data5[1] + ')' + '/' + data5[3] + '-' +
                                                          data5[4] + ' <- ' + data6[0] + '(' + data6[1] + ')' + '/' +
                                                          data6[3] + '-' + data6[4] + ' <- ' + data7[0] + '(' +
                                                          data7[1] + ')' + '/' + data7[3] + '-' + data7[4] + ' <- ' +
                                                          data8[0] + '(' + data8[1] + ')' + '/' + data8[3] + '-' +
                                                          data8[4] + ' <- ' + data9[0] + '(' + data9[1] + ')' + '/' +
                                                          data9[3] + '-' + data9[4]
                                                          + ' <- ' + data10[0] + '(' + data10[1]
                                                          + ')' + '/' + data10[3] + '-' + data10[
                                                              4] + ' root process is ' + ' ' + data10[2])

                                                    forward_p(process, df)
                                                    forRunningProcesses.dll(process, df_dll)
                                                    forRunningProcesses.handles(process, df_handles)

                                                    print(Fore.GREEN)
                                                    processes_more()

                                                else:
                                                    print('\n')
                                                    print('\nTraceability: Maximum of 10 proceeses')
                                                    processes()
    else:
        print('\n')
        print(Fore.YELLOW + 'Wrong  process ID, trying again')
        processes()
    return run.user_input()


def scan_through(process, df):
    """
    Scan and identify  process in the DataFrame and return the result.
    """
    data = df.loc[df['PID'] == process]
    return data


def process_cmd_find(d_frame, process):
    """
    In relation to memory image. Search, identify, commands or paths in a form of suspicious or genuine.
    """
    find_ = d_frame.loc[d_frame['PID']== process]
    process_path_check = find_['Argu']
    process_path = find_['Argu'].to_string(index=False, header=False)

    sec_model = pickle.load(open(filename, 'rb'))
    load_vect = pickle.load(open(vectfile, 'rb'))
    text = load_vect.transform([process_path])

    if pd.DataFrame(process_path_check).empty:
        print('\n')
        print(Fore.YELLOW + 'Nothing relevant found - path nor command ')
        # print('\n')
        #print(Fore.YELLOW + '-' * 110)
    elif pd.DataFrame(process_path_check).isnull().values.any():
        print('\n')
        print(Fore.YELLOW + '->Nothing relevant found - path nor command ')
        # print('\n')
        #print(Fore.YELLOW + '-' * 110)
    elif re.search('Required memory', process_path):
        print('\n')
        print(Fore.YELLOW + 'No relevant commands found')
        #print('\n')
        #print(Fore.YELLOW + '-' * 110)
    else:
        print_this = sec_model.predict(text)
        print_prob = sec_model.predict_proba(text) * 100
        print(Fore.WHITE + '\n')
        print('Possible process path or execution: ' + Fore.YELLOW + process_path)
        print('\n')
        #print(Fore.YELLOW + '-' * 110)
        #print('\n')
        if print_this == 1:
            print(
                'Machine Learning model classifies ' + Fore.GREEN + ' ' + process_path + Fore.WHITE + ' to be '
                + Fore.RED + ' suspicious.' + Fore.WHITE + ' Please consider its percentage scores shown below: ')
            print(pd.DataFrame(print_prob).to_string(index=False, header=True))
            #print('\n')
            #print(Fore.YELLOW + '-' * 110)
        elif print_this == 0:
            print(
                Fore.WHITE + 'Machine Learning model classifies' + Fore.GREEN + ' ' + process_path + Fore.WHITE +
                ' to be ' + Fore.GREEN + 'genuine' + Fore.WHITE +
                ' Please consider its percentage scores shown below: ')
            print(pd.DataFrame(print_prob).to_string(index=False, header=True))
            #print('\n')
           #print(Fore.YELLOW + '-' * 110)
        else:
            print('No command to learn about')
            #print('\n')
            print(Fore.YELLOW + '-' * 110)

    return 0


def forward_p(process, df):
    """
    In relation to memory image. Search, identify and print  the processes - if applicable,  generated by the process
    that is requested by the user in the DatFrame.

    """
    data = df.loc[df['PPID'] == process]
    forwards = data[['ImageFileName', 'PPID', 'PID']]
    forward_pro = forwards.to_string(index=False, header=True)
    if forwards.empty:
        #print('\n')
        #print(Fore.YELLOW + '-' * 110)
        print('\n')
        print(Fore.YELLOW + process + ' Does not execute other process(es) - i.e. is not a parent process.')
        print('\n')
        print(Fore.YELLOW + '-' * 110)
        print(Fore.WHITE)
    else:
        #print('\n')
        #print(Fore.YELLOW + '-' * 110)
        print('\n')
        print(Fore.YELLOW + process + ' is a parent process of the following process(es):')
        #print('\n')
        print(Fore.WHITE)
        print(forward_pro)
        print('\n')
        print(Fore.YELLOW + '-' * 110)
        print(Fore.WHITE)
    return 0


def processes_more():
    """
    In relation to memory image. Asking user to continue finding more processes 

    """
    process_m = str(input('\nMore processes to trace y/n: ')).lower().strip()
    if process_m == 'y':
        processes()
    elif process_m == 'n':
        run.user_input()
    else:
        processes_more()
    return 0
