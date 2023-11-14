import os
from pathlib import *
import xlwings as xw



class ExcelHelper:

    def __init__(self):
        self.app = xw.App(visible=True, add_book=False)

    def create_excel_workbook(self, save_path):
        app = xw.App(visible=True, add_book=False)
        workbook = app.books.add()
        workbook.save(save_path)
        app.quit()

    def get_excel_data(self, excel_path: str):
        app = xw.App(visible=True, add_book=False)
        try:
            workbook = app.books.open(excel_path)
        except FileNotFoundError as err:
            print(f"指定路径不存在目标Excel文件, 请检查! --> {err}")

    def set_excel_data(self, excel_path: str, value):
        pass


