import processCheckingNu

import subprocess
import pandas
import userassist
#import autoscan
import re

from pandas import DataFrame
from userassist import *


from pandas import DataFrame
from userassist import *

dir_path = os.path.dirname(os.path.realpath(__file__))
file1 = dir_path + r'\csvFiles\imgs\MalAnomaly.txt'
file2 = dir_path + r'\csvFiles\imgs\MalAnomaly1.csv'
path_to_process = dir_path + r'\csvFiles\process_cmd.csv'
filename = dir_path + r'\ML\cmdModel.sav'
vectfile = dir_path + r'\ML\vecFile.sav'
path2 = dir_path + r'\csvFiles\imgs\processTrace.csv'

def analysis():
    """
       Auto analyse memory images.
    """
    pandas.set_option('display.max_rows', 30000)
    pd.options.display.max_colwidth = 10000
    frame = pd.read_csv(path_to_process, delimiter="\t", names=["PID", "Process", "Argu"], encoding='cp1252' ,header=None)
    file = open(path2, 'r')
    df_f = pd.read_csv(file, delimiter="\t",
                     names=["PID", "PPID", "ImageFileName", "Offset", "Threads", "Handles", "SessionId", "Wow64",
                            "CreateTime", "ExitTime"], header=None)
    file.close()



    with open(file1, 'r') as f:
        all_lines = [line for line in f if ".exe" in line]
        #print (targets)
        f.close()
        with open(file2, "w") as f2:
            for line in all_lines:
                f2.writelines(line)
        f2.close()


    name = ['n1','n2','n3','n4','n5','n6','n7','n8', 'n9', 'n10']
    df_col = pd.read_csv(file2, delimiter="\t", encoding='utf-8', header=None, names=name )
    ps_numbers= df_col['n1']
    process  = ps_numbers.drop_duplicates()
    process_df = pd.DataFrame(process, index=None)
    ps_string = process_df.values.flatten()

    for item in map(str, ps_string):
        print (Fore.YELLOW + '\nInformation about process Number '+Fore.RED + item )
        processCheckingNu.process_cmd_find(frame, item.strip())
        process_trace(item.strip(), df_f)
        processCheckingNu.forward_p(item.strip(), df_f)



