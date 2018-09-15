# encoding=utf-8
# Date: 2018-09-11
# Author: MJUZY


import json
import cmath
import eventlet
import numpy as np
import os
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import time
from TransferTypes import Transfer2TimeType, Transfer2FloatType
import datetime
import urllib.request


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


def myRequest(req, timeout_mark):
    data = urllib.request.urlopen(req, timeout=5)
    print("---sleep---0.5---second---")
    time.sleep(0.5)

    read_data = data.read().decode('utf-8', 'ignore')

    timeout_mark = False
    return read_data, timeout_mark


def catchWeibo_HTML(scheme):
    req = urllib.request.Request(
        scheme)  # <Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'
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


def tryGetData(i, weibo_url, proxy_addr, recordedINFO, process_mark, lng, lat):
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
                        print("lng : ", lng, "lat : ", lat)

                        weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1 = extractINFO(
                            HTML_data)

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


# 定义页面打开函数
def use_proxy(url, proxy_addr):  # <Sample> proxy_addr = '122.241.72.191:808'

    req = urllib.request.Request(
        url)  # <Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'

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


def writeData(file, recordedINFO):
    fh = open_Json_File_To_Write(file)
    for data in recordedINFO:
        a = json.dumps(data)
        b = str(a) + "\n"

        fh.write(b)

    fh.close()


def getWeibo(id, file, lng, lat):
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
            recordedINFO, process_mark = tryGetData(i, weibo_url, proxy_addr, recordedINFO, process_mark, lng, lat)
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


def GoThrough_Current_Page(obj, vip_panel_list, panel_id_record, length_panel_list, recordedINFO):
    print("---Go Through Current Page !---")

    while panel_id_record < length_panel_list:

        vip_panel_sample = vip_panel_list[panel_id_record]

        vip_panel_text = vip_panel_sample.text
        if "·" in vip_panel_text:
            recordedINFO.append(vip_panel_text)
            print("---panel_id_record---", panel_id_record)

        panel_id_record += 1

    return vip_panel_list, panel_id_record, recordedINFO, obj


def get_Weibo_host(obj, host_url, file):
    panel_id_record = 0

    length_panel_change = True

    """
    注意：现在开始进入到微博主页
    """
    obj.get(host_url)

    print("---sleep 1.5 after get host page !---")
    time.sleep(1.5)

    vip_panel_list = obj.find_elements_by_class_name("weibo-text")
    length_panel_list = len(vip_panel_list)
    print("---length_panel_list---", length_panel_list)
    if length_panel_list > 0:

        recorded_POIPanel_Texts = []  # 初始化panel Text记录器

        while length_panel_change:
            """
            recordedINFO改成记录有POI的微博的标号
            """
            vip_panel_list, panel_id_record, recorded_POIPanel_Texts, obj = GoThrough_Current_Page(obj, vip_panel_list,
                                                                                                   panel_id_record,
                                                                                                   length_panel_list,
                                                                                                   recorded_POIPanel_Texts)
            print("---One Loop Finished !---")

            # 执行js代码（让滚动条向下偏移n个像素（作用：动态加载了更多信息））
            js = 'var q=document.body.scrollTop=10000'
            obj.execute_script(js)  # 该函数可以执行一组字符串形式的js代码

            print("---滚动条下拉---")
            print("---Sleep 2 Seconds for the more INFO Loaded !---")
            time.sleep(2)

            vip_panel_list = obj.find_elements_by_class_name("weibo-text")
            newlength_panel_list = len(vip_panel_list)
            print("---newlength_panel_list---", newlength_panel_list)

            if not newlength_panel_list > length_panel_list:
                length_panel_change = False

                return recorded_POIPanel_Texts
            else:
                length_panel_list = newlength_panel_list


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


def getUSRID(obj):
    current_url = obj.current_url  # <Sample>: current_url = 'https://m.weibo.cn/u/2145605952?uid=2145605952&luicode=10000011&lfid=2304410021114.305248_30.60786_'
    construct1 = current_url.split('/')
    current_url = construct1[4]
    construct1 = current_url.split('?')
    uid = construct1[0]

    return uid


def constructURL(random, rightBoundage, downBoundage, ori_lng, ori_lat):
    lng = random.uniform(ori_lng, rightBoundage)  # 随机数范围
    lat = random.uniform(downBoundage, ori_lat)  # 随机数范围

    BEGIN_URL = 'https://m.weibo.cn/p/index?containerid=2304410021' + str(lng) + '_' + str(
        lat) + '_&needlocation=1&uid=&count=10&page=1&luicode=&lfid=&featurecode='

    print("---New lng : ", lng, " lat : ", lat, "---")

    return BEGIN_URL, lng, lat


def configDriver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")

    obj = webdriver.PhantomJS(executable_path='./phantomjs-2.1.1-windows/bin/phantomjs.exe',
                              desired_capabilities=dcap)  # 加载驱动

    return obj


