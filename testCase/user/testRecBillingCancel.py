import unittest
import paramunittest
from common import Log as Log
from common import Common
from common.ExcelReader import ExcelReader
import time
from device.ApiTester import ApiTester

recBilling_xls = ExcelReader().get_xls("RecBilling.xlsx", "recBillingCancel")


@paramunittest.parametrized(*recBilling_xls)
class RecBillingCancel(unittest.TestCase):
    def setParameters(self, case_name, action, merchantnumber, org_recbillnumber, recbillname, recbillinfo_name,
                      recbillinfo_verify, amount, payername,
                      cellphone_1, cellphone_2, cellphone_3, memo, transcode, rc, rm):
        """
        set params

        :return:
        """
        self.case_name = str(case_name)
        self.amount = str(amount)
        self.action = str(action)
        self.merchantnumber = str(merchantnumber)
        self.org_recbillnumber = str(org_recbillnumber)
        self.recbillname = str(recbillname)
        self.recbillinfo_name = str(recbillinfo_name)
        self.recbillinfo_verify = str(recbillinfo_verify)
        self.payername = str(payername)
        self.cellphone_1 = str(cellphone_1)
        self.cellphone_2 = str(cellphone_2)
        self.cellphone_3 = str(cellphone_3)
        self.memo = str(memo)
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

    def testRecBillingCancel(self):
        """
        test body
        :return:
        """

        time.sleep(1)
        # set data
        data = {
            'data': {'action': self.action,
                     'amount': self.amount,
                     'cellphone_1': self.cellphone_1,
                     'memo': self.memo,
                     'merchantnumber': self.merchantnumber,
                     'org_recbillnumber': self.org_recbillnumber.format(timestamp=self.timestamp),
                     'payername': self.payername,
                     'recbillinfo_name': self.recbillinfo_name,
                     'recbillinfo_verify': self.recbillinfo_verify,
                     'recbillname': self.recbillname,

                     }
        }



        # test interface
        apiTester = ApiTester()
        startTime = time.time()
        self.return_json = apiTester.send_rec_billing_command(data, self.transcode)
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
            if (self.info['rc'] == '0000'):
                self.assertEqual(self.info['rc'], str(self.rc))
                apiTester = ApiTester()
                data = {
                    'data': {'action': 'cancel',
                             'merchantnumber': self.merchantnumber,
                             'org_recbillnumber': self.org_recbillnumber.format(timestamp=self.timestamp),
                             }
                }
                self.return_json = apiTester.send_rec_billing_cancel_command(data, self.transcode)
                Common.show_return_msg(self.return_json)

            elif (self.info['rc'] == '400'):
                self.assertIn(str(self.rm), self.info['rm'])
            elif (self.info['rc'] == '1'):  # 需要轉導網址
                # apiTester = ApiTester()
                # self.return_json = apiTester.send_simulator_command()
                self.assertEqual(self.info['merchantnumber'], str(self.merchantnumber))
            elif (self.info['rc'] == '206'):  # 交易金額過高或低, 時效已超過
                self.assertIn(str(self.rm), self.info['rm'])
            elif (self.info['rc'] == '205'):
                self.assertEqual(self.info['rm'], str(self.rm))
            else:
                self.assertEqual(self.info['rc'], str(self.rc))

        if (self.return_json.status_code == 404):
            self.return_json.raise_for_status()
        if (self.return_json.status_code == 500):
            self.return_json.raise_for_status()
