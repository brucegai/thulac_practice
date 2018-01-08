import pandas as pd
import csv,os
import xlrd,xlwt

filepath_a = 'D:/sam/0103'
def iter_folder(filepath):
    childpath=[]
    path=os.listdir(filepath)
    for alldirpath in path:
        childpath.append(alldirpath)
    return childpath

def read_excel():
    filepath=iter_folder(filepath_a)
    list_agg=[]
    file_number=len(filepath)
    j=0
    wb = xlwt.Workbook()
    ws = wb.add_sheet("sheet1")
    for eachpath in filepath:
        workbook = xlrd.open_workbook('D:/sam/0103/'+eachpath)
        sheet2 = workbook.sheet_by_index(2)
        tmp_list=deal_with_sheet(sheet2)
        tmp_list=minus_sheet(tmp_list)
        for i in range(0,len(tmp_list)):
            ws.write(1+2*j,i,tmp_list[i][0])
            ws.write(2+2*j,i,tmp_list[i][1])
        wb.save('D:/sam/0103/gai_workhard.xls')
        j+=1
        j<=file_number

def deal_with_sheet(sheet2):
    store_name_list = []
    store_name_list_update = []
    store_name_list += [["store number"] + [sheet2.row_values(0)[1]]]
    for i in range(13, sheet2.nrows):
        try:
            store_name_list += [[sheet2.col_values(3)[i]] + [sheet2.col_values(4)[i]] + [sheet2.col_values(7)[i]]]
        except Exception as e:
            continue
    for j in range(0, len(store_name_list)):
        if store_name_list[j][1] == "":
            store_name_list[j][1] = store_name_list[j - 1][1]
        if store_name_list[j][0] == "":
            store_name_list[j][0] = store_name_list[j - 1][0]
    for m in range(1, len(store_name_list)):
        if store_name_list[m][1] == store_name_list[m - 1][1]:
            if store_name_list[m][1] == store_name_list[m - 1][1] and store_name_list[m][1] != store_name_list[m - 2][1]:
                store_name_list[m].append(store_name_list[m][2] + store_name_list[m - 1][2])
            elif store_name_list[m][1] == store_name_list[m - 1][1] and store_name_list[m][1] == store_name_list[m - 2][1]:
                store_name_list[m].append(store_name_list[m][2] + store_name_list[m - 1][3])
        else:
            store_name_list[m].append(store_name_list[m][2])
    for w in range(len(store_name_list) - 1, -1, -1):
        if store_name_list[w - 1][1] != store_name_list[w][1]:
            store_name_list_update.append(store_name_list[w - 1])
            # elif store_name_list[w][1]!=store_name_list[w+1][1] and store_name_list[w][1]==store_name_list[w-1][1]:
            #     store_name_list_update.append(store_name_list[w])
    store_name_list_update.insert(0, store_name_list_update[-1])
    del store_name_list_update[-1]
    store_name_list_update.reverse()
    return store_name_list_update

def minus_sheet(list_a):
    # print(list_a)
    for i in range(1,len(list_a)):
        del list_a[i][0]
        del list_a[i][1]
    return list_a



read_excel()
