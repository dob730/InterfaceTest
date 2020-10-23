import requests
from common import ConfigReader
from common.Log import MyLog as Log
import json

localReadConfig = ConfigReader.ConfigReader()


class HttpConfig:

    def __init__(self):
        self.scheme = localReadConfig.get_http("scheme")
        self.host = localReadConfig.get_http("baseurl")
        self.port = localReadConfig.get_http("port")
        self.timeout = localReadConfig.get_http("timeout")
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.headers = {}
        self.params = {}
        self.data = {}
        self.url = None
        self.files = {}

    def set_url(self, url):
        """
        set url
        :param: interface url
        :return:
        """
        self.url = self.scheme + '://' + self.host + ':' + self.port + url

    def set_headers(self, header):
        """
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_data(self, data):
        """
        set data
        :param data:
        :return:
        """
        self.data = data

    def req(self, method):
        """
        defined get method
        :return:
        """
        try:
            if (method == 'get'):
                response = requests.get(self.url, headers=self.headers, data=json.dumps(self.data),
                                        timeout=float(self.timeout))
                return response
            if (method == 'post'):
                response = requests.post(self.url, headers=self.headers, data=json.dumps(self.data),
                                         timeout=float(self.timeout))
                return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file
    def postWithFile(self):
        """
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, data=self.data, files=self.files,
                                     timeout=float(self.timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None
