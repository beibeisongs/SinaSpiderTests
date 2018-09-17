# encoding=utf-8
# Date: 2018-09-11
# Author: MJUZY


import json
import os
import re
import time
import datetime
import urllib.request


# 定义页面打开函数
def use_proxy(url, proxy_addr):  # <Sample> proxy_addr = '122.241.72.191:808'

    req = urllib.request.Request(url)  # <Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'

    # req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1")

    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)

    request_mark = True
    while request_mark:
        try:
            data = urllib.request.urlopen(req, timeout=5)
            data_read = data.read().decode('utf-8', 'ignore')

            request_mark = False  # 退出循环
        except:
            print("---Proxy Time Out !---")
            request_mark = True

    return data_read


# 获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data = use_proxy(url, proxy_addr)
    data_json = json.loads(data)

    containerid = ''

    content = data_json.get('data')

    try:
        for data in content.get('tabsInfo').get('tabs'):
            if (data.get('tab_type') == 'weibo'):
                containerid = data.get('containerid')
                print("containerid : ", containerid)
    except:
        return containerid

    return containerid


def myRequest(req, timeout_mark):
    data = urllib.request.urlopen(req, timeout=5)
    print("---sleep---0.5---second---")
    time.sleep(0.5)

    read_data = data.read().decode('utf-8', 'ignore')

    timeout_mark = False
    return read_data, timeout_mark


def catchWeibo_HTML(scheme):
    req = urllib.request.Request(scheme)  # <Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")

    timeout_mark = True
    while timeout_mark:
        try:
            read_data, timeout_mark = myRequest(req, timeout_mark)
        except:
            print("---Time Out ! And Sleep 2 Seconds !---")
            time.sleep(2)
            timeout_mark = True

    return read_data


def getYear(weibo_created_time):
    year = weibo_created_time.split(' ')
    year = year[5]

    return year


def catchFromScripts_Steps(m_script):
    weibo_content1 = ''  # Initialize the variable weibo_page_title
    weibo_created_time = ''  # Initialize the variable weibo_created_time
    weibo_uid = ''
    weibo_pic_url = []
    weibo_gender = ''

    for script in m_script:
        res_content1 = r'"content1": "(.*?)"'

        weibo_content1 = re.findall(res_content1, script)
    print("weibo_content1 : ", weibo_content1)
    if len(weibo_content1) != 0:
        weibo_content1 = weibo_content1[0]
    else:
        weibo_content1 = ''

    for script in m_script:
        # 注意：created_at 是一个类似json 的key
        res_created_time = r'"created_at": "(.*?)"'

        weibo_created_time = re.findall(res_created_time, script)
    print("weibo_created_time : ", weibo_created_time)
    if len(weibo_created_time) == 0:
        return weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_content1
    weibo_created_time = weibo_created_time[0]

    for script in m_script:
        res_uid = r'"id": (.*?),'

        weibo_uid = re.findall(res_uid, script)
    print("weibo-uid : ", weibo_uid)
    weibo_uid = weibo_uid[1]

    for script in m_script:
        res_url = r'"url": "(.*?)"'

        weibo_pic_url = re.findall(res_url, script)
    print("weibo_pic_url : ", weibo_pic_url)

    for script in m_script:
        res_gender = r'"gender": "(.*?)"'

        weibo_gender = re.findall(res_gender, script)
    print("weibo_gender : ", weibo_gender)
    weibo_gender = weibo_gender[0]

    return weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_content1


def catchFromScipt(html_script, HTML_data):
    weibo_uid = ''
    weibo_created_time = ''
    weibo_pic_url = []
    weibo_gender = ''
    weibo_page_title = []
    weibo_content1 = ''

    m_script = re.findall(html_script, HTML_data, re.S | re.M)

    weibo_page_title = []  # Initialize the variable weibo_page_title
    for script in m_script:
        res_page_title = r'"page_title": "(.*?)"'

        weibo_page_title = re.findall(res_page_title, script)

    """
        <Attention>: maybe you can use the sign : "·" to create a new filter
    """

    if (weibo_page_title != []):
        if weibo_page_title[0] != '':
            if not ("#" in weibo_page_title[0]):
                if not ("视频" in weibo_page_title[0]):
                    if ("·" in weibo_page_title[0]):
                        weibo_page_title = weibo_page_title[0]

                        weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_content1 = catchFromScripts_Steps(
                            m_script)
                else:
                    weibo_page_title = ''

                    weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_content1 = catchFromScripts_Steps(
                        m_script)
        else:
            weibo_page_title = ''

            weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_content1 = catchFromScripts_Steps(
                m_script)
    else:
        weibo_page_title = ''

        weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_content1 = catchFromScripts_Steps(m_script)

    return weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1


def extractINFO(HTML_data):
    html_script = r'<script>(.*?)</script>'

    weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1 = catchFromScipt(
        html_script, HTML_data)

    return weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1


