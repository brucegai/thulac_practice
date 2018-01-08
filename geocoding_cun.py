#
from bs4 import BeautifulSoup
import re,csv,os,six,itertools
import pandas
import sys,time
import json,multiprocessing
import logging
import requests
import urllib.request as urlreq
import urllib.parse as urlpse
import tensorflow as tf
from gensim.models import word2vec as wv
import matplotlib as mtb
from collections import Counter

def read_data():
    csv_reader = open('D:/cun.csv', "r")
    for row in csv_reader:
        print (row)
    csv_reader.close()

def transform(filename):
    url='http://restapi.amap.com/v3/geocode/geo?key=a755f2f36ba0d82b835b84d3ba74e218'
    request_url=""
    address=""
    city="深圳"
    request_result=""
    json_result=""
    geocoding_result=""
    not_available_list=""
    each_row_=""
    valid_address_street=""
    csv_reader = open('D:/cun.csv', "r")
    for row in csv_reader:
        each_row=row.split(',')[2]
        address=each_row.split('^')[0]
        # print (address)
        #wv.word2phrase()
    json_reader=open('D:/base.json',encoding='utf-8')
    json_file=json.load(json_reader)
    #print(json_file)
    for item in json_file:
        try:
            sparate_address=item['segmentation']
            valid_address=str(sparate_address).split(',')[2]
            valid_address=valid_address.strip("'").split("'")[1]
            #print(valid_address)
            if re.search('路',valid_address)!=None:
                if valid_address not in valid_address_street:
                    valid_address_street+=valid_address+","
        except:
            #print("wrong value")
            continue
    #print (valid_address_street)
    return valid_address_street

def automatic_clean_of_province():
    state_info_group=""
    city_info_group=""
    address_info_group=""
    numbers=""
    csv_reader = open('D:/hz_nodiff_0703.csv', "r")
    for row in csv_reader:
        try:
            address_sep=row.split(',')[2]
            number = re.findall(r'\d+', address_sep)
            number = str(number)
            if (number.split(',')[0].strip("['"))==str(1):
                state_info=address_sep.split('(')[0]
                if re.search("浙江",state_info)!=None:
                    state_info_group+=state_info+"\n"
                elif(re.search("浙江",state_info)==None):
                    state_info_group+="bad state info"+"\n"
            else:
                state_info_group += "bad state info" + "\n"
            # district_info=address_sep.split('(')[2].split(')')[1]
            # secondary_district_info=address_sep.split('(')[3].split(')')[1]
            # POI_info=address_sep.split('(')[4].split(')')[1]
            #print(state_info,len(state_info),city_info,district_info)
            # cleanning of province
            # write another line in csv file
        except:
            print("skip")
    print(type(state_info_group))
    return state_info_group

def clean_of_city():
    city_info_group = ""
    city_info=""
    csv_reader = open('D:/hz_nodiff_0703.csv', "r")
    for row in csv_reader:
        try:
            address_sep = row.split(',')[2]
            number = re.findall(r'\d+', address_sep)
            number = str(number)
            if (number.split(',')[1].strip("['").split("'")[1]) == str(2):
                city_info = address_sep.split('(')[1].split(')')[1]
                if (re.search("杭州", city_info) != None) and (len(city_info) < 4):
                    city_info_group += city_info + "\n"
                elif (re.search("杭州", city_info) == None):
                    city_info_group += "bad city info" + "\n"
            else:
                city_info_group+= "bad city info" + "\n"
        except:
            print("skip city")
    print(type(city_info_group))
    return city_info_group

def clean_of_district():
    # third position info, could be district or street or POI or village, extract useful info into training
    ditrict_info=""
    district_info_group=[]
    new_district=[]
    cixing=""
    cixing_count={}
    csv_reader = open('D:/hz_nodiff_0703.csv', "r")
    available_district=""
    wv_output=""
    for row in csv_reader:
        try:
            district_sep=row.split(',')[2]
            number = re.findall(r'\d+', district_sep)
            number = str(number)
            cixing+=number.split(',')[2].strip("['").split("'")[1]+"\n"
            if (split_function(number)==str(3))|(split_function(number)==str(5))|(split_function(number)==str(9))|(split_function(number)==str(4))|(split_function(number)==str(13)):
                district_info = district_sep.split('(')[2].split(')')[1]
                district_info_group.append(district_info)
                available_district+=district_info+","
            else:
                district_info_group .append( "bad district info" )
        except:
            print("error")
    new_district = []
    i=1
    while i<=len(district_info_group):
        if new_district.count(district_info_group[i]) < 1000 and district_info_group[i]!="bad district info":
            new_district.append(district_info_group[i])
        else:
            continue
        i+=1


    print(new_district)

    with open('D:/word_train_2.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for item in new_district:
            item=re.sub(',','',item)
            csv_writer.writerow(item)
    # print (available_district)
    # with open('D:/word_train.csv', 'w', newline='') as csvfile:
    #     csv_writer=csv.writer(csvfile,delimiter=' ')
    #     for item in available_district:
    #         csv_writer.writerow(item)
    return district_info_group

def remove_surplus(x):
    return_list=[]
    for item in x:
        while return_list.count(item)<1000:
            return_list.append(item)
    return (return_list)


def convert_comma():
    csv_reader = open('D:/word_train_2.csv', "r")
    for row in csv_reader:
        row = re.sub(r',', '', row)



def word_2_vec_train():
    # train a model, initialize a mode, output wordvector
    x=wv.Word2Vec.load_word2vec_format('D:/word_train_2.txt')
    print(x.vectors)

def split_function(x):
    result=x.split(',')[2].strip("['").split("'")[1]
    return result


def combine_info():
    city_list=clean_of_city().split("\n")
    province_list=automatic_clean_of_province().split("\n")
    district_list=clean_of_district().split("\n")
    address_list=""
    try:
        for i in range(len(province_list)):
            address_list += province_list[i] + "," +city_list[i]+","+district_list[i]+"\n"
    except:
        print("unmatch index")
    return address_list


def summary_of_itemlist():
    address_item=""

# word_2_vec_train()
clean_of_district()
# convert_comma()
# automatic_clean_of_province()
# clean_of_city()
#combine_info()
# transform('D:\cun.csv')

# def write_doc(x):
#     csv_writer=open('D:/cun.csv', "w")
#     for row in csv_writer:
#         row.writerow()

    # for i in json_file:
    #     address_info=i['segementation']
    #     print (address_info)

        # gaode geocoding part
        # request_url = url + "&" + "city=" + "深圳" + "&" + "address=" + address
        # print (type(request_url))
        # #request_url_2=urlpse.quote(request_url)
        # #print (request_url_2)
        # request_result=urlreq.urlopen(request_url)
        # json_result=json.load(request_result)
        # print (json_result['geocoding'])
    #     geocoding_result=json_result['geocoding']
    #     if geocoding_result==None:
    #         not_available_list+=geocoding_result
    # #
    # #
    # print(request_result,not_available_list)
    # csv_reader.close()


# def convert_None(x):
#     while type(x)=="NoneType":
#




#def geocoding