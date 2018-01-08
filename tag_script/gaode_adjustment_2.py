# -*- coding: utf-8 -*-
import csv,re
import requests as rq
from bs4 import BeautifulSoup
import json
import time

def main():
    adjustment()

def adjustment():
    key = "08d750b299c704dc6c9114d7261673a6"
    address_word=""
    new_list=[]
    word_list_all=[]
    with open('E:/test/sample_api_different_list_128.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        for line in csv_reader:
            word_list=line[:2]
            url= url="http://restapi.amap.com/v3/place/text?&keywords="+word_list[0]+"&city=北京&output=json&offset=20&page=1&key=08d750b299c704dc6c9114d7261673a6&extensions=all"
            content = rq.get(url)
            content_json = json.loads(content.text)
            if "pois" in content_json and len(content_json["pois"]) > 0:
                # makes sure the name in
                if content_json["pois"][0]["name"]==word_list[0]:
                    print(content_json["pois"][0]["name"],word_list[0])
                    correct_type_word=content_json["pois"][0]["type"]
                    correct_type=return_dict()[correct_type_word]
                    word_list.append(correct_type)
                else:
                    word_list.append("unmatched word")
            else:
                word_list.append(18)
            word_list_all.append(word_list)

    with open('E:/test/different_list_adjustment_128_3.csv', 'w', newline="") as csvwriter:
        csv_writer_2 = csv.writer(csvwriter)
        for j in range(0, len(word_list_all)):
            csv_writer_2.writerow(word_list_all[j])
    print(word_list_all)
    return word_list_all

def return_dict():
    compare_list_dict = {}
    with open('E:/compare_list/compare_list.csv', 'r') as csvreader:
        csv_reader_gaode = csv.reader(csvreader)
        for line in csv_reader_gaode:
            compare_list_dict.setdefault(line[0], line[1])
    return compare_list_dict




if __name__ == '__main__':
    main()

