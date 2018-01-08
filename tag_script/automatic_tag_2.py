# -*- coding: utf-8 -*-
import csv,re
import requests as rq
from bs4 import BeautifulSoup
import json


#main function
def main():
    # import_address_2()
    request_api()
    # filter()

# sample_api_2.csv
# test_debug.csv
# read raw file and return a list
def import_address_2():
    word_list=[]
    with open('E:/test_debug.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        next(csv_reader)
        for line in csv_reader:
            word_list.append(line[2].split('^')[:2])
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
def request_api():
    address_word_list=filter()
    address_word_list_test=address_word_list
    address_word_type_list=[]
    address_word_type=""
    address_word=""
    different_list=[]
    different_list_filter=[]
    tag_list=[]
    with open('E:/test/test_1.csv', 'w', newline="") as csvwriter:
        csv_writer = csv.writer(csvwriter)
        for i in range(0,len(address_word_list_test)):
            # if re.search()
            key="08d750b299c704dc6c9114d7261673a6"
            url="http://restapi.amap.com/v3/geocode/geo?address="+address_word_list_test[i][0]+"&key=08d750b299c704dc6c9114d7261673a6&city=110000"
            content=rq.get(url)
            content_json=json.loads(content.text)

            # make sure keyword:"geocodes" exists in api return values and then look for keywords
            if "geocodes" in content_json and len(content_json["geocodes"])>0:
                # these two objects are used in filter function
                address_word_type = content_json["geocodes"][0]["level"]
                address_word=address_word_list_test[i][0]

                # first look for each word's return value and then see each word's type in raw file, if these two conditions
                if content_json["geocodes"][0]["level"]=="兴趣点":
                    if str(address_word_list_test[i][1]) == "13":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("POI")

                    # print(content_json["geocodes"][0]["level"])
                elif content_json["geocodes"][0]["level"] == "村庄":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached village")

                elif (content_json["geocodes"][0]["level"]=="村庄")and("门外"in address_word_list_test[i][0])and(str(address_word_list_test[i][1])!="13"):
                    # print(content_json["geocodes"][0]["level"])
                    address_word_list_test[i].append("1")
                    different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))

                elif content_json["geocodes"][0]["level"] == "道路":
                    if str(address_word_list_test[i][1]) == "9":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached road")

                elif content_json["geocodes"][0]["level"] == "乡镇":
                    if str(address_word_list_test[i][1]) == "5":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached town")

                elif content_json["geocodes"][0]["level"] == "开发区":
                    if str(address_word_list_test[i][1]) == "4":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached district")

                elif content_json["geocodes"][0]["level"] == "热点商圈":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


                elif content_json["geocodes"][0]["level"] == "地铁站":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


                elif content_json["geocodes"][0]["level"] == "公交站台":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


                elif content_json["geocodes"][0]["level"] == "道路交叉口":
                    if str(address_word_list_test[i][1]) == "9":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


            csv_writer.writerow(address_word_list_test[i])
        print(different_list)
        # filter gaode geocoding results based on keyword:"level" and only return words which their levels are different from original file
        for k in range(0,len(different_list)):
            if (different_list[k][0]==different_list[k-1][0] and different_list[k][1]!=different_list[k-1][1]):
                different_list_filter.append(different_list[k])
                different_list_filter.append(different_list[k-1])

    # output fliter result
    with open('E:/test/test_different_1.csv', 'w', newline="") as csvwriter:
        csv_writer_2 = csv.writer(csvwriter)
        for j in range(0, len(different_list_filter)):
            csv_writer_2.writerow(different_list_filter[j])

        return address_word_list_test

# 需要修改逻辑，完善代码
# filter function
def compare_gaode(word,str1,number):
    compare_list={"村庄":6,"兴趣点":13,"道路":9,"乡镇":5,"开发区":4,"热点商圈":6,"地铁站":6,"公交站台":6,"道路交叉路口":9}
    try:
        if compare_list[str1]!=int(number):
            return(word,number)
        else:
            return(word)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()