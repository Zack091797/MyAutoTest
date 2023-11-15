import xlwings as xw


class XlwingsHelper:

    def __init__(self):

        self.app = xw.App(visible=True, add_book=False)
        self.app.display_alerts = False  # 关闭一些提示信息，加快运行速度
        self.app.screen_updating = True  # 更新显示工作表的内容，默认为True，关闭可提升运行速度
        self.workbook = None
        self.sheet = None

    # 建立上下文管理器-方法1：__enter__()、__exit__()
    # def __enter__(self, *args, **kwargs):
    #     pass
    #
    # def __exit__(self, *args, **kwargs):
    #     pass

    # 建立上下文管理器-方法2：装饰器@contextmanager、生成器方法yield
    # @contextmanager
    # def operate_excel_elements(self, ):
    #     self.app = xw.App(visible=True, add_book=False)
    #     yield self.app
    #     self.exit_app(kill=True)

    def exit_app(self, kill=False):
        """
        关闭app对象打开的Excel桌面进程

        :param kill:
        :return:
        """
        if kill is True:
            self.app.kill()
        else:
            self.app.quit()

    def create_excel_workbook(self):
        """
        新建工作簿

        :param save_path:
        :return:
        """
        self.workbook = self.app.books.add()

    def open_excel_workbook(self, file_path):
        """
        打开现有工作簿

        :param file_path:
        :return:
        """
        self.workbook = self.app.books.open(file_path)
        return self.workbook

    def save_excel_workbook(self, file_path=None):
        """
        保存工作簿

        :param file_path:
        :return:
        """
        if file_path is None:
            self.workbook.safve()
        else:
            self.workbook.save(file_path)

    def active_excel_workbook(self):
        """
        获取当前活动的工作簿

        :return:
        """
        self.workbook = self.app.books.active

    def create_excel_sheet(self, sheet_name="New Sheet", front_sheet=None):
        """
        新建工作表

        :param sheet_name:
        :param front_sheet:
        :return:
        """
        self.sheet = self.workbook.sheets.add(sheet_name, after=front_sheet)

    def active_excel_sheet(self):
        """
        获取当前活动的工作表

        :return:
        """
        self.sheet = self.workbook.sheets.active

    def index_excel_sheet(self, sheet_index: int):
        """
        按索引获取工作表

        :param sheet_index:
        :return:
        """
        self.sheet = self.workbook.sheets[sheet_index]

    def name_excel_sheet(self, sheet_name: str):
        """
        按表名获取工作表

        :param sheet_name:
        :return:
        """
        self.sheet = self.workbook.sheets[sheet_name]


