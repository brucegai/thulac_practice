import csv,re,sys,os,math
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib,requests
list_x=[]
list_y=[]
# every other seven elements

with open('HR.csv','r') as csvreader:
    csv_reader=csv.reader(csvreader)
    for bb in csv_reader:
        rotate = -1
        for laopo in bb:
            rotate+=1
            if rotate%10==0:
                # print(laopo)
                print(repr(laopo))
                list_x.append(laopo)
        satisfaction=str(bb).split(',')[0].strip("['")
        evaluation=str(bb).split(',')[1].strip("'").split("'")[1]
        # turn each element in satisfaction from str into int
print(list_x)