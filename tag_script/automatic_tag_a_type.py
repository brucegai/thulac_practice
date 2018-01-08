import csv,re

def main():
    # request_for_api(import_address())
    import_address()

def import_address():
    address_group=[]
    address_list=[]
    with open('D:/try_debug_for_automatic_tag.csv', 'r') as csvreader:
        csv_reader = csv.reader(csvreader)
        next(csv_reader)
        for row in csv_reader:
            address_group.append(row)
        for i in range(0,len(address_group),2):
            if i%2==0:
                address_every_two_group=[]
                address_every_two_group.append(address_group[i])
                address_every_two_group.append(address_group[i+1])
                address_list.append(address_every_two_group)
                print(len(address_every_two_group))
                for m in range(0,1):
                    # request_for_api(address_every_two_group[m])
                    print(address_every_two_group[m])
    return address_list

def request_for_api(list_a):
    tag="|"
    for i in range(0,len(list_a)):
        number=0
        for item in list_a[i]:
            number=item[2].count(tag)
            # print(item[2])
            if tag in item[2]:
                word_1=item[2].split('|')[0].split('^')[0]
                if number >=1:
                    temp_word_list=[]
                    for k in range(0,number+1):
                        word_temp=item[2].split('|')[k].split('^')[0]
                        temp_word_list.append(word_temp)
                    print(temp_word_list)
                else:
                    print("unsolved")

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

if __name__ == '__main__':
    main()
