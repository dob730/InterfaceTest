import json
import hashlib
from urllib.parse import urlencode
from urllib.parse import unquote
import datetime
import re
import xmltodict


def get_checksum(data, transcode):
    mySHA256 = hashlib.sha256()  # 建立一個sha256物件
    newData = {}
    # 判斷dict[key]中有空值，不加入到newData的dict裡
    for key, value in data.items():
        if data[key]:
            newData[key] = value

    querystring = urlencode(newData)  # 把 {key:value,key2:value2}轉換成key=value&key2=value2的字串
    originStr = unquote(querystring)
    hashStr = originStr + transcode
    mySHA256.update(hashStr.encode('utf-8'))
    checksum = mySHA256.hexdigest()
    return checksum

def get_hash(data, transcode):
    mySHA256 = hashlib.sha256()  # 建立一個sha256物件
    data = data['data']
    querystring = urlencode(data)  # 把 {key:value,key2:value2}轉換成key=value&key2=value2的字串
    originStr = unquote(querystring)
    hashStr = originStr + transcode
    mySHA256.update(hashStr.encode('utf-8'))
    checksum = mySHA256.hexdigest()
    return checksum

def get_time(dateFormat="%Y%m%d%H%M%S%f", addDays=0):
    timeNow = datetime.datetime.now()
    if (addDays != 0):
        anotherTime = timeNow + datetime.timedelta(days=addDays)
    else:
        anotherTime = timeNow

    return anotherTime.strftime(dateFormat)

def get_day(dateFormat="%Y%m%d", addDays=0):
    timeNow = datetime.datetime.now()
    if (addDays != 0):
        anotherTime = timeNow + datetime.timedelta(days=addDays)
    else:
        anotherTime = timeNow

    return anotherTime.strftime(dateFormat)

def show_return_msg(response):
    """
    show msg detail
    :param response:
    :return:
    """
    url = response.url
    msg = response.text
    print("\n請求地址：" + url)
    # 可以显示中文
    print("\n請求返回值：" + '\n' + json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))


def get_duedate(date):
    regex = r'[0-9]{14}'
    duedate_regex = r'{timestamp}\+[0-9]+'
    timestamp_regex = r'{timestamp}'
    if (re.match(regex, date)):
        return date
    elif (re.match(duedate_regex, date)):
        days = date.split('+')[1]
        duedate = get_time("%Y%m%d%H%M%S%f", int(days))
        date = duedate[0:14]
        return date
    elif (re.match(timestamp_regex, date)):
        date = get_time("%Y%m%d%H%M%S%f")[0:14]
        return date
    else:
        return date


def parse_xml_to_json(xml):
    strRqXML = xmltodict.parse(xml)
    strRq = json.dumps(strRqXML['MERCHANTXML'])
    return strRq