def mkDocument(_dir, uid):
    docPath = _dir + uid
    if not os.path.exists(docPath):
        os.makedirs(docPath)

        return docPath
    else:
        return ''


def obj_Get(obj, BEGIN_URL):
    getURLProcess_mark = True

    tryConnectLoop_mark = True

    while tryConnectLoop_mark:
        try:
            eventlet.monkey_patch()
            while getURLProcess_mark:
                with eventlet.Timeout(10, False):
                    obj.get(BEGIN_URL)
                    getURLProcess_mark = False  # 从而退出循环

            tryConnectLoop_mark = False  # 从而退出最外层循环
        except:
            tryConnectLoop_mark = True

            print("---obj_Get Error !---sleep 3 seconds !---")
            time.sleep(3)

    return obj


if __name__ == "__main__":

    random = np.random.RandomState(12)  # RandomState生成随机数种子

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

    obj = configDriver()

    # 设置代理IP
    proxy_addr = "122.241.72.191:808"

    ori_lng = 113.6833
    ori_lat = 31.36666
    """Sample lng : 114.78330000000042 lat : 31.36666"""
    rightBoundage = 115.0833
    downBoundage = 29.9666

    BEGIN_URL, lng, lat = constructURL(random, rightBoundage, downBoundage, ori_lng, ori_lat)
    obj = obj_Get(obj, BEGIN_URL)
    print("lng : " + str(lng) + " lat : " + str(lat))

    Loop_Mark = True
    while Loop_Mark:
        print("---waite 2 second for Get(BEGIN_URL) !---")
        time.sleep(2)

        """声明index暂存变量
            目前是在“此地周边”进行的列表性点击
        """
        click_i = 1 # 注意：初始值为1 是规律

        scorll_i = 0  # 记录滚动滑块的次数

        """try:"""
        box_list = obj.find_elements_by_class_name("m-text-cut")
        box_length = len(box_list)
        print("box_length : ", box_length)

        while click_i < box_length:

            boxes_sample = box_list[click_i]
            boxes_sample.click()
            obj.refresh()

            print("lng : " + str(lng) + " lat : " + str(lat))

            print("---waite 1 second for the refreshing---")
            time.sleep(1)

            try:
                docPath = ''
                uid = getUSRID(obj)
                # 临时测试：--------------------------------------
                # 测试：5313321908
                # 曾出错测试：3904590483
                # uid = '3904590483'
                # 曾出错测试：6174060595
                # uid = '6174060595'
                # 曾出错测试：'3636204462'
                # uid = '3636204462'
                print("uid : ", uid)
            except:
                uid = 'abc'

            try:
                uid_int = int(uid)  # 有时：uid 不是数字，要跳过
                docPath = mkDocument(_dir, uid)
            except:
                docPath = ''

            if docPath != '':
                writeTimeLog(_dir, uid, timeLogFileName)

                file = docPath + "/" + uid + ".json"

                """This is the logic left before:

                host_url = 'https://m.weibo.cn/u/' + str(uid)
                print("---host_url !---")

                recorded_POIPanel_Texts = get_Weibo_host(obj, host_url, file)

                POIExist_Count = len(recorded_POIPanel_Texts)
            """

                getWeibo(uid, file, lng, lat)
            else:
                print("The Account Exists ! ")


            click_i += 2  # 去click 下一个img-box
                            # 注意：+2 是规律

            print("click_i : ", click_i)
            print("scroll_i : ", scorll_i)

            if click_i < box_length:
                print("---click_i < box_length !---")
                obj = obj_Get(obj, BEGIN_URL)

                print("---waite 2 second for Get(BEGIN_URL) !---")
                time.sleep(2)

                box_list = obj.find_elements_by_class_name("m-text-cut")
                box_length = len(box_list)
                print("---newlength_panel_list---", box_length)

            elif click_i >= box_length:
                print("---click_i >= box_length !---")

                scorll_i += 1
                if scorll_i == 2:
                    break  # 从而退出该while 循环

                # 执行js代码（让滚动条向下偏移n个像素（作用：动态加载了更多信息））
                js = 'var q=document.body.scrollTop=10000'
                obj.execute_script(js)  # 该函数可以执行一组字符串形式的js代码

                print("---滚动条下拉---")
                print("---Sleep 2 Seconds for the more INFO Loaded !---")
                time.sleep(2)

                box_list = obj.find_elements_by_class_name("m-img-box")
                new_box_list_length = len(box_list)
                print("---newlength_panel_list---", new_box_list_length)

                if not new_box_list_length > click_i:
                    break  # 从而退出该while 循环
                else:
                    box_length = new_box_list_length

        print("---退出while 循环---")

        """上面的做完才构造新的URL"""
        BEGIN_URL, lng, lat = constructURL(random, rightBoundage, downBoundage, ori_lng, ori_lat)
        obj = obj_Get(obj, BEGIN_URL)

        """
        except:
            print("---Error Appearance---")
            time.sleep(2)
        """
