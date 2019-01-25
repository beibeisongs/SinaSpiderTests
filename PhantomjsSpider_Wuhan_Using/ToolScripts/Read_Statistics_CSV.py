# encoding=utf-8
# Date: 2019-1-20
# Author:
# Reference:
#   solve _csv.Error: field larger than field limit (131072)
#   https://blog.csdn.net/dm_learner/article/details/79028357


import csv
from matplotlib import pyplot as plt


def LngLat2TimeFormat(lng_float, lat_float):
    lng_h = int(lng_float)
    lng_float_part = lng_float - lng_h
    lng_m = int(lng_float_part * 60)
    lng_s = int((lng_float_part * 60 - lng_m) * 60)

    lat_h = int(lat_float)
    lat_float_part = lat_float - lat_h
    lat_m = int(lat_float_part * 60)
    lat_s = int((lat_float_part * 60 - lat_m) * 60)

    lng_time = (lng_h, lng_m, lng_s)
    lat_time = (lat_h, lat_m, lat_s)

    return lng_time, lat_time


def LngLat2FloatFormat(lng_time, lat_time):
    """

    :param lng_time: <sample> (113, 41, )
    :param lat_time: <sample> (29, 58, )
    :return:
    """
    lng_float = lng_time[0] + lng_time[1] / 60
    lat_float = lat_time[0] + lat_time[1] / 60

    return lng_float, lat_float


if __name__ == "__main__":

    lng_time_1, lat_time_1 = LngLat2FloatFormat((113, 41), (29, 58))
    lng_time_2, lat_time_2 = LngLat2FloatFormat((115, 5), (31, 22))

    csv.field_size_limit(500 * 1024 * 1024)

    csv_name = "./CheckIn_Distribution_Statistics.csv"
    with open(csv_name, 'r', encoding="utf-8") as csvFile:
        reader = csv.reader(csvFile)

        line_i = 0

        LNG = []
        LAT = []
        for item in reader:
            coors = item[2]

            temp_1 = coors.split("[(")[1].split("]")[0].split("), (")
            temp_1[-1] = temp_1[-1].split(")")[0]

            for coor in temp_1:
                coor = coor.split(", ")

                LNG.append(float(coor[0]))
                LAT.append(float(coor[1]))

            line_i += 1
            print("line_i", line_i)

        csvFile.close()

        lng_wuhan = []
        lat_wuhan = []

        for i in range(len(LNG)):

            # Please refer to
            # ./Readme.txt to see the lng lat region
            if LNG[i] > lng_time_1:
                if LNG[i] < lng_time_2:
                    if LAT[i] > lat_time_1:
                        if LAT[i] < lat_time_2:
                            lng_wuhan.append(LNG[i])
                            lat_wuhan.append(LAT[i])

        for i in range(len(LNG)):
            print("i", i)

            if i <= 7000:
                plt.plot(lng_wuhan[i], lat_wuhan[i], color='b', markersize=3, marker='o', alpha=0.5)

        plt.show()
