# -*- coding: utf-8 -*-
import csv,re
import requests as rq
from bs4 import BeautifulSoup
import json
import _thread

#main function
def main():
    # import_address_2()
    request_api()
    # filter()


#read address_data and return all address parts as a single list for sample_api format
def import_address():
    tag="|"
    number_tag=0
    address_word_list=[]
    address_word_1=""
    address_word_2=""
    with open('E:/sample_api_2.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        for row in csv_reader:
            if tag in row[2]:
                number_tag=row[2].count(tag)
                if number_tag==1:
                    address_word_1=row[2].split(tag)[0].split('^')[0]
                    address_word_2=row[2].split(tag)[1].split('^')[0]
                    address_word_list.append(address_word_1)
                    address_word_list.append(address_word_2)
                else:
                    address_word_list+=split_times(row[2],number_tag)
            else:
                address_word_1=row[2].split('^')[0]
                address_word_list.append(address_word_1)
    return address_word_list

def import_address_2():
    word_list=[]
    with open('E:/sample_api_2.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        for line in csv_reader:
            # print(line[2])
            # print(line[2].split('^')[0])
            # print(line[2].split('^')[:2])
            word_list.append(line[2].split('^')[:2])
    return word_list

# deal with address that contains multiple "|",apply for sample_api
def split_times(split_sentence,number):
    tag = "|"
    return_list=[]
    address_list=split_sentence.split(tag,number)
    i=0
    for i in range(0,number):
        eachword=address_list[i].split('^')[0]
        return_list.append(eachword)
        i+=1
    return return_list

#remove all unnecessary syntax
def filter():
    source_file=import_address_2()
    i=1
    for i in range(1,len(source_file)):
        source_file[i].append(i)
        if len(source_file[i][0])==1:
            source_file[i].append("0")
        elif (source_file[i][0]=="0号")|(source_file[i][0]=="0排")|(source_file[i][0]=="0楼")|(source_file[i][0]=="0#"):
            source_file[i].append("0")
    return source_file


#request api and return all tag
def request_api():
    address_word_list = filter()
    address_word_list_test = address_word_list
    address_word_type_list = []
    address_word_type = ""
    address_word = ""
    different_list = []
    different_list_filter = []
    tag_list = []
    with open('E:/sample_api_output_14.csv', 'w', newline="") as csvwriter:
        csv_writer = csv.writer(csvwriter)
        for i in range(0, len(address_word_list_test)):
            # if re.search()
            key = "08d750b299c704dc6c9114d7261673a6"
            url = "http://restapi.amap.com/v3/geocode/geo?address=" + address_word_list_test[i][
                0] + "&key=08d750b299c704dc6c9114d7261673a6&city=110000"
            content = rq.get(url)
            content_json = json.loads(content.text)

            # make sure keyword:"geocodes" exists in api return values and then look for keywords
            if "geocodes" in content_json and len(content_json["geocodes"]) > 0:
                # these two objects are used in filter function
                address_word_type = content_json["geocodes"][0]["level"]
                address_word = address_word_list_test[i][0]

                # first look for each word's return value and then see each word's type in raw file, if these two conditions
                if content_json["geocodes"][0]["level"] == "兴趣点":
                    if str(address_word_list_test[i][1]) == "13":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("POI")

                        # print(content_json["geocodes"][0]["level"])
                elif content_json["geocodes"][0]["level"] == "村庄":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached village")

                elif (content_json["geocodes"][0]["level"] == "村庄") and ("门外" in address_word_list_test[i][0]) and (
                    str(address_word_list_test[i][1]) != "13"):
                    # print(content_json["geocodes"][0]["level"])
                    address_word_list_test[i].append("1")
                    different_list.append(compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))

                elif content_json["geocodes"][0]["level"] == "道路":
                    if str(address_word_list_test[i][1]) == "9":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached road")

                elif content_json["geocodes"][0]["level"] == "乡镇":
                    if str(address_word_list_test[i][1]) == "5":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached town")

                elif content_json["geocodes"][0]["level"] == "开发区":
                    if str(address_word_list_test[i][1]) == "4":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))
                        print("reached district")

                elif content_json["geocodes"][0]["level"] == "热点商圈":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


                elif content_json["geocodes"][0]["level"] == "地铁站":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


                elif content_json["geocodes"][0]["level"] == "公交站台":
                    if str(address_word_list_test[i][1]) == "6":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))


                elif content_json["geocodes"][0]["level"] == "道路交叉口":
                    if str(address_word_list_test[i][1]) == "9":
                        address_word_list_test[i].append("1")
                    else:
                        different_list.append(
                            compare_gaode(address_word, address_word_type, address_word_list_test[i][1]))

            csv_writer.writerow(address_word_list_test[i])
        # print(address_word_list_test)

        print(different_list)

        # filter gaode geocoding results based on keyword:"level" and only return words which their levels are different from original file
        for k in range(0, len(different_list)):
            if (different_list[k][0] == different_list[k - 1][0] and different_list[k][1] != different_list[k - 1][
                1]) | (
                    different_list[k][0] == different_list[k - 1][0] and different_list[k][1] != different_list[k - 1][
                1]):
                different_list_filter.append(different_list[k])

    # output fliter result
    with open('E:/sample_api_different_list_output.csv', 'w', newline="") as csvwriter:
        csv_writer_2 = csv.writer(csvwriter)
        for j in range(0, len(different_list_filter)):
            csv_writer_2.writerow(different_list_filter[j])

        return address_word_list_test



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


