import csv,os,numpy,math
import matplotlib
import pandas as pd
import sqlalchemy as sqla


def import_data():
    file_a = pd.read_csv('D:/tianchi_competition/train_format1.csv')
    file_b = pd.read_csv('D:/tianchi_competition/user_info_format1.csv')
    file_c = pd.read_csv('D:/tianchi_competition/user_log_format1.csv')
    data_integrate=pd.merge(pd.merge(file_a,file_b,on="user_id"),file_c,on="user_id")
    # convert_to_array=data_integrate.as_matrix(columns="user_id")
    return data_integrate

def feature_selection():
    file=import_data()






# def predict_behavior():
#
#
#
#
# def loss_function():



# def sigmod_fun(x):
#     return 1.0/(1+math.exp(-x))

# def train_logistic_func(train_x,train_y,option_x):

import_data()
write_csv()



