# -*- coding: utf-8 -*-
import csv,re
import requests as rq
from bs4 import BeautifulSoup
import json
import threading

#main function
def main():
    import_address_2()
    request_api()
    # filter()

# sample_api_2.csv
# test_debug.csv
# read raw file and return a list
def import_address_2():
    word_list=[]
    with open('D:/wh_0102/420100.all_tag.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        for line in csv_reader:
            word_list.append(line[1].split('^')[:2])
    print(word_list)
    return word_list

#remove all unnecessary syntax
def filter():
    source_file=import_address_2()
    i=1
    for i in range(1,len(source_file)):
        if len(source_file[i][0])==1:
            source_file[i].append("0")
        elif (source_file[i][0]=="0号")|(source_file[i][0]=="0排")|(source_file[i][0]=="0楼")|(source_file[i][0]=="0#"):
            source_file[i].append("0")
    return source_file

# request api and get result
# "http://restapi.amap.com/v3/geocode/geo?address="+address_word_list_test[i][0]+"&key=08d750b299c704dc6c9114d7261673a6&city=110000"
#http://restapi.amap.com/v3/place/text?&keywords=key&city=北京&output=json&offset=20&page=1&key=08d750b299c704dc6c9114d7261673a6&extensions=all
def request_api():
    address_word_list=filter()
    address_word_list_test=address_word_list
    address_word_type_list=[]
    address_word_type=""
    address_word=""
    different_list=[]
    different_list_filter=[]
    tag_list=[]
    with open('D:/wh_0102/wu_0102_result.csv', 'w', newline="") as csvwriter:
        csv_writer = csv.writer(csvwriter)
        for i in range(0,len(address_word_list_test)):
            # if re.search()
            key="08d750b299c704dc6c9114d7261673a6"
            #  old url request: url="http://restapi.amap.com/v3/geocode/geo?address="+address_word_list_test[i][0]+"&key=08d750b299c704dc6c9114d7261673a6&city=110000"
            url="http://restapi.amap.com/v3/place/text?&keywords="+address_word_list_test[i][0]+"&city=北京&output=json&offset=20&page=1&key=08d750b299c704dc6c9114d7261673a6&extensions=all"
            content=rq.get(url)
            content_json=json.loads(content.text)


            # make sure keyword:"geocodes" exists in api return values and then look for keywords
            if "pois" in content_json and len(content_json["pois"])>0:

                # these two objects are used in filter function
                address_word_type = content_json["pois"][0]["type"]
                address_word=address_word_list_test[i][0]
                # print(content_json["pois"][0], address_word_list_test[i][0])

                if content_json["pois"][0]["type"] in return_dict():
                    if return_dict()[content_json["pois"][0]["type"]]==address_word_list_test[i][1]:
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

                # first look for each word's return value and then see each word's type in raw file, if these two conditions
                # elif content_json["pois"][0]["type"] not in return_dict():
                #     if str(address_word_list_test[i][1]) == "13":
                #         address_word_list_test[i].append("1")

            csv_writer.writerow(address_word_list_test[i])
        # print(address_word_list_test)


        # filter gaode geocoding results based on keyword:"level" and only return words which their levels are different from original file
        for k in range(0,len(different_list)):
            if (different_list[k][0]==different_list[k-1][0] and different_list[k][1]!=different_list[k-1][1]):
                different_list_filter.append(different_list[k])
                different_list_filter.append(different_list[k - 1])

    # print(different_list)
    # print(different_list_filter)


    # output fliter result
    with open('D:/wh_0102/wu_0102_result_different_list.csv', 'w', newline="") as csvwriter:
        csv_writer_2 = csv.writer(csvwriter)
        for j in range(0, len(different_list_filter)):
            csv_writer_2.writerow(different_list_filter[j])

        return address_word_list_test
# filter function
# def compare_gaode(word,str1,number):
#     compare_list={"村庄":6,"兴趣点":13,"道路":9,"乡镇":5,"开发区":4,"热点商圈":6,"地铁站":6,"公交站台":6,"道路交叉路口":9}
#     try:
#         if compare_list[str1]!=int(number):
#             return(word,number)
#         else:
#             return(word)
#     except Exception as e:
#         print(e)

# filter function for new api
def compare_gaode_accurate(word,str1,number):
    compare_list_dict={}
    with open('E:/compare_list/compare_list.csv', 'r') as csvreader:
        csv_reader_gaode = csv.reader(csvreader)
        for line in csv_reader_gaode:
            compare_list_dict.setdefault(line[0],line[1])
    try:
        if compare_list_dict[str1]!=int(number):
            return(word,number)
        else:
            return(word)
    except Exception as e:
        print(e)

def return_dict():
    compare_list_dict = {}
    with open('E:/compare_list/compare_list.csv', 'r') as csvreader:
        csv_reader_gaode = csv.reader(csvreader)
        for line in csv_reader_gaode:
            compare_list_dict.setdefault(line[0], line[1])
    return compare_list_dict

# define multithread processing:

if __name__ == '__main__':
    main()