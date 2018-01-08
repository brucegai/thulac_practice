# use python private method to
import csv,os,numpy,math
import matplotlib
import pandas as pd
import sqlalchemy as sqla
from sklearn.preprocessing import StandardScaler
from sklearn import feature_extraction
from sklearn import feature_selection
from sklearn import linear_model

def cut_tianchi_test():
    i=0
    with open ('D:/tianchi_competition/agg_file_filter.csv', 'w',newline="") as csvwriter:
        csv_writer = csv.writer(csvwriter)
        with open('D:/tianchi_competition/agg_file.csv', 'r') as csvreader:
            csv_reader = csv.reader(csvreader)
            for line in csv_reader:
                csv_writer.writerow(line)
                i+=1
                if i==500000:
                    break

# import data and feature selection
class feature_generation:
    def __init__(self,data_group,feature_set):
        self.data_group=data_group
        self.feature_set=feature_set

    def import_data(self):
        with open ('D:/tianchi_competition/agg_file_filter.csv', 'r') as csvreader:
            csv_reader = csv.reader(csvreader)
            for line in csv_reader:
                self.data_group.append(line)
            return self.data_group

    def __get__data_group(self):
        return self.import_data()

    def __set__data_group(self,data_group):
        self.data_group=data_group

    def __get__feature_set(self):
        return self.count_ratio()

    def count_ratio(self):
        self.data_group=feature_generation.__get__data_group(self)
        list_user_merchant_click_ratio=[]
        for i in range(0,len(self.data_group)):
            list_user_merchant_click_ratio.append(self.data_group.group)
            print(self.data_group[1])


        return self.feature_set





feature_set={}
list_a=[]
method_a=feature_generation(list_a,feature_set)
method_a.count_ratio()

    # mu_age_ave=file_a.groupby(['merchant_id'])['age_range'].mean()
    # um_label_list = file_a.groupby(['user_id', 'merchant_id'])['label'].mean()
    # iu_age_ave=file_a.groupby(['item_id'])['age_range'].mean()
    # user_merchant_action=file_a.groupby(['user_id','merchant_id','item_id'])['action_type'].std()
    # user_merchant_age = file_a.groupby(['user_id', 'merchant_id', 'item_id'])['age_range'].std()
    # print(mu_age_ave,um_label_list,iu_age_ave,user_merchant_age,user_merchant_action)

# combine data
# def combine_data():
#     file_a = pd.read_csv('D:/tianchi_competition/train_format1.csv')
#     file_b = pd.read_csv('D:/tianchi_competition/user_info_format1.csv')
#     file_c = pd.read_csv('D:/tianchi_competition/user_log_format1.csv')
#     data_integrate=pd.merge(pd.merge(file_a,file_b,on="user_id"),file_c,on="user_id")
#     data_integrate.to_csv('D:/tianchi_competition/agg_file.csv')
#     return data_integrate

# filter 500000 rows of data


# def feature_selection(feature_group):
#     # linear_model.LinearRegression
#     return feature_group

# combine_data()

# cut_tianchi_test()