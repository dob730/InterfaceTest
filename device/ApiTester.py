from common.HttpConfig import HttpConfig
from device.CmdReader import CmdReader
from common.UrlParamParser import UrlParamPaser
from common.Common import get_checksum
from common.Common import get_hash
from common.Common import parse_xml_to_json
import base64
from collections import OrderedDict
from bs4 import BeautifulSoup

class ApiTester:
    def __init__(self):
        pass

    def send_create_show_command(self, data):
        httpConfig = HttpConfig()
        url, method = CmdReader().get_url_method_from_create_show()
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/json'})
        httpConfig.set_data(data)
        return_json = httpConfig.req(method)
        return return_json

    def send_cancel_order_command(self, merchantnumber, ordernumber, timestamp, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_from_cancel_order()
        params = {'merchantnumber': merchantnumber, 'ordernumber': ordernumber, 'timestamp': timestamp}
        params = dict(sorted(params.items()))  # sorted dictionary by key
        checksum = get_checksum(params, transcode)  # queryString+transcode取得checksum
        params.update({'checksum': checksum})
        url = UrlParamPaser().get_url(path, params)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_payment_command(self, params, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_payment()
        params = dict(sorted(params.items()))  # sorted dictionary by key
        checksum = get_checksum(params, transcode)  # queryString+transcode取得checksum
        params.update({'checksum': checksum})
        url = UrlParamPaser().get_url(path, params)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_acceptpayment_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_accept_payment()
        data = dict(sorted(data.items()))  # sorted dictionary by key
        checksum = get_checksum(data, transcode)  # queryString+transcode取得checksum
        data.update({'checksum': checksum})
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_simulator_command(self):
        httpConfig = HttpConfig()
        data = {'PaymentID': 'MTIxNjMwMDAwMDgwMjk3OA=='}
        path, method = CmdReader().get_url_method_simulator()
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_3d_auth_command(self, xml):
        strRqJson = parse_xml_to_json(xml)
        httpConfig = HttpConfig()
        byteStrRqJson = strRqJson.encode('UTF-8')
        strRq = base64.b64encode(byteStrRqJson)
        data = {'strRq': strRq, 'trans_pwd': '1'}
        path, method = CmdReader().get_url_method_3dAuth()
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_receive_3d_command(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        httpConfig = HttpConfig()
        strOrderInfo = soup.find('input', {'name': 'strOrderInfo'})["value"]
        strRsXML = soup.find('input', {'name': 'strRsXML'})["value"]
        data = {'strOrderInfo': strOrderInfo, 'strRsXML': strRsXML}
        path, method = CmdReader().get_url_method_3dReceive()
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_refund_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_refund()
        data = dict(sorted(data.items()))  # sorted dictionary by key
        checksum = get_checksum(data, transcode)  # queryString+transcode取得checksum
        data.update({'checksum': checksum})
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_refund_reversal_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_refund_reversal()
        data = dict(sorted(data.items()))  # sorted dictionary by key
        checksum = get_checksum(data, transcode)  # queryString+transcode取得checksum
        data.update({'checksum': checksum})
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_query_order_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_query_order()
        data = dict(sorted(data.items()))  # sorted dictionary by key
        checksum = get_checksum(data, transcode)  # queryString+transcode取得checksum
        data.update({'checksum': checksum})
        url = UrlParamPaser().get_url(path, data)
        httpConfig.set_url(url)
        httpConfig.set_headers({'content-type': 'application/x-www-form-urlencoded'})
        return_json = httpConfig.req(method)
        return return_json

    def send_rec_billing_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_rec_billing()
        new_data = OrderedDict()
        for key, val in data.items():  # go through the dictionary
            new_data[key] = OrderedDict(sorted(val.items()))  # sort according to keys
        checksum = get_hash(new_data, transcode)  # queryString+transcode取得checksum
        data.update({'hash': checksum})
        httpConfig.set_data(data)
        httpConfig.set_url(path)
        httpConfig.set_headers({'content-type': 'application/json'})
        return_json = httpConfig.req(method)
        return return_json

    def send_rec_billing_writeoff_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_rec_billing()
        new_data = OrderedDict()
        for key, val in data.items():  # go through the dictionary
            new_data[key] = OrderedDict(sorted(val.items()))  # sort according to keys
        checksum = get_hash(new_data, transcode)  # queryString+transcode取得checksum
        data.update({'hash': checksum})
        httpConfig.set_data(data)
        httpConfig.set_url(path)
        httpConfig.set_headers({'content-type': 'application/json'})
        return_json = httpConfig.req(method)
        return return_json

    def send_rec_billing_cancel_command(self, data, transcode):
        httpConfig = HttpConfig()
        path, method = CmdReader().get_url_method_rec_billing()
        new_data = OrderedDict()
        for key, val in data.items():  # go through the dictionary
            new_data[key] = OrderedDict(sorted(val.items()))  # sort according to keys
        checksum = get_hash(new_data, transcode)  # queryString+transcode取得checksum
        data.update({'hash': checksum})
        httpConfig.set_data(data)
        httpConfig.set_url(path)
        httpConfig.set_headers({'content-type': 'application/json'})
        return_json = httpConfig.req(method)
        return return_json