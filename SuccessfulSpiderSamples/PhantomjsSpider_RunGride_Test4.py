# encoding=utf-8
# Date: 2018-09-05


import json
import cmath
import os
import re
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import time
import urllib.request


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
    data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')

    return data


# 获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data = use_proxy(url, proxy_addr)

    containerid = ''

    content = json.loads(data).get('data')
    for data in content.get('tabsInfo').get('tabs'):
        if (data.get('tab_type') == 'weibo'):
            containerid = data.get('containerid')

    return containerid


# 获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id  # <Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'

    data = use_proxy(url,
                     proxy_addr)  # <Sample>: data = {"ok":1,"data":{"userInfo":{"id":1259110474,"screen_name":"\u8d75\u4e3d\u9896","profile_image_url":"https:\/\/tvax1.sinaimg.cn\/crop.0.0.684.684.180\/4b0c804aly8fu4lq4gumvj20j00j0ta6.jpg","profile_url":"https:\/\/m.weibo.cn\/u\/1259110474?uid=1259110474&luicode=10000011&lfid=1005051259110474","statuses_count":1342,"verified":true,"verified_type":0,"verified_type_ext":1,"verified_reason":"\u6f14\u5458\uff0c\u4ee3\u8868\u4f5c\u54c1\u300a\u82b1\u5343\u9aa8\u300b\u300a\u6749\u6749\u6765\u4e86\u300b\u300a\u9646\u8d1e\u4f20\u5947\u300b","close_blue_v":false,"description":"","gender":"f","mbtype":12,"urank":46,"mbrank":7,"follow_me":false,"following":false,"followers_count":68521642,"follow_count":461,"cover_image_phone":"https:\/\/wx4.sinaimg.cn\/crop.0.0.640.640.640\/4b0c804aly1fdwoyoobn7j20e60e83z9.jpg","avatar_hd":"https:\/\/wx1.sinaimg.cn\/orj480\/4b0c804aly8fu4lq4gumvj20j00j0ta6.jpg","like":false,"like_me":false,"toolbar_menus":[{"type":"profile_follow","name":"\u5173\u6ce8","pic":"","params":{"uid":1259110474}},{"type":"link","name":"\u804a\u5929","pic":"http:\/\/h5.sinaimg.cn\/upload\/2015\/06\/12\/2\/toolbar_icon_discuss_default.png","params":{"scheme":"sinaweibo:\/\/messagelist?uid=1259110474&nick=\u8d75\u4e3d\u9896"},"scheme":"https:\/\/passport.weibo.cn\/signin\/welcome?entry=mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fapi%2Fcontainer%2FgetIndex%3Ftype%3Duid%26value%3D1259110474"},{"type":"link","name":"\u6587\u7ae0","pic":"","params":{"scheme":"sinaweibo:\/\/cardlist?containerid=2303190002_445_1259110474_WEIBO_ARTICLE_LIST_DETAIL&count=20"},"scheme":"https:\/\/m.weibo.cn\/p\/index?containerid=2303190002_445_1259110474_WEIBO_ARTICLE_LIST_DETAIL&count=20&luicode=10000011&lfid=1005051259110474"}]},"avatar_guide":[],"fans_scheme":"https:\/\/m.weibo.cn\/p\/index?containerid=231051_-_fans_intimacy_-_1259110474&luicode=10000011&lfid=1005051259110474","follow_scheme":"https:\/\/m.weibo.cn\/p\/index?containerid=231051_-_followersrecomm_-_1259110474&luicode=10000011&lfid=1005051259110474","tabsInfo":{"selectedTab":1,"tabs":[{"title":"\u4e3b\u9875","tab_type":"profile","containerid":"2302831259110474"},{"title":"\u5fae\u535a","tab_type":"weibo","containerid":"1076031259110474","apipath":"\/profile\/statuses","url":"\/index\/my"},{"title":"\u8d85\u8bdd","tab_type":"cardlist","containerid":"2314751259110474"},{"title":"\u76f8\u518c","tab_type":"album","containerid":"1078031259110474","filter_group_info":{"title":"\u5168\u90e8\u7167\u7247(0)","icon":"http:\/\/u1.sinaimg.cn\/upload\/2014\/06\/10\/userinfo_icon_album.png","icon_name":"\u4e13\u8f91","icon_scheme":""}}]},"showAppTips":1,"scheme":"sinaweibo:\/\/userinfo?uid=1259110474&luicode=10000011&lfid=1005051259110474&from=1110006030"}}
    content = json.loads(data).get('data')

    profile_url = content.get('userInfo').get('profile_url')
    name = content.get('userInfo').get('screen_name')
    gender = content.get('userInfo').get('gender')

    return gender


