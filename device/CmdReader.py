import json
import getpathInfo
import os



class CmdReader:
    def __init__(self):
        proDir = getpathInfo.get_path()
        urlFile = os.path.join(proDir, "device","InterfaceUrl.json")
        with open(urlFile) as f:
            self.data = json.load(f)

    def get_url_method_from_create_show(self):
        """
        get value by key
        :return:
        """
        info = self.data['Show']
        group = info['createShow']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_from_cancel_order(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['cancelOrder']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_payment(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['payment']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_accept_payment(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['acceptPayment']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_simulator(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['simulator']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_3dAuth(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['3dAuth']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_3dReceive(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['3dReceive']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_refund(self):
        """
        get value by key
        :return:
        """
        info = self.data['Payment']
        group = info['refund']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_refund_reversal(self):
        info = self.data['Payment']
        group = info['refundReversal']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_query_order(self):
        info = self.data['Payment']
        group = info['queryOrder']
        url = group['url']
        method = group['method']
        return url, method

    def get_url_method_rec_billing(self):
        info = self.data['RecBilling']
        group = info['createBilling']
        url = group['url']
        method = group['method']
        return url, method