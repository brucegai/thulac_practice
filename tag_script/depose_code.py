# unused code from automatic tag script

if content_json["pois"][0]["type"] == "地名地址信息;普通地名;普通地名":
    if str(address_word_list_test[i][1]) == "13":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))
        print("POI")

        # print(content_json["geocodes"][0]["level"])
elif content_json["pois"][0]["type"] == "地名地址信息;普通地名;村庄级地名":
    if str(address_word_list_test[i][1]) == "6":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))
        print("reached village")

elif content_json["pois"][0]["type"] == "地名地址信息;交通地名;道路名":
    if str(address_word_list_test[i][1]) == "9":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "地名地址信息;交通地名;环岛名":
    if str(address_word_list_test[i][1]) == "9":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "地名地址信息;交通地名;隧道":
    if str(address_word_list_test[i][1]) == "9":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "地名地址信息;普通地名;乡镇级地名":
    if str(address_word_list_test[i][1]) == "5":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "地名地址信息;普通地名;街道级地名":
    if str(address_word_list_test[i][1]) == "5":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "商务住宅;产业园区;产业园区":
    if str(address_word_list_test[i][1]) == "4":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "地名地址信息;交通地名;桥":
    if str(address_word_list_test[i][1]) == "6":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))


elif content_json["pois"][0]["type"] == "地名地址信息;自然地名;河流":
    if str(address_word_list_test[i][1]) == "6":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))

elif content_json["pois"][0]["type"] == "地名地址信息;交通地名;立交桥":
    if str(address_word_list_test[i][1]) == "6":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))


elif content_json["pois"][0]["type"] == "地名地址信息;交通地名;路口名":
    if str(address_word_list_test[i][1]) == "13":
        address_word_list_test[i].append("1")
    else:
        different_list.append(compare_gaode_accurate(address_word, address_word_type, address_word_list_test[i][1]))