def catchWeibo_HTML(scheme):
    req = urllib.request.Request(
        scheme)  # <Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'
    req.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")

    data = urllib.request.urlopen(req)
    print("---sleep---0.5---second---")
    time.sleep(0.5)

    read_data = data.read().decode('utf-8', 'ignore')

    return read_data


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
    try:
        if (weibo_page_title != []):
            if weibo_page_title[0] != '':
                if not ("视频" in weibo_page_title[0]):
                    if not ("#" in weibo_page_title[0]):
                        if ("·" in weibo_page_title[0]):
                            weibo_page_title = weibo_page_title[0]

                            try:
                                weibo_content1 = ''  # Initialize the variable weibo_page_title
                                for script in m_script:
                                    res_content1 = r'"content1": "(.*?)"'

                                    weibo_content1 = re.findall(res_content1, script)
                                weibo_content1 = weibo_content1[0]

                                weibo_created_time = ''  # Initialize the variable weibo_created_time
                                for script in m_script:
                                    # 注意：created_at 是一个类似json 的key
                                    res_created_time = r'"created_at": "(.*?)"'

                                    weibo_created_time = re.findall(res_created_time, script)
                                weibo_created_time = weibo_created_time[0]

                                weibo_uid = ''
                                for script in m_script:
                                    res_uid = r'"id": (.*?),'

                                    weibo_uid = re.findall(res_uid, script)
                                weibo_uid = weibo_uid[1]

                                weibo_pic_url = []
                                for script in m_script:
                                    res_url = r'"url": "(.*?)"'

                                    weibo_pic_url = re.findall(res_url, script)

                                weibo_gender = ''
                                for script in m_script:
                                    res_gender = r'"gender": "(.*?)"'

                                    weibo_gender = re.findall(res_gender, script)
                                weibo_gender = weibo_gender[0]

                            except Exception as e:
                                print(e)
    except Exception as e:
        print(e)

    return weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1


def extractINFO(HTML_data):
    html_script = r'<script>(.*?)</script>'

    weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1 = catchFromScipt(
        html_script, HTML_data)

    return weibo_uid, weibo_created_time, weibo_pic_url, weibo_gender, weibo_page_title, weibo_content1


def getYear(weibo_created_time):
    year = weibo_created_time.split(' ')
    year = year[5]

    return year


def tryGetData(i, weibo_url, proxy_addr, recordedINFO, process_mark):
    data = use_proxy(weibo_url, proxy_addr)

    content = json.loads(data).get('data')

    cards = content.get('cards')

    if (len(cards) > 0):
        for j in range(len(cards)):

            print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")

            card_type = cards[j].get('card_type')

            if (card_type == 9):

                """Initialize data dict"""
                data_dict = {}

                mblog = cards[j].get('mblog')

                idstr = mblog.get('idstr')  # 微博的idstr，储存起来，为后续爬虫再用
                # <Sample>: idstr = 4281561774373070
                # (Sample): tested_url of weibo: https://m.weibo.cn/status/4281561774373070

                scheme = cards[j].get('scheme')  # <Sample>: scheme = 'https://m.weibo.cn/status/GydNfilDo?mblogid=GydNfilDo&luicode=10000011&lfid=1076031995216231'
                text = mblog.get('text')

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
    else:
        process_mark = False

    i += 1

    return i, recordedINFO, process_mark


def writeData(file, recordedINFO):
    fh = open_Json_File_To_Write(file)
    for data in recordedINFO:
        a = json.dumps(data)
        b = str(a) + "\n"

        fh.write(b)

    fh.close()


