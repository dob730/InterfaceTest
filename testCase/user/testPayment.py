import unittest
import paramunittest
from common import Log as Log
from common import Common
from common.ExcelReader import ExcelReader
from datetime import datetime
import time
from device.ApiTester import ApiTester

payment_xls = ExcelReader().get_xls("PaymentCase.xlsx", "payment")


@paramunittest.parametrized(*payment_xls)
class Payment(unittest.TestCase):
    def setParameters(self, case_name, amount, currency, duedate, merchantnumber, merchantordernumber, ordernumber, paymenttype, payphone, transcode, msg):
        """
        set params
        :param transcode:
        :param payphone:
        :param paymenttype:
        :param merchantordernumber:
        :param duedate:
        :param currency:
        :param amount:
        :param case_name:
        :param ordernumber:
        :param merchantnumber:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.amount = int(amount)
        self.currency = str(currency)
        self.duedate = int(duedate)
        self.merchantnumber = int(merchantnumber)
        self.merchantordernumber = int(merchantordernumber)
        self.ordernumber = int(ordernumber)
        self.paymenttype = str(paymenttype)
        self.payphone = str(payphone)
        self.transcode = str(transcode)
        self.msg = str(msg)

    def description(self):
        """

        :return:
        """
        self.case_name

    def avgDuration(self):
        """

        :return:
        """
        self.duration

    def setUp(self):
        """

        :return:
        """
        print(self.case_name + "測試開始前準備")
        self.startTime = time.time()
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()
        currenttime = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S%f')
        self.timestamp = currenttime[:-4]

    def tearDown(self):
        """

        :return:
        """
        print("測試結束，輸出log完結\n\n")
        self.duration = time.time() - self.startTime

    def testPayment(self):
        """
        test body
        :return:
        """

        # set data
        data = {'amount': self.amount,
                'currency': self.currency,
                'duedate': self.duedate,
                'merchantnumber': self.merchantnumber,
                'merchantordernumber': self.merchantordernumber,
                'ordernumber': self.ordernumber,
                'paymenttype': self.paymenttype,
                'payphone': self.payphone,
                'timestamp': self.timestamp
                }



        # test interface
        apiTester = ApiTester()
        startTime = time.time()
        self.return_json = apiTester.send_payment_command(data, self.transcode)
        echoTime = time.time() - startTime
        print('duration:' + str(echoTime))
        # check result
        self.checkResult()

    def checkResult(self):
        """

        :return:
        """

        # self.info = self.return_json.json()
        Common.show_return_msg(self.return_json)