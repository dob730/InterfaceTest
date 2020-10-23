import unittest
import paramunittest
from common import Log as Log
from common import Common
from common.ExcelReader import ExcelReader
import time
from device.ApiTester import ApiTester

acceptPayment_xls = ExcelReader().get_xls(None, "refund")


@paramunittest.parametrized(*acceptPayment_xls)
class Refund(unittest.TestCase):
    def setParameters(self, case_name, amount, cardcvc2, cardexpiry, cardnumber, consumerip, currency, duedate,
                      merchantnumber, ordernumber, paymemo, paymenttype, paytitle, payphone, transcode, transmode, rc,
                      rm):
        """
        set params
        :param transmode:
        :param cardnumber:
        :param cardexpiry:
        :param cardcvc2:
        :param paytitle:
        :param paymemo:
        :param consumerip:
        :param transcode:
        :param payphone:
        :param paymenttype:
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
        self.amount = str(amount)
        self.cardcvc2 = str(cardcvc2)
        self.cardexpiry = str(cardexpiry)
        self.cardnumber = str(cardnumber)
        self.consumerip = str(consumerip)
        self.currency = str(currency)
        self.duedate = str(duedate)
        self.merchantnumber = str(merchantnumber)
        self.ordernumber = str(ordernumber)
        self.paymemo = str(paymemo)
        self.paymenttype = str(paymenttype)
        self.paytitle = str(paytitle)
        self.payphone = str(payphone)
        self.transcode = str(transcode)
        self.transmode = str(transmode)
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
        self.duedate = Common.get_duedate(self.duedate)
        self.ordernumber = Common.get_day("%Y%m%d")

    def tearDown(self):
        """

        :return:
        """
        print("測試結束，輸出log完結\n\n")
        self.duration = time.time() - self.startTime

    def testRefund(self):
        """
        test body
        :return:
        """

        # set data
        data = {'amount': self.amount,
                'cardcvc2': self.cardcvc2,
                'cardexpiry': self.cardexpiry,
                'cardnumber': self.cardnumber,
                'consumerip': self.consumerip,
                'currency': self.currency,
                'duedate': self.duedate,
                'merchantnumber': self.merchantnumber,
                'ordernumber': self.ordernumber,
                'paymemo': self.paymemo.format(timestamp=self.timestamp),
                'paymenttype': self.paymenttype,
                'payphone': self.payphone,
                'paytitle': self.paytitle,
                'transmode': self.transmode,
                'timestamp': self.timestamp
                }

        # test interface
        apiTester = ApiTester()
        startTime = time.time()
        self.return_json = apiTester.send_acceptpayment_command(data, self.transcode)
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
                apiTester = ApiTester()
                self.ordernumber = Common.get_day("%Y%m%d", -1)
                data = {
                    'merchantnumber': self.merchantnumber,
                    'ordernumber': self.ordernumber,
                    'refundamount': self.amount,
                    'timestamp': self.timestamp,
                }
                self.return_json = apiTester.send_refund_command(data, self.transcode)
                Common.show_return_msg(self.return_json)
                self.info = self.return_json.json()
                self.assertEqual(self.info['rc'], str(self.rc))

            elif (self.info['rc'] == '1'):  # 需要轉導網址
                apiTester = ApiTester()
                apiTester.send_3d_auth_command(self.info['redirect_data']['strRqXML'])
                self.ordernumber = Common.get_day("%Y%m%d", -1)
                data = {
                    'merchantnumber': self.merchantnumber,
                    'ordernumber': self.ordernumber,
                    'refundamount': self.amount,
                    'timestamp': self.timestamp,
                }

                self.return_json = apiTester.send_refund_command(data, self.transcode)
                Common.show_return_msg(self.return_json)
                self.info = self.return_json.json()
                self.assertEqual(self.info['rc'], str(self.rc))
                time.sleep(1.5)
            elif (self.info['rc'] == '400'):
                self.assertIn(str(self.rm), self.info['rm'])
            elif (self.info['rc'] == '205'):
                self.assertEqual(self.info['rm'], str(self.rm))
            else:
                self.assertEqual(self.info['rc'], str(self.rc))

        if (self.return_json.status_code == 404):
            self.return_json.raise_for_status()
        if (self.return_json.status_code == 500):
            self.return_json.raise_for_status()
