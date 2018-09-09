# encoding=utf-8
# Date: 2018-09-09
# Author: MJUZY


def Transfer2TimeType(lon_temp, lat_temp):

    # Part1 Used
    lon_temp_ZP = int(lon_temp) # Get The Main Number Part
    lat_temp_ZP = int(lat_temp) # Get The Main Number Part

    lon_temp_minP = (lon_temp - lon_temp_ZP) * 60
    lat_temp_minP = (lat_temp - lat_temp_ZP) * 60

    # Big letter 'P' refers to the Word "Part"
    # Part2 Used
    lon_P2_ZP = int(lon_temp_minP)
    lat_P2_ZP = int(lat_temp_minP)

    lon_P2_minP = lon_temp_minP - lon_P2_ZP
    lat_P2_minP = lat_temp_minP - lat_P2_ZP

    # Part3 Used
    lon_P3 = lon_P2_minP * 60
    lat_P3 = lat_P2_minP * 60

    return lon_temp_ZP, lon_P2_ZP, lon_P3, lat_temp_ZP, lat_P2_ZP, lat_P3


def Transfer2FloatType(lng_h, lng_m, lng_s, lat_h, lat_m, lat_s):
    lng_Float = lng_h + lng_m / 60 + lng_s / 3600
    lat_Float = lat_h + lat_m / 60 + lat_s / 3600
    return lng_Float, lat_Float


if __name__ == "__main__":

    """
    <Samples>: as the following
    """
    lon_temp_ZP, lon_P2_ZP, lon_P3, lat_temp_ZP, lat_P2_ZP, lat_P3 = Transfer2TimeType(111.666, 30.666)
    print(lon_temp_ZP, lon_P2_ZP, lon_P3, lat_temp_ZP, lat_P2_ZP, lat_P3)

    lng_Float, lat_Float = Transfer2FloatType(29, 58, 0, 31, 22, 0)
    print(lng_Float, lat_Float)
