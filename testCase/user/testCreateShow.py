import unittest
import paramunittest
from common import Log as Log
from common import Common
from common.ExcelReader import ExcelReader
import json
import time
from device.ApiTester import ApiTester

createShow_xls = ExcelReader().get_xls("ShowCase.xlsx", "createShow")


@paramunittest.parametrized(*createShow_xls)
class CreateShow(unittest.TestCase):
    def setParameters(self, case_name, command, duration, name, msg):
        """
        set params
        :param name:
        :param duration:
        :param command:
        :param case_name:
        :param msg:
        :return:
        """
        self.case_name = str(case_name)
        self.command = str(command)
        self.duration = str(duration)
        self.name = str(name)
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
        self.startTime = time.time()
        print(self.case_name + "測試開始前準備")
        self.log = Log.MyLog.get_log()
        self.logger = self.log.get_logger()

    def tearDown(self):
        """

        :return:
        """
        print("測試結束，輸出log完結\n\n")
        self.duration = time.time() - self.startTime

    def testCreateShow(self):
        """
        test body
        :return:
        """

        # set data
        data = {'command': json.loads(self.command),
                'duration': json.loads(self.duration),
                'name': json.loads(self.name)
                }

        # test interface
        apiTester = ApiTester()
        startTime = time.time()
        self.return_json = apiTester.send_create_show_command(data)
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