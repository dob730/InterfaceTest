import os
import unittest
from common.Log import MyLog as Log
from common.ConfigReader import ConfigReader
from common.HTMLTestRunner import HTMLTestRunner
import getpathInfo


from common.EmailConfig import MyEmail


class AllTest:
    def __init__(self):
        localReadConfig = ConfigReader()
        path = getpathInfo.get_path()
        self.log = Log.get_log()
        self.logger = self.log.get_logger()
        self.resultPath = self.log.get_report_path()
        self.on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(path, "caselist.txt")
        self.caseFile = os.path.join(path, "testCase")
        self.caseList = []
        self.logger.info('resultPath' + self.resultPath)  # 將resultPath的值輸入到日誌，方便定位查看問題
        self.logger.info('caseListFile' + self.caseListFile)  # 同理
        self.logger.info('caseList' + str(self.caseList))  # 同理
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        set case list
        :return:
        """
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):  # 如果data非空且不以#開頭
                self.caseList.append(data.replace("\n", ""))  # 讀取每行數據會將換行轉換為\n，去掉每行數據中的\n
        fb.close()

    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        self.set_case_list()  # 通過set_case_list()拿到caselist元素組
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:  # 從caselist元素組中循環取出case
            case_name = case.split("/")[-1]  # 通過split函數來將aaa/bbb分割字符串，-1取後面，0取前面
            print(case_name + ".py")  # 打印出取出來的名稱
            # 批量加載用例，第一個參數為用例存放路徑，第一個參數為路徑文件名
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)  # 將discover存入suite_module元素組

        if len(suite_module) > 0:

            for suite in suite_module:  # 判斷suite_module元素組是否存在元素
                for test_name in suite:  # 如果存在，循環取出元素組內容，命名為suite
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()  # 調用set_case_suite獲取test_suite
            if suit is not None:
                self.logger.info("********TEST START********")
                fp = open(self.resultPath, 'wb')  # 打開result/20181108/report.html測試報告文件，如果不存在就創建
                # 调用HTMLTestRunner
                runner = HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                runner.run(suit)
            else:
                self.logger.info("Have no case to test.")
        except Exception as ex:
            self.logger.error(str(ex))
        finally:
            self.logger.info("*********TEST END*********")
            fp.close()
            # send test report by email
            if self.on_off == 'on':
                self.email.send_email()
                self.logger.info("Send report email to developer.")
            elif self.on_off == 'off':
                self.logger.info("Doesn't send report email to developer.")
            else:
                self.logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