def process_trace(p, df_f):
    df= df_f
    process = p
    s = processCheckingNu.scan_through(process=p, df=df)
    data = s[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False, header=False)
    data = list(data.split())
    # print (data)
    s0 = processCheckingNu.scan_through(data[2], df)
    lis = list()
    lis.append(data[1])

    if s0.empty or data[2] == '4' or data[2] == data[1]:

        print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
        print(Fore.WHITE)
        print('Process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
            4] + '\n' + ' has a root process of ' + ' ' + data[2])

        print(Fore.GREEN)

    else:
        data1 = data[2]
        # print (data1)
        s1 = processCheckingNu.scan_through(data1, df)
        data1 = s1[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False, header=False)
        data1 = list(data1.split())
        s1 = processCheckingNu.scan_through(data1[2], df)
        # print(data1)
        lis.append(data1[1])
        if s1.empty or data1[2] == '4' or data1[2] in lis:

            print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
            print(Fore.WHITE)
            print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                4] + ' executed by  ' + '\n' + data1[0] + '(' + data1[1] + ')' + '/' +
                  data1[3] + '-' + data1[4] + ' root process is ' + ' ' + data1[2])

            print(Fore.GREEN)


        else:
            data2 = data1[2]
            # print(data2)
            s2 = processCheckingNu.scan_through(data2, df)
            data2 = s2[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False,
                                                                                             header=False)
            data2 = list(data2.split())
            s2 = processCheckingNu.scan_through(data2[2], df)
            # print(data2)
            lis.append(data2[1])
            if s2.empty or data2[2] == '4' or data2[2] in lis:

                print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
                print(Fore.WHITE)

                print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                    4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                      data1[3] + '-' + data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[3] + '-' +
                      data2[4] + ' root process is ' + '  ' + data2[2])

                print(Fore.GREEN)


            else:
                data3 = data2[2]
                # print(data3)
                s3 = processCheckingNu.scan_through(data3, df)
                data3 = s3[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False,
                                                                                                 header=False)
                data3 = list(data3.split())
                s3 = processCheckingNu.scan_through(data3[2], df)
                # print(data3)
                lis.append(data3[1])
                if s3.empty or data3[2] == '4' or data3[2] in lis:

                    print(Fore.YELLOW + '\n\nProcess traceability coupled with time executions of each process\n')
                    print(Fore.WHITE)
                    print('process ' + data[0] + '(' + process + ')' + '/' + data[3] + '-' + data[
                        4] + ' executed by  ' + '\n' + ' ' + data1[0] + '(' + data1[1] + ')' + '/' +
                          data1[3] + '-' + data1[4] + ' <- ' + data2[0] + '(' + data2[1] + ')' + '/' + data2[
                              3] + '-' +
                          data2[4] + ' <- ' + data3[0] + '(' + data3[1] + ')' + '/' + data3[3] + '-' + data3[4]
                          + ' root process is ' + ' ' + data3[2])

                    print(Fore.GREEN)


                else:
                    data4 = data3[2]
                    # print(data4)
                    s4 = processCheckingNu.scan_through(data4, df)
                    data4 = s4[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(index=False,
                                                                                                     header=False)
                    data4 = list(data4.split())
                    s4 = processCheckingNu.scan_through(data4[2], df)
                    # print(data4)
                    lis.append(data4[1])
                    if s4.empty or data4[2] == '4' or data4[2] in lis:

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

                        print(Fore.GREEN)

                    else:
                        data5 = data4[2]
                        # print(data5)
                        s5 = processCheckingNu.scan_through(data5, df)
                        data5 = s5[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                            index=False,
                            header=False)
                        data5 = list(data5.split())
                        s5 = processCheckingNu.scan_through(data5[2], df)
                        # print(data5)
                        lis.append(data5[1])
                        if s5.empty or data5[2] == '4' or data5[2] in lis:

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

                            print(Fore.GREEN)


                        else:
                            data6 = data5[2]
                            # print(data6)
                            s6 = processCheckingNu.scan_through(data6, df)
                            data6 = s6[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                index=False, header=False)
                            data6 = list(data6.split())
                            s6 = processCheckingNu.scan_through(data6[2], df)
                            # print(data6)
                            lis.append(data6[1])
                            if s6.empty or data6[2] == '4' or data6[2] in lis:

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

                                print(Fore.GREEN)


                            else:
                                data7 = data6[2]
                                # print(data7)
                                s7 = processCheckingNu.scan_through(data7, df)
                                data7 = s7[['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                    index=False, header=False)
                                data7 = list(data7.split())
                                s7 = processCheckingNu.scan_through(data7[2], df)
                                # print(data7)
                                lis.append(data7[1])
                                if s7.empty or data7[2] == '4' or data7[2] in lis:

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

                                    # print ('\n')
                                    print(Fore.GREEN)


                                else:
                                    data8 = data7[2]
                                    # print(data8)
                                    s8 = processCheckingNu.scan_through(data8, df)
                                    data8 = s8[
                                        ['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                        index=False, header=False)
                                    data8 = list(data8.split())
                                    s8 = processCheckingNu.scan_through(data8[2], df)
                                    # print(data8)
                                    lis.append(data8[1])
                                    if s8.empty or data8[2] == '4' or data8[2] in lis:

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

                                        # print ('\n')
                                        print(Fore.GREEN)


                                    else:
                                        data9 = data8[2]
                                        # print(data9)
                                        s9 = processCheckingNu.scan_through(data9, df)
                                        data9 = s9[
                                            ['ImageFileName', 'PID', 'PPID', "CreateTime", "ExitTime"]].to_string(
                                            index=False, header=False)
                                        data9 = list(data9.split())
                                        s9 = processCheckingNu.scan_through(data9[2], df)
                                        # print(data9)
                                        lis.append(data9[1])
                                        if s9.empty or data9[2] == '4' or data9[2] in lis:

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

                                            # print ('\n')
                                            print(Fore.GREEN)


                                        else:
                                            data10 = data9[2]
                                            # print(data10)
                                            s10 = processCheckingNu.scan_through(data10, df)
                                            data10 = s10[['ImageFileName', 'PID', 'PPID', "CreateTime",
                                                          "ExitTime"]].to_string(index=False, header=False)
                                            data10 = list(data10.split())
                                            s10 = processCheckingNu.scan_through(data10[2], df)
                                            # print(data10)
                                            lis.append(data10[1])
                                            if s10.empty or data10[2] == '4' or data10[2] in lis:

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

                                                print(Fore.GREEN)


                                            else:
                                                print('\n')
                                                print('\nTraceability: Maximum of 10 proceeses')


    return 0