# 获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id, file):
    i = 1

    recordedINFO = []  # 该博主的每条微博信息为一个元素

    process_mark = True

    while process_mark:

        """<Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474'"""
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id

        """<Sample>: url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=1259110474&containerid=1076031259110474&page=1'"""
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + \
                    '&containerid=' + get_containerid(url) + \
                    '&page=' + str(i)

        try:
            i, recordedINFO, process_mark = tryGetData(i, weibo_url, proxy_addr, recordedINFO, process_mark)

        except Exception as e:
            """
            <Attention>:
                When page out, the screen will show the following words after the orders executed

                >>>list index out of range
                >>>---Now use input to Stop this process--- 
            """
            print(e)

            print("---Now sleep for 1 second to Stop this process---")
            time.sleep(1)

        writeData(file, recordedINFO)


def configDriver():
    dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")

    obj = webdriver.PhantomJS(executable_path='L:\\USBei\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
                              desired_capabilities=dcap)  # 加载驱动

    return obj


def getUSRID(obj):
    current_url = obj.current_url  # <Sample>: current_url = 'https://m.weibo.cn/u/2145605952?uid=2145605952&luicode=10000011&lfid=2304410021114.305248_30.60786_'
    construct1 = current_url.split('/')
    current_url = construct1[4]
    construct1 = current_url.split('?')
    uid = construct1[0]

    return uid


def constructURL(lng, lat, Inc, rightBoundage, downBoundage, ori_lng, ori_lat):
    BEGIN_URL = 'https://m.weibo.cn/p/index?containerid=2304410021' + str(lng) + '_' + str(
        lat) + '_&needlocation=1&uid=&count=10&page=1&luicode=&lfid=&featurecode='

    if lng < rightBoundage:
        lng += Inc
    if abs(lng - rightBoundage) < 0.0001:
        lng = ori_lng

    if lat > downBoundage:
        lat -= Inc
    if abs(lat - downBoundage) < 0.0001:
        lat = ori_lat

    return BEGIN_URL, lng, lat


def mkDocument(_dir, uid):
    docPath = _dir + uid
    if not os.path.exists(docPath):
        os.makedirs(docPath)

        return docPath
    else:
        return ''


if __name__ == "__main__":

    _dir = "./"
    _dir = mkDocument(_dir, "Account")
    _dir += "/"
    """
        <Attention>: 不要轻易改变该默认项
    """
    _dir = "./Account/"


    obj = configDriver()

    # 设置代理IP
    proxy_addr = "122.241.72.191:808"

    Inc = 0.001
    lng = 114.305248
    lat = 30.60786
    ori_lng = 114.305248
    ori_lat = 30.60786
    """Sample lng : 114.30724800000002 lat : 30.605859999999996"""
    rightBoundage = 114.308248
    downBoundage = 30.60386

    BEGIN_URL, lng, lat = constructURL(lng, lat, Inc, rightBoundage, downBoundage, ori_lng, ori_lat)
    obj.get(BEGIN_URL)  # 打开网址
    print("lng : " + str(lng) + " lat : " + str(lat))

    Loop_Mark = True
    while Loop_Mark:

        print("---waite 2 second for the following click---")
        time.sleep(2)
        try:
            obj.find_element_by_class_name("m-img-box").click()
            obj.refresh()

            print("lng : " + str(lng) + " lat : " + str(lat))

            print("---waite 1 second for the refreshing---")
            time.sleep(0.5)

            docPath = ''
            uid = getUSRID(obj)
            docPath = mkDocument(_dir, uid)
            # 临时测试：------------------------------------------------------------------------------------------------------------------------------------------------------------
             # uid = '5147250296'
              # uid = '5534369029'

            if docPath != '':
                file = docPath + "/" + uid + ".json"
                get_weibo(uid, file)
        except:
            print("---Error Appearance---")
            time.sleep(1)

        BEGIN_URL, lng, lat = constructURL(lng, lat, Inc, rightBoundage, downBoundage, ori_lng, ori_lat)
        obj.get(BEGIN_URL)  # 打开网址

    obj.quit()  # 关闭浏览器。当出现异常时记得在任务浏览器中关闭PhantomJS，因为会有多个PhantomJS在运行状态，影响电脑性能
