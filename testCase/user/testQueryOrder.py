import unittest
import paramunittest
from common import Log as Log
from common import Common
from common.ExcelReader import ExcelReader
import time
from device.ApiTester import ApiTester

acceptPayment_xls = ExcelReader().get_xls(None, "queryOrder")


@paramunittest.parametrized(*acceptPayment_xls)
class QueryOrder(unittest.TestCase):
    def setParameters(self, case_name, merchantnumber, ordernumber, transcode, rc, rm):
        """
        set params
        :param transcode:
        :param rm:
        :param rc:
        :param case_name:
        :param ordernumber:
        :param merchantnumber:
        :return:
        """
        self.case_name = str(case_name)
        self.merchantnumber = str(merchantnumber)
        self.ordernumber = str(ordernumber)
        self.transcode = str(transcode)
        self.rc = str(rc)
        self.rm = str(rm)

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
        currenttime = Common.get_time("%Y%m%d%H%M%S%f")
        self.timestamp = currenttime[0:14]

    def tearDown(self):
        """

        :return:
        """
        print("測試結束，輸出log完結\n\n")
        self.duration = time.time() - self.startTime

    def testQueryOrder(self):
        """
        test body
        :return:
        """

        # set data
        data = {
                'merchantnumber': self.merchantnumber,
                'ordernumber': self.ordernumber,
                'timestamp': self.timestamp
                }

        # test interface
        apiTester = ApiTester()
        startTime = time.time()
        self.return_json = apiTester.send_query_order_command(data, self.transcode)
        echoTime = time.time() - startTime
        print('duration:' + str(echoTime))
        # check result
        self.checkResult()

    def checkResult(self):
        """

        :return:
        """
        self.info = self.return_json.json()
        Common.show_return_msg(self.return_json)

        if (self.return_json.status_code == 200):
            if (self.info['rc'] == '0'):
                self.assertEqual(self.info['rc'], str(self.rc))
            elif (self.info['rc'] == '400'):
                self.assertEqual(self.info['rm'], str(self.rm))
            elif (self.info['rc'] == '206'):  # 交易金額過高或低, 時效已超過
                self.assertEqual(self.info['rm'], str(self.rm))
            elif (self.info['rc'] == '205'):
                self.assertEqual(self.info['rm'], str(self.rm))
            else:
                self.assertEqual(self.info['rc'], str(self.rc))

        if (self.return_json.status_code == 404):
            self.return_json.raise_for_status()
        if (self.return_json.status_code == 500):
            self.return_json.raise_for_status()
