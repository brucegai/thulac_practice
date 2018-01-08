import re,sys,csv
import logging,six

def process_data():
    index=0
    odd_word=""
    double_word=""
    with open('E:/grepdiff.csv','r') as csvreader:
        csv_reader=csv.reader(csvreader)
        for line in csv_reader:
            if index%2==0:
                double_word=load_word(line)
                # print(double_word)
            elif index%2!=0:
                print(line)
                odd_word=load_word(line)
                print(odd_word)
            index += 1
    return odd_word,double_word

#only a word with two character
def find_singleconnect_word():
    connect_word=""
    connect_word_2=""
    check_boolean=False
    with open('E:/grepdiff.csv','r') as csvreader:
        csv_reader=csv.reader(csvreader)
        for row in csv_reader:
            if row[2].find('|')>0:
                front_word=row[2].split('|')[0]
                front_word_2=front_word.split('^')[0]
                front_index=len(front_word_2)
                back_word=row[2].split('|')[1]
                back_index=len(back_word)
                connect_word=list(front_word_2)[front_index-1]+list(back_word)[0]
                print(connect_word)
                check_boolean=True
                with open('D:/singleconnect_word.csv', 'r') as csvreader2:
                    csv_reader_2=csv.reader(csvreader2)
                    for item in csv_reader_2:
                        print(item)
            else:
                print("no")
        # if check_boolean==True

#
def find_multipleconnect_word():
    connect_word = ""
    connect_word_2 = []
    check_boolean = False
    word_length=[5,4,3,2,1]
    attach_word_list=[]
    connect_word_length=5
    with open('E:/grepdiff.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        for row in csv_reader:
            if row[2].find('|') > 0:
                front_word = row[2].split('|')[0]
                front_word_2 = front_word.split('^')[0]
                front_word_length=len(front_word_2)
                back_word = row[2].split('|')[1]
                back_word_length=len(back_word)
                for number in word_length:
                    attach_word_list.append((front_word_2)[front_word_length - 1 - number:-1] + (back_word)[0:5 - number])
    return attach_word_list

def adjust_word():
    word_list=find_multipleconnect_word()
    # print(word_list)
    with open('D:/connect_word.csv', 'r') as csvreader2:
        csv_reader_2=csv.reader(csvreader2)
        for item in csv_reader_2:
            # print(type(item))
            for i in range(1,len(word_list)):



                # print(type(number),type(item))
                # print((front_word_2)[front_word_length - 1 - number:-1] + (back_word)[0:5 - number])
                # print(re.match(str(item),((front_word_2)[front_word_length-1-number:-1]+(back_word)[0:5-number])))
                # if re.findall(str(item),((front_word_2)[front_word_length-1-number:-1]+(back_word)[0:5-number]))!=[]:
                #      print(((front_word_2)[front_word_length-1-number:-1]+(back_word)[0:5-number]),str(item))
                # else:
                #     break

def find_should_cut_word():
    complete_word=""
    word_fragment=""



find_multipleconnect_word()
# find_singleconnect_word()

def load_word(x):
    i=1
    fine_word=""
    for item in x:
        i += 1
        if i == 4:
            item_split_2 = item
            if re.search(r'(\S)', item_split_2) != None:
                raw_word = item.split('|')[0]
                fine_word = raw_word.split('^')[0]
                # print(fine_word)
        elif i==3:
            item_split=item
    return fine_word


def replicate_words(input_words):
    feedback=""
    if re.findall('([0-9])',input_words)!=None:
        feedback="single_string"
    else:
        feedback=""
    return (feedback)



def main():
    find_multipleconnect_word()
    adjust_word()
    #  process_data()

if __name__ == '__main__':
    main()
