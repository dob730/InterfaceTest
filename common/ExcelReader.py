import os
import getpathInfo  # 自己定義的內部類，該類返回項目的絕對路徑
# 調用讀Excel的第三方庫xlrd
from xlrd import open_workbook
import openpyxl

# 拿到該項目所在的絕對路徑


class ExcelReader():
    def get_xls(self, xls_name=None, sheet_name=None, start=None, end=None, repeat=None):  # xls_name填寫用例的Excel名稱 sheet_name該Excel的sheet名稱
        path = getpathInfo.get_path()
        cls = []
        # 獲取用例文件路徑
        casePath = os.path.join(path, "testFile", 'case')
        for root, dirs, files in os.walk(casePath):
            if xls_name is None:
                xlsfiles = [_ for _ in files if _.endswith('.xlsx')]
            else:
                xlsfiles = [xls_name]

            for xlsfile in xlsfiles:
                file = open_workbook(os.path.join(root, xlsfile))  # 打開用例Excel
                if sheet_name in file.sheet_names():  # 檢查分頁是否存在excel
                    sheet = file.sheet_by_name(sheet_name)  # 獲得打開Excel的sheet
                    # 獲取這個sheet內容行數
                    nrows = sheet.nrows
                    try:
                        if (start != None and end != None and repeat != None):
                            for j in range(repeat):
                                for i in range(start, end):
                                    if sheet.row_values(i)[0] != u'case_name':  # 如果這個Excel的這個sheet的第i行的第一列不等於case_name那麽我們把這行的數據添加到cls[]
                                        cls.append(sheet.row_values(i))
                        elif (start != None and end != None):
                            for i in range(start, end):
                                if sheet.row_values(i)[0] != u'case_name':
                                    cls.append(sheet.row_values(i))
                        elif (repeat != None):
                            for j in range(repeat):
                                for i in range(1, nrows):
                                    cls.append(sheet.row_values(i))
                        else:
                            for i in range(1, nrows):
                                cls.append(sheet.row_values(i))

                    except IndexError:
                        print('list index out of range')
                else:
                    wb = openpyxl.load_workbook(os.path.join(root, xlsfile))
                    wb.create_sheet(sheet_name)
                    wb.save(os.path.join(root, xlsfile))
            return cls

if __name__ == '__main__':
    ExcelReader().get_xls(None, 'cancelOrder')