# encoding=utf-8
# Date: 2018-008-31


import json
import base64
import requests


def spider(session):
    # The URL following is "此地周边"
     # URL = r'https://m.weibo.cn/p/index?containerid=2304410021111.775248_30.18786_B2094655D464AAFA449D&needlocation=1&uid=2808429250&count=10&page=1&luicode=10000011&lfid=100101B2094655D464AAFA449D&featurecode=20000320'

    # The URL following is One Specific UserID
    URL = r'https://m.weibo.cn/detail/4279239991151924'

    r = session.get(URL)
    print(r.text)


def login(username, password):

    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')

    postData = {

        "entry": "sso",

        "gateway": "1",

        "from": "null",

        "savestate": "30",

        "useticket": "0",

        "pagerefer": "",

        "vsnf": "1",

        "su": username,

        "service": "sso",

        "sp": password,


        "sr": "1440*900",

        "encoding": "UTF-8",

        "cdult": "3",

        "domain": "sina.com.cn",

        "prelt": "0",

        "returntype": "TEXT",

    }

    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'

    session = requests.Session()
    res = session.post(loginURL, data = postData)

    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)

    if info["retcode"] == "0":

        print("登录成功")

        # 把cookies添加到headers中，必须写这一步，否则后面调用API 失败
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)    # <Attention>: The first string is 分号 ！
        session.headers["cookie"] = cookies

    else:
        print("登录失败，原因： %s" % info["reason"])

    return session


if __name__ == '__main__':

    account = "18100000000"
    passwd = "**************"

    session = login(account, passwd)

    spider(session)