def tryGetData(i, weibo_url, proxy_addr, recordedINFO, process_mark):
    print("---Process : tryGetData---")

    data = use_proxy(weibo_url, proxy_addr)

    content = json.loads(data).get('data')

    cards = content.get('cards')

    card_tot_id = 0

    if (len(cards) > 0):
        for j in range(len(cards)):

            print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")

            card_type = cards[j].get('card_type')

            if (card_type == 9):

                mblog = cards[j].get('mblog')
                text = mblog.get('text')

                if len(text) > 0:
                    if ("·" in text):

                        print()
                        print()
                        print()

                        """Initialize data dict"""
                        data_dict = {}

                        idstr = mblog.get('idstr')  # 微博的idstr，储存起来，为后续爬虫再用
                        # <Sample>: idstr = 4281561774373070
                        # (Sample): tested_url of weibo: https://m.weibo.cn/status/4281561774373070

                        scheme = cards[j].get(
                            'scheme')  # <Sample>: scheme = 'https://m.weibo.cn/status/GydNfilDo?mblogid=GydNfilDo&luicode=10000011&lfid=1076031995216231'

                        HTML_data = catchWeibo_HTML(scheme)

                        weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1 = extractINFO(HTML_data)

                        if weibo_uid != '':

                            data_dict["uid"] = weibo_uid
                            data_dict["idstr"] = idstr
                            data_dict["gender"] = weibo_gender
                            data_dict["title"] = weibo_page_title
                            print("---" + weibo_page_title + "---")
                            data_dict["content1"] = weibo_content1

                            data_dict["created_at"] = weibo_created_time
                            print("created_at : ", weibo_created_time)

                            data_dict["text"] = text
                            data_dict["pic_urls"] = weibo_pic_url

                            year = getYear(weibo_created_time)
                            if int(year) <= 2016: process_mark = False  # <Attention>: 发出年份小于2016的将不再爬取

                            recordedINFO.append(data_dict)

                card_tot_id += 1
    else:
        process_mark = False

    return recordedINFO, process_mark


def open_Json_File_To_Write(path_to_write):
    judgeExisting = os.path.exists(path_to_write)
    if not judgeExisting:
        f1 = open(path_to_write, mode='w')
    else:
        f1 = open(path_to_write, mode='a')

    return f1


def writeData(file, recordedINFO):
    fh = open_Json_File_To_Write(file)
    for data in recordedINFO:
        a = json.dumps(data)
        b = str(a) + "\n"

        fh.write(b)

    fh.close()


def getWeibo(id, file):
    print("---Process : get_weibo---")

    """
    注意：现在进入到了提取有POI的微博的数据的环节
    """

    i = 1

    process_mark = True

    POIWeibo_Count = 0

    while process_mark:

        """<Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'"""
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id

        containerid = get_containerid(url)
        if containerid != '':

            """<Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474&containerid=1076031259110474&page=1'"""
            weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + \
                        '&containerid=' + containerid + '&page=' + str(i)

            recordedINFO = []  # 该博主的每条微博信息为一个元素
            """try:"""
            recordedINFO, process_mark = tryGetData(i, weibo_url, proxy_addr, recordedINFO, process_mark)
            """
            except Exception as e:

                print(e)

                print("---Now sleep for 3 second to Stop this process---")
                time.sleep(3)
            """

            if recordedINFO != []:
                writeData(file, recordedINFO)

                POIWeibo_Count += len(recordedINFO)
                print("POIWeibo_Count : ", POIWeibo_Count)

                print("content of one page:　")
                for record_sample in recordedINFO:
                    print(record_sample)
        else:
            process_mark = False

        i += 1

        if i == 21:
            if POIWeibo_Count == 0:
                process_mark = False  # 从而退出循环

        if i == 50:
            if POIWeibo_Count < 3:
                process_mark = False

        if i == 70:
            if POIWeibo_Count < 4:
                process_mark = False


def writeTimeLog(_dir, uid, timeLogFileName):
    json_path = _dir + uid + "/" + timeLogFileName

    log_data = {}

    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在的时间
    construct1 = nowTime.split('-')

    year = construct1[0]
    month = construct1[1]
    day = ((construct1[2]).split(' '))[0]

    log_data["year"] = year
    log_data["month"] = month
    log_data["day"] = day

    fh = open(json_path, mode='w')  # 必须重写

    a = json.dumps(log_data)
    b = str(a) + "\n"

    fh.write(b)
    fh.close()

    return


def mkDocument(_dir, uid):
    docPath = _dir + uid
    if not os.path.exists(docPath):
        os.makedirs(docPath)

        return docPath
    else:
        return ''


def goThroughPath(dir_path, _dir):
    file_i = 0
    for dirpath, dirnames, filenames in os.walk(dir_path):
        construct1 = str(dirpath).split("\\")
        if len(construct1) >= 3:
            uid = construct1[2]

            print(uid, file_i)
            file_i += 1

            docPath = ''
            docPath = mkDocument(_dir, uid)
            if docPath != '':
                writeTimeLog(_dir, uid, timeLogFileName)

                file = docPath + "/" + uid + ".json"

                getWeibo(uid, file)


if __name__ == "__main__":
    _dir = "./"
    _dir = mkDocument(_dir, "Accounts_Wuhan")
    _dir += "/"
    """
        <Attention>: 不要轻易改变该默认项
                    要改的话，必须
                                上下两个 "Accounts"
                                同时改动为相同的！
    """
    _dir = "./Accounts_Wuhan/"

    timeLogFileName = "TimeLog.json"

    # 设置代理IP
    proxy_addr = "122.241.72.191:808"

    dir_path = "L:\\ForCompensated_Wuhan"
    goThroughPath(dir_path, _dir)
