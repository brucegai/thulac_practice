import pandas as pd
import csv,os
import re
import xlrd
# convert excel into csv file
# file_a=pd.read_excel('C:/sam/test1.xlsx')
# print(file_a.head(20))
# file_a.to_csv('c:/sam/test2.csv')
# NAN read as a former value
filepath_a = 'D:/sam/0103'
def iter_folder(filepath):
    childpath=[]
    path=os.listdir(filepath)
    for alldirpath in path:
        childpath.append(alldirpath)
    return childpath

def read_excel():
    filepath=iter_folder(filepath_a)
    for eachpath in filepath:
        store_name_list = []
        store_name_list_update=[]
        workbook = xlrd.open_workbook('D:/sam/0103/'+eachpath)
        sheet2 = workbook.sheet_by_index(2)
        store_name_list+=[["store number"]+[sheet2.row_values(0)[1]]]
        for i in range(13,sheet2.nrows):
            try:
                store_name_list+=[[sheet2.col_values(3)[i]]+[sheet2.col_values(4)[i]]+[sheet2.col_values(7)[i]]]
            except Exception as e:
                continue
        for j in range(0,len(store_name_list)):
            if store_name_list[j][1]=="":
                store_name_list[j][1] = store_name_list[j-1][1]
            if store_name_list[j][0]=="":
                store_name_list[j][0] = store_name_list[j-1][0]
        for m in range(1,len(store_name_list)):
            if store_name_list[m][1]==store_name_list[m-1][1]:
                if store_name_list[m][1]==store_name_list[m-1][1] and store_name_list[m][1]!=store_name_list[m-2][1]:
                    store_name_list[m].append(store_name_list[m][2]+store_name_list[m-1][2])
                elif store_name_list[m][1]==store_name_list[m-1][1] and store_name_list[m][1]==store_name_list[m-2][1]:
                    store_name_list[m].append(store_name_list[m][2]+store_name_list[m-1][3])
            else:
                store_name_list[m].append(store_name_list[m][2])
        # print(store_name_list)
        for w in range(0,len(store_name_list)):
            if store_name_list[w][1]!=store_name_list[w-1][1]:
                store_name_list_update.append(store_name_list[w])
            elif store_name_list[w][1]==store_name_list[w-1][1] and store_name_list[w][1]!=store_name_list[w+1][1]:
                store_name_list_update.append(store_name_list[w])
            else:
                continue
        print(store_name_list_update)
        return store_name_list

def calculation_sum(list_a):
    return list_a


read_excel()
