import forRunningProcesses
import os
import run


import pandas as pd
from colorama import Fore
from pandas import DataFrame

dir_path = os.path.dirname(os.path.realpath(__file__))


def live_process():
    """
    Identify live processes in combination with traceability combined with ML.
    """
    wmic = 'wmic /output:' + dir_path + r'\csvFiles\Process.csv' + ' ' + 'process get Caption,ParentProcessId,' \
                                                                         'ProcessId,CommandLine /format:csv '
    os.system(wmic)

    output_ml = dir_path + r'\csvFiles\Process.csv'

    df = pd.read_csv(output_ml, delimiter=',', encoding='utf-16',
                     names=['Services', 'CommandLine', 'ParentProcessId', 'ProcessId'], header=None)

    df1 = df[['Services', 'ParentProcessId', 'ProcessId']]
    print(Fore.WHITE)
    grouped = df1.groupby(df1['ParentProcessId'])
    for name, group in grouped:
        print('\n')
        print(name)
        print(DataFrame(group).to_string(index=False, header=True))
    print('\n')
    print(Fore.YELLOW + 'Above output represents clusters, organised according to their parent processes')
    print(Fore.GREEN)
    print('Type Process ID for traceability')
    process = input('Enter  process ID : ')

    if process.isdigit():

        s = forRunningProcesses.loop_through(process, df)
        data = s[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(index=False, header=False)

        data = list(data.split())
        # print (data)
        s0 = forRunningProcesses.loop_through(data[2], df)
        f_ind = df.loc[df['ProcessId'] == data[1]]
        ist = list()
        ist.append(data[1])
        # print (s0)
        if s0.empty or data[2] == '4' or data[2] == data[1]:
            print('\n')
            print(Fore.YELLOW + 'Process traceability\n')
            print(Fore.WHITE)
            print('Process ' + data[0] + '(' + process + ')' + ' has a root process of ' + ' ' + data[2])

            print('\n')
            print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
            print(Fore.WHITE)
            p = f_ind[['Services', 'CommandLine']]
            print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
            forRunningProcesses.process_ml(p)
            print(Fore.WHITE)
            print('-----------------------------------')
            forRunningProcesses.forward_process(process, df)
            print(Fore.GREEN)
            forRunningProcesses.more_processes()

        else:
            data1 = data[2]
            # print (data1)
            s1 = forRunningProcesses.loop_through(data1, df)
            data1 = s1[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(index=False, header=False)
            data1 = list(data1.split())
            s1 = forRunningProcesses.loop_through(data1[2], df)
            # print(data1)
            f_ind1 = df.loc[df['ProcessId'] == data1[1]]
            ist.append(data1[1])
            if s1.empty or data1[2] == '4' or data1[2] in ist:
                print('\n')
                print(Fore.YELLOW + 'Process traceability \n')
                print(Fore.WHITE)
                print('process ' + data[0] + '(' + process + ')' + ' executed by  ' + data1[0] + '(' + data1[
                    1] + ')' + ' root process is ' + ' ' + data1[2])
                print('\n')
                print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                print(Fore.WHITE)
                p = f_ind[['Services', 'CommandLine']]
                print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                forRunningProcesses.process_ml(p)
                print(Fore.WHITE)
                print('-----------------------------------')
                print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=True))
                print('-----------------------------------')
                forRunningProcesses.forward_process(process, df)

                print(Fore.GREEN)
                forRunningProcesses.more_processes()

            else:
                data2 = data1[2]
                # print(data2)
                s2 = forRunningProcesses.loop_through(data2, df)
                data2 = s2[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(index=False,
                                                                                                  header=False)
                data2 = list(data2.split())
                s2 = forRunningProcesses.loop_through(data2[2], df)
                # print(data2)

                f_ind2 = df.loc[df['ProcessId'] == data2[1]]

                ist.append(data2[1])
                if s2.empty or data2[2] == '4' or data2[2] in ist:
                    print('\n')
                    print(Fore.YELLOW + 'Process traceability \n')
                    print(Fore.WHITE)
                    print('process ' + data[0] + '(' + process + ')' ' executed by  ' + '\n' + ' ' + data1[0] + '(' +
                          data1[1] + ')' + ' <- ' + data2[0] + '(' + data2[1] + ')'
                          + ' root process is ' + '  ' + data2[2])

                    print('\n')
                    print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                    print(Fore.WHITE)
                    p = f_ind[['Services', 'CommandLine']]
                    print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                    forRunningProcesses.process_ml(p)
                    print(Fore.WHITE)
                    print('-----------------------------------')
                    print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=True))
                    print('-----------------------------------')
                    print(f_ind2[['Services', 'CommandLine']].to_string(index=False, header=True))
                    forRunningProcesses.forward_process(process, df)

                    print(Fore.GREEN)
                    forRunningProcesses.more_processes()

                else:
                    data3 = data2[2]
                    # print(data3)
                    s3 = forRunningProcesses.loop_through(data3, df)
                    data3 = s3[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(index=False,
                                                                                                      header=False)
                    data3 = list(data3.split())
                    s3 = forRunningProcesses.loop_through(data3[2], df)

                    # print(data3)
                    f_ind3 = df.loc[df['ProcessId'] == data3[1]]
                    # print (Fore.YELLOW)
                    # print (f_ind3)
                    ist.append(data3[1])
                    if s3.empty or data3[2] == '4' or data3[2] in ist:
                        print('\n')
                        print(Fore.YELLOW + 'Process traceability \n')
                        print(Fore.WHITE)
                        print('process ' + data[0] + '(' + process + ')' + ' executed by  ' + '\n' + ' ' + data1[
                            0] + '(' + data1[1] + ')'
                              + ' <- ' + data2[0] + '(' + data2[1] + ')'
                              + ' <- ' + data3[0] + '(' + data3[1] + ')'
                              + ' root process is ' + ' ' + data3[2])
                        print('\n')
                        print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                        print(Fore.WHITE)
                        p = f_ind[['Services', 'CommandLine']]
                        print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                        forRunningProcesses.process_ml(p)
                        print(Fore.WHITE)
                        print('-----------------------------------')
                        print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=True))
                        print('-----------------------------------')
                        print(f_ind2[['Services', 'CommandLine']].to_string(index=False, header=True))
                        print('-----------------------------------')
                        print(f_ind3[['Services', 'CommandLine']].to_string(index=False, header=True))
                        print('-----------------------------------')
                        forRunningProcesses.forward_process(process, df)

                        print(Fore.GREEN)
                        forRunningProcesses.more_processes()

                    else:
                        data4 = data3[2]
                        # print(data4)
                        s4 = forRunningProcesses.loop_through(data4, df)
                        data4 = s4[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(index=False,
                                                                                                          header=False)
                        data4 = list(data4.split())
                        s4 = forRunningProcesses.loop_through(data4[2], df)
                        f_ind4 = df.loc[df['ProcessId'] == data4[1]]
                        ist.append(data4[1])
                        # print(data4)
                        if s4.empty or data4[2] == '4' or data4[2] in ist:
                            print('\n')
                            print(Fore.YELLOW + 'Process traceability \n')
                            print(Fore.WHITE)
                            print('process ' + data[0] + '(' + process + ')' + ' executed by  ' + '\n' + ' ' + data1[
                                0] + '(' + data1[1] + ')' + ' <- ' + data2[0]
                                  + '(' + data2[1] + ')' + ' <- ' + data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[
                                      0] + '(' + data4[1] + ')'
                                  + ' ' + ' root process is ' + ' ' + data4[2])
                            print('\n')
                            print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                            print(Fore.WHITE)
                            p = f_ind[['Services', 'CommandLine']]
                            print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                            forRunningProcesses.process_ml(p)
                            print(Fore.WHITE)
                            print('-----------------------------------')
                            print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=False))
                            print('-----------------------------------')
                            print(f_ind2[['Services', 'CommandLine']].to_string(index=False, header=False))
                            print('-----------------------------------')
                            print(f_ind3[['Services', 'CommandLine']].to_string(index=False, header=False))
                            print('-----------------------------------')
                            print(f_ind4[['Services', 'CommandLine']].to_string(index=False, header=False))
                            forRunningProcesses.forward_process(process, df)

                            print(Fore.GREEN)
                            forRunningProcesses.more_processes()

                        else:
                            data5 = data4[2]
                            # print(data5)
                            s5 = forRunningProcesses.loop_through(data5, df)
                            data5 = s5[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(
                                index=False,
                                header=False)
                            data5 = list(data5.split())
                            s5 = forRunningProcesses.loop_through(data5[2], df)
                            f_ind5 = df.loc[df['ProcessId'] == data5[1]]
                            # print(data5)
                            ist.append(data5[1])
                            if s5.empty or data5[2] == '4' or data5[2] in ist:
                                print('\n')
                                print(Fore.YELLOW + 'Process traceability \n')
                                print(Fore.WHITE)
                                print('process ' + data[0] + '(' + process + ')' +
                                      ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + ' <- ' + data2[
                                          0] +
                                      '(' + data2[1] + ')' + ' <- ' + data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[
                                          0] + '(' + data4[1] + ')' + ' <- ' +
                                      data5[0] + '(' + data5[1] + ')'
                                      + ' root process is ' + ' ' + data5[2])
                                print('\n')
                                print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                                print(Fore.WHITE)
                                p = f_ind[['Services', 'CommandLine']]
                                print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                                forRunningProcesses.process_ml(p)
                                print(Fore.WHITE)
                                print('-----------------------------------')
                                print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=False))
                                print('-----------------------------------')
                                print(f_ind2[['Services', 'CommandLine']].to_string(index=False, header=False))
                                print('-----------------------------------')
                                print(f_ind3[['Services', 'CommandLine']].to_string(index=False, header=False))
                                print('-----------------------------------')
                                print(f_ind4[['Services', 'CommandLine']].to_string(index=False, header=False))
                                print('-----------------------------------')
                                print(f_ind5[['Services', 'CommandLine']].to_string(index=False, header=False))
                                forRunningProcesses.forward_process(process, df)

                                print(Fore.GREEN)
                                forRunningProcesses.more_processes()

                            else:
                                data6 = data5[2]
                                # print(data6)
                                s6 = forRunningProcesses.loop_through(data6, df)
                                data6 = s6[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(
                                    index=False, header=False)
                                data6 = list(data6.split())
                                s6 = forRunningProcesses.loop_through(data6[2], df)
                                f_ind6 = df.loc[df['ProcessId'] == data6[1]]
                                # print(data6)
                                ist.append(data6[1])
                                if s6.empty or data6[2] == '4' or data6[2] in ist:
                                    print('\n')
                                    print(Fore.YELLOW + 'Process traceability \n')
                                    print(Fore.WHITE)
                                    print('process ' + data[0] + '(' + process + ')' + ' executed by  ' + '\n' + ' ' +
                                          data1[0] + '(' + data1[1] + ')'
                                          + ' <- ' + data2[0] + '(' + data2[1] + ')' + ' <- ' +
                                          data3[0] + '(' + data3[1] + ')'  ' <- ' + data4[0] + '(' + data4[
                                              1] + ')' + ' <- ' +
                                          data5[0] + '(' + data5[1] + ')' + ' <- ' + data6[0] + '(' + data6[1] + ')'
                                          + ' root process is ' + ' ' + data6[2])

                                    print('\n')
                                    print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                                    print(Fore.WHITE)
                                    p = f_ind[['Services', 'CommandLine']]
                                    print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                                    forRunningProcesses.process_ml(p)
                                    print(Fore.WHITE)
                                    print('-----------------------------------')
                                    print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=False))
                                    print('-----------------------------------')
                                    print(f_ind2[['Services', 'CommandLine']].to_string(index=False, header=False))
                                    print('-----------------------------------')
                                    print(f_ind3[['Services', 'CommandLine']].to_string(index=False, header=False))
                                    print('-----------------------------------')
                                    print(f_ind4[['Services', 'CommandLine']].to_string(index=False, header=False))
                                    print('-----------------------------------')
                                    print(f_ind5[['Services', 'CommandLine']].to_string(index=False, header=False))
                                    print('-----------------------------------')
                                    print(f_ind6[['Services', 'CommandLine']].to_string(index=False, header=False))
                                    forRunningProcesses.forward_process(process, df)

                                    print(Fore.GREEN)
                                    forRunningProcesses.more_processes()

                                else:
                                    data7 = data6[2]
                                    # print(data7)
                                    s7 = forRunningProcesses.loop_through(data7, df)
                                    data7 = s7[['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(
                                        index=False, header=False)
                                    data7 = list(data7.split())
                                    s7 = forRunningProcesses.loop_through(data7[2], df)
                                    f_ind7 = df.loc[df['ProcessId'] == data7[1]]
                                    # print(data7)
                                    ist.append(data7[1])
                                    if s7.empty or data7[2] == '4' or data7[2] in ist:
                                        print('\n')
                                        print(Fore.YELLOW + 'Process traceability \n')
                                        print(Fore.WHITE)
                                        print(
                                            'process ' + data[0] + '(' + process + ')' + ' executed by  ' + '\n' + ' ' +
                                            data1[0] + '(' + data1[
                                                1] + ')' + ' <- ' + data2[0] + '(' + data2[1] + ')' + ' <- ' +
                                            data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[0] + '(' + data4[
                                                1] + ')' + ' <- ' +
                                            data5[0] + '(' + data5[1] + ')' + ' <- ' + data6[0] + '(' + data6[
                                                1] + ')' + ' <- ' + data7[0] + '(' + data7[1] + ')'
                                            + ' root process is ' + ' ' +
                                            data7[2])
                                        print('\n')
                                        print(Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                                        print(Fore.WHITE)
                                        p = f_ind[['Services', 'CommandLine']]
                                        print(f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                                        forRunningProcesses.process_ml(p)
                                        print(Fore.WHITE)
                                        print('-----------------------------------')
                                        print(f_ind1[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        print('-----------------------------------')
                                        print(f_ind2[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        print('-----------------------------------')
                                        print(f_ind3[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        print('-----------------------------------')
                                        print(f_ind4[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        print('-----------------------------------')
                                        print(f_ind5[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        print('-----------------------------------')
                                        print(f_ind6[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        print('-----------------------------------')
                                        print(f_ind7[['Services', 'CommandLine']].to_string(index=False, header=False))
                                        forRunningProcesses.forward_process(process, df)

                                        print(Fore.GREEN)
                                        forRunningProcesses.more_processes()

                                    else:
                                        data8 = data7[2]
                                        # print(data8)
                                        s8 = forRunningProcesses.loop_through(data8, df)
                                        data8 = s8[
                                            ['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(
                                            index=False, header=False)
                                        data8 = list(data8.split())
                                        s8 = forRunningProcesses.loop_through(data8[2], df)
                                        f_ind8 = df.loc[df['ProcessId'] == data8[1]]
                                        # print(data8)
                                        ist.append(data8[1])
                                        if s8.empty or data8[2] == '4' or data8[2] in ist:
                                            print('\n')
                                            print(Fore.YELLOW + 'Process traceability \n')
                                            print(Fore.WHITE)
                                            print('process ' + data[
                                                0] + '(' + process + ')' + '/' + ' executed by  ' + '\n' + ' ' +
                                                  data1[0] + '(' + data1[1] + ')' + ' <- ' + data2[0] + '(' + data2[
                                                      1] + ')' + ' <- ' +
                                                  data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[0] + '(' + data4[
                                                      1] + ')' + ' <- ' +
                                                  data5[0] + '(' + data5[1] + ')' + ' <- ' + data6[0] + '(' + data6[
                                                      1] + ')' + ' <- ' + data7[0] + '(' +
                                                  data7[1] + ')' + ' <- ' + data8[
                                                      0] + '(' + data8[1] + ')' + ' root process is ' +
                                                  data8[2])

                                            print('\n')
                                            print(
                                                Fore.YELLOW + 'Involved Commands if exist - read from top to bottom:\n')
                                            print(Fore.WHITE)
                                            p = f_ind[['Services', 'CommandLine']]
                                            print(
                                                f_ind[['Services', 'CommandLine']].to_string(index=False, header=True))
                                            forRunningProcesses.process_ml(p)
                                            print(Fore.WHITE)
                                            print('-----------------------------------')
                                            print(f_ind1[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind2[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind3[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind4[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind5[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind6[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind7[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            print('-----------------------------------')
                                            print(f_ind8[['Services', 'CommandLine']].to_string(index=False,
                                                                                                header=False))
                                            forRunningProcesses.forward_process(process, df)

                                            print('\n')
                                            print(Fore.GREEN)
                                            forRunningProcesses.more_processes()

                                        else:
                                            data9 = data8[2]
                                            # print(data9)
                                            s9 = forRunningProcesses.loop_through(data9, df)
                                            data9 = s9[
                                                ['Services', 'ProcessId', 'ParentProcessId', 'CommandLine']].to_string(
                                                index=False, header=False)
                                            data9 = list(data9.split())
                                            s9 = forRunningProcesses.loop_through(data9[2], df)
                                            f_ind9 = df.loc[df['ProcessId'] == data9[1]]
                                            # print(data9)
                                            ist.append(data9[1])
                                            if s9.empty or data9[2] == '4' or data9[2] in ist:
                                                print('\n')
                                                print(Fore.YELLOW + 'Process traceability \n')
                                                print(Fore.WHITE)
                                                print('process ' + data[
                                                    0] + '(' + process + ')' + ' executed by  ' + '\n' + ' ' +
                                                      data1[0] + '(' + data1[1] + ')' + ' <- ' + data2[0] + '(' + data2[
                                                          1] + ')' + ' <- ' +
                                                      data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[0] + '(' + data4[
                                                          1] + ')' + ' <- ' +
                                                      data5[0] + '(' + data5[1] + ')' + ' <- ' + data6[0] + '(' + data6[
                                                          1] + ')' + ' <- ' +
                                                      data7[0] + '(' + data7[1] + ')' + ' <- ' + data8[0] + '(' + data8[
                                                          1] + ')' + ' <- ' +
                                                      data9[0] + '(' + data9[1] + ')' + ' root process is ' + ' ' +
                                                      data9[2])
                                                print('\n')
                                                print(
                                                    Fore.YELLOW + 'Involved Commands if exist - read from top to '
                                                                  'bottom:\n')
                                                print(Fore.WHITE)
                                                p = f_ind[['Services', 'CommandLine']]
                                                print(f_ind[['Services', 'CommandLine']].to_string(index=False,
                                                                                                   header=True))
                                                forRunningProcesses.process_ml(p)
                                                print(Fore.WHITE)
                                                print('-----------------------------------')
                                                print(f_ind1[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind2[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind3[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind4[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind5[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind6[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind7[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind8[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                print('-----------------------------------')
                                                print(f_ind9[['Services', 'CommandLine']].to_string(index=False,
                                                                                                    header=False))
                                                forRunningProcesses.forward_process(process, df)

                                                print('\n')
                                                print(Fore.GREEN)
                                                forRunningProcesses.more_processes()

                                            else:
                                                data10 = data9[2]
                                                # print(data10)
                                                s10 = forRunningProcesses.loop_through(data10, df)
                                                data10 = s10[['Services', 'ProcessId', 'ParentProcessId',
                                                              'CommandLine']].to_string(index=False, header=False)
                                                data10 = list(data10.split())
                                                s10 = forRunningProcesses.loop_through(data10[2], df)
                                                f_ind10 = df.loc[df['ProcessId'] == data10[1]]
                                                # print(data10)
                                                ist.append(data10[1])
                                                if s10.empty or data10[2] == '4' or data10[2] in ist:
                                                    print('\n')
                                                    print(Fore.YELLOW + 'Process traceability \n')
                                                    print(Fore.WHITE)
                                                    print('process ' + data[
                                                        0] + '(' + process + ')' + ' exEcuted by  ' + '\n' + ' ' +
                                                          data1[0] + '(' + data1[1] + ')' + ' <- ' + data2[0] + '(' +
                                                          data2[1] + ')' + ' <- ' +
                                                          data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[0] + '(' +
                                                          data4[1] + ')' + ' <- ' +
                                                          data5[0] + '(' + data5[1] + ')' + ' <- ' + data6[0] + '(' +
                                                          data6[1] + ')' + ' <- ' + data7[0] + '(' +
                                                          data7[1] + ')'  ' <- ' + data8[0] + '(' + data8[
                                                              1] + ')' + ' <- ' + data9[0] + '(' + data9[1] + ')'
                                                          + ' <- ' + data10[0] + '(' + data10[1]
                                                          + ')' + ' root process is ' + ' ' + data10[2])
                                                    print('\n')
                                                    print(
                                                        Fore.YELLOW + 'Involved Commands if exist - read from top to '
                                                                      'bottom:\n')
                                                    print(Fore.WHITE)
                                                    p = f_ind[['Services', 'CommandLine']]
                                                    print(f_ind[['Services', 'CommandLine']].to_string(index=False,
                                                                                                       header=True))
                                                    forRunningProcesses.process_ml(p)
                                                    print(Fore.WHITE)
                                                    print('-----------------------------------')
                                                    print(f_ind1[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind2[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind3[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind4[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind5[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind6[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind7[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind8[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind9[['Services', 'CommandLine']].to_string(index=False,
                                                                                                        header=False))
                                                    print('-----------------------------------')
                                                    print(f_ind10[['Services', 'CommandLine']].to_string(index=False,
                                                                                                         header=False))
                                                    print('\n')
                                                    forRunningProcesses.forward_process(process, df)

                                                    print(Fore.GREEN)
                                                    forRunningProcesses.more_processes()

                                                else:
                                                    data11 = data10[2]
                                                    # print(data11)
                                                    s11 = forRunningProcesses.loop_through(data11, df)
                                                    data11 = s11[['Services', 'ProcessId', 'ParentProcessId',
                                                                  'CommandLine']].to_string(index=False, header=False)
                                                    data11 = list(data11.split())
                                                    s11 = forRunningProcesses.loop_through(data11[2], df)
                                                    f_ind11 = df.loc[df['ProcessId'] == data11[1]]
                                                    # print(data11)
                                                    ist.append(data11[1])
                                                    if s11.empty or data11[2] == '4' or data11[2] in ist:
                                                        print(Fore.YELLOW + 'Process traceability \n')
                                                        print(Fore.WHITE)
                                                        print('process ' + data[
                                                            0] + '(' + process + ')' + ' executed by  ' + '\n' + ' ' +
                                                              data1[0] + '(' + data1[1] + ')' + ' <- ' + data2[
                                                                  0] + '(' + data2[1] + ')' + ' <- ' +
                                                              data3[0] + '(' + data3[1] + ')' + ' <- ' + data4[
                                                                  0] + '(' + data4[1] + ')' + ' <- ' +
                                                              data5[0] + '(' + data5[1] + ')' + ' <- ' + data6[
                                                                  0] + '(' + data6[1] + ')' + ' <- ' + data7[0] + '(' +
                                                              data7[1] + ')'  ' <- ' + data8[0] + '(' + data8[
                                                                  1] + ')' + ' <- ' + data9[0] + '(' + data9[1] + ')'
                                                              + ' <- ' + data10[0] + '(' + data10[1]
                                                              + ')' + ' <- ' + data11[0] + '(' + data11[1]
                                                              + ' root process is ' + ' ' + data11[2])
                                                        print('\n')
                                                        print(
                                                            Fore.YELLOW + 'Involved Commands if exist - read from top '
                                                                          'to bottom:\n')
                                                        print(Fore.WHITE)
                                                        p = f_ind[['Services', 'CommandLine']]
                                                        print(f_ind[['Services', 'CommandLine']].to_string(index=False,
                                                                                                           header=True))
                                                        forRunningProcesses.process_ml(p)
                                                        print(Fore.WHITE)
                                                        print('-----------------------------------')
                                                        print(f_ind1[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind2[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind3[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind4[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind5[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind6[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind7[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False))
                                                        print('-----------------------------------')
                                                        print(f_ind8[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False)
                                                              )
                                                        print('-----------------------------------')
                                                        print(f_ind9[['Services', 'CommandLine']].to_string(index=False,
                                                                                                            header=False)
                                                              )
                                                        print('-----------------------------------')
                                                        print(
                                                            f_ind10[['Services', 'CommandLine']].to_string(index=False,
                                                                                                           header=False)
                                                        )
                                                        print('-----------------------------------')
                                                        print(
                                                            f_ind11[['Services', 'CommandLine']].to_string(index=False,
                                                                                                           header=False)
                                                        )
                                                        print('\n')
                                                        forRunningProcesses.forward_process(process, df)
                                                        print(Fore.GREEN)
                                                        forRunningProcesses.more_processes()

                                                    else:
                                                        print(Fore.YELLOW)
                                                        print('\n')
                                                        print('\nTraceability: Maximum of 11 processes')
                                                        live_process()
    else:
        print(Fore.YELLOW + 'Wrong  process ID, trying again')
        live_process()

    return run.user_input()
