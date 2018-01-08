#-*- coding:utf-8 -*-
import os,sys,csv
from math import sqrt
from itertools import permutations




def test1():
    for i in range(1,5):
        for j in range(1,5):
            for k in range(1,5):
                if (i!=j)&(i!=k)&(j!=k):
                    print (i,j,k)


def test2():
    for i in range(1,168):
        for j in range(1,168):
            k=i-j
            m=i+j
            if k*m==168:
                print(i,j)

def test1_new():
    t = 0
    for i in permutations('1234', 3):
        print(''.join(i))
        t += 1


def test4(x,y,z):
    year=x
    month=y
    day=z
    if (year%4==0):
        number=x




def test10():
    for i in range(1,10):
        print("\n")
        for j in range(1,i+1):
            print("%d*%d=%d"%(i,j,i*j))

def test11():
    for i in range(1,10):
        for j in range(0,9):
            for k in range(0,9):
                number1=i*100+j*10+k
                number2=pow(i,3)+pow(j,3)+pow(k,3)
                if number1==number2:
                    print(number1)


def test12():
    str_string=input('please enter a word:'+'\n')
    list_a=[]
    str_string=str(str_string)
    for letter in str_string:
        list_a.append(letter)

    for i in reversed(list_a):
        print(i)




def test13():
    int_a=input('please enter a number:'+'\n')
    str_int=list(int_a)
    i=1
    back_number=str_int[len(str_int)-1]
    front_number=str_int[len(str_int)-2]
    for i in range(1,len(str_int)):
        back_number = str_int[len(str_int) - i]
        front_number = str_int[i]
        if back_number==front_number:
            print("same")
        else:
            print("mistake")
            break

week_list=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
user_input=input('please enter a day in a week:'+'\n')
print(type(user_input))
def week_test(x):
    input_string=''
    input_string=user_input


























