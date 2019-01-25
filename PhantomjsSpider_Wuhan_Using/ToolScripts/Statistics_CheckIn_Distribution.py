# encoding=utf-8
# Date: 2019-1-20
# Author: MJUZY
# Reference
#   solve UnicodeEncodeError
#   https://blog.csdn.net/abcdasdff/article/details/81706178


import csv
import json
import os


def walk_path(walked_path):
    for dirpath, dirnames, filenames in os.walk(walked_path):

        statistics_path = "./CheckIn_Distribution_Statistics.csv"
        csvFile = open(statistics_path, 'a+', newline='', encoding="utf-8")
        writer = csv.writer(csvFile)

        display_names = []
        statistics_dic = {"No_POI": [0, []]}

        for uid_file in filenames:
            json_path = walked_path + '/' + uid_file

            uid = uid_file.split('.')[0]

            line_i = 0

            display_names_one_uid = []

            with open(json_path, encoding="utf-8") as f:
                for line in f.readlines():
                    print("uid: " + uid + " " + "line_i : ", line_i)

                    rline = json.loads(line)
                    geo = rline["geo"]
                    coor = geo["coordinates"]

                    lng = coor[1]
                    lat = coor[0]

                    try:
                        url_objects = rline["url_objects"][0]
                        object_1 = url_objects["object"]
                        object_2 = object_1["object"]
                        display_name = object_2["display_name"]

                        if display_name not in display_names:
                            display_names.append(display_name)
                            statistics_dic[display_name] = [1, [(lng, lat)]]

                            display_names_one_uid.append(display_name)
                        else:
                            if display_name not in display_names_one_uid:
                                display_names_one_uid.append(display_name)

                                temp = statistics_dic[display_name][1]
                                temp.append((lng, lat))

                                statistics_dic[display_name] = [statistics_dic[display_name][0] + 1, temp]
                            else:
                                print("Warning: repeated ! ")
                    except(KeyError, IndexError):
                        if "No_POI" not in display_names_one_uid:
                            display_names_one_uid.append("No_POI")

                            temp = statistics_dic["No_POI"][1]
                            temp.append((lng, lat))

                            statistics_dic["No_POI"] = [statistics_dic["No_POI"][0] + 1, temp]

                    line_i += 1

        line_i = 0
        for key, value in statistics_dic.items():
            data = [key, value[0], value[1]]

            writer.writerow(data)

            line_i += 1
            if line_i % 50 == 0:
                csvFile.close()

                csvFile = open(statistics_path, 'a+', newline='', encoding="utf-8")
                writer = csv.writer(csvFile)

        csvFile.close()

        break


if __name__ == "__main__":

    province = "湖北省"
    city = "武汉市"

    dir_disk = "F"
    dir_file1 = "Fast_Prepared_Json"
    dir_file2 = "2014"
    dir_file3 = "08"

    walked_path = dir_disk + ":/" + dir_file1 + '/' + province + '/' + city + '/' + dir_file2 + '/' + dir_file3

    walk_path(walked_path)
