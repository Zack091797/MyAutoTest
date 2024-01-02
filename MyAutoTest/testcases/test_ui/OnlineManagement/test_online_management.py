import timeit

import pytest
import pytest_check as check
from UI_Objects.OnlineManagement.OnlineManagement_Home import Management_Home_Page
from UI_Objects.OnlineManagement.ProcessCheck import ProcessCheck_Page
from UI_Objects.OnlineManagement.ProcessView import ProcessView_Page
from Utils.LogConfig.LogConfig import logHelper
from time import sleep


class TestOnlineManagement:

    @pytest.mark.dependency()
    def test_log_in(self, init_page, base_url):
        """用户登录系统"""
        home = init_page(Management_Home_Page, "home")
        home.open_url(base_url)
        # home.js_body_style_zoom("0.67")
        logHelper.info(f"打开页面:{base_url}")
        home.login_account("liuyk", "admin")
        logHelper.info(f"输入账号:liuyk, 密码:admin")
        page_title = home.get_title()
        check.is_not_in("登录", page_title)
        # 处理密码过期弹框场景
        if home.is_element_exist("//*[@id='jbox-state-state0']/div[2]/button"):
            home.click_element("//*[@id='jbox-state-state0']/div[2]/button")
        else:
            pass
        sleep(3)

    @pytest.mark.skip
    # @pytest.mark.usefixtures("reset_side_bar")
    @pytest.mark.dependency(depends=["test_log_in"], scope="class")
    def test_view_loopViewPage(self, init_page, base_url, cache):
        """循环查看业务页面加载是否报错"""
        processView: ProcessView_Page = init_page(ProcessView_Page, "processView")
        processView.choose_top_menu("流程查看")
        firstMenuLen = len(processView.locates("//*[@id='ztree']/li"))
        for i in range(firstMenuLen):
            processView.click_element(f"//*[@id='ztree']/li[{i + 1}]")
            firstMenuText = processView.get_text(f"//*[@id='ztree']/li[{i + 1}]/a/span[2]")
            secondMenuLen = len(processView.locates(f"//*[@id='ztree']/li[{i + 1}]/ul/li"))
            for j in range(int(secondMenuLen / secondMenuLen)):
                processView.click_element(f"//*[@id='ztree']/li[{i + 1}]/ul/li[{j + 1}]")
                secondMenuText = processView.get_text(f"//*[@id='ztree']/li[{i + 1}]/ul/li[{j + 1}]/a/span[2]")
                logHelper.info(f"打开菜单 {firstMenuText}->{secondMenuText}")
                processView.iframe_into_Content()
                processView.wait_condition(ConditionType=6, loc="/html/body/ul/li/a", value="流程列表")
                form_topic = processView.get_text("/html/body/ul/li/a")
                check.is_in("流程列表", form_topic)
                processView.switch_parent_frame()
                sleep(1)
        sleep(3)

    @pytest.mark.skip
    def test_view_multi_conditions_search(self, get_page_dict, init_page):
        """三方存管菜单为例，多条件组合搜索功能"""
        processView: ProcessView_Page = get_page_dict.get("processView", init_page(ProcessView_Page, "processView"))
        processView.choose_top_menu("流程查看")
        processView.choose_left_menu("证券账户开立", "[012]三方存管银行管理")

        processView.input_custMobile("13651706659")
        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        exeTime1 = timeit.default_timer()
        processView.click_btnSubmit()
        tableTrue = processView.is_element_exist("//*[@id='contentTable']/tbody/tr")
        exeTime2 = timeit.default_timer()
        exeTime = exeTime2 - exeTime1
        logHelper.info(f"查询执行时长: {exeTime}秒")
        check.is_true(tableTrue, "手机号搜索")
        if tableTrue:
            check.less(exeTime, 3, "查询时间小于3s.")
        sleep(2)
        processView.click_btnReset()

        processView.input_custName("陈大大")
        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        processView.click_btnSubmit()
        tableTrue = processView.is_element_exist("//*[@id='contentTable']/tbody/tr")
        check.is_true(tableTrue, "客户名称搜索")
        sleep(2)
        processView.click_btnReset()

        processView.input_fundAcct("1647039913")
        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        processView.click_btnSubmit()
        tableTrue = processView.is_element_exist("//*[@id='contentTable']/tbody/tr")
        check.is_true(tableTrue, "资金账号搜索")
        sleep(2)
        processView.click_btnReset()

        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        processView.click_btnSubmit()
        processStatuslen = processView.getLen_processStatus("办理成功")
        processView.click_btnProcessStatus("办理成功")
        tableLen = processView.getLen_tableInstance()
        check.equal(processStatuslen, tableLen, "流程状态单数与列表筛选单数一致")
        sleep(2)

    @pytest.mark.skip
    def test_view_formContent(self, get_page_dict, init_page):
        """三方存管菜单为例，验证表单信息"""
        processView: ProcessView_Page = get_page_dict.get("processView", init_page(ProcessView_Page, "processView"))
        processView.choose_top_menu("流程查看")
        processView.choose_left_menu("证券账户开立", "[012]三方存管银行管理")

        processView.input_timeInterval(("2023", "十二", "29"), ("2023", "十二", "29"))
        processView.click_btnSubmit()
        processView.click_btnProcessStatus("办理成功")
        tableProcessNum = processView.get_text("//*[@id='contentTable']/tbody/tr[1]/td[1]")
        tableCustName = processView.get_text("//*[@id='contentTable']/tbody/tr[1]/td[2]")
        tableFundAcct = processView.get_text("//*[@id='contentTable']/tbody/tr[1]/td[3]")
        tableProcessStatus = processView.get_text("//*[@id='contentTable']/tbody/tr[1]/td[4]")
        tableChannel = processView.get_text("//*[@id='contentTable']/tbody/tr[1]/td[5]")
        tableProcessNode = processView.get_text("//*[@id='contentTable']/tbody/tr[1]/td[6]")

        processView.click_element("//*[@id='contentTable']/tbody/tr[1]/td[1]/a")

        formXpath = lambda formTxt: f"//*[@id='tab_cont2']/div[3]/table/tbody//tr/td[text()='{formTxt}']/following-sibling::td[1]"
        formProcessFundAcct = processView.get_text(formXpath("资金账号"))
        formProcessCustName = processView.get_text(formXpath("用户姓名"))
        formProcessNode = processView.get_text(formXpath("当前节点"))
        formProcessNum = processView.get_text(formXpath("流程编号"))
        formNodeType = processView.get_text(formXpath("节点类型"))
        formChannel = processView.get_text(formXpath("渠道"))

        check.equal(formProcessFundAcct, tableFundAcct)
        check.equal(formProcessCustName, tableCustName)
        check.equal(formProcessNode, tableProcessNode)
        check.equal(formProcessNum, tableProcessNum)
        check.equal(formNodeType, tableProcessStatus)
        check.equal(formChannel, tableChannel)

    def test_check_(self, get_page_dict, init_page):
        """单向视频优先待办流程"""
        processCheck: ProcessCheck_Page = get_page_dict.get("processView", init_page(ProcessCheck_Page, "processCheck"))
        processCheck.choose_top_menu("流程审核")
        processCheck.choose_left_menu("待办流程", "待办流程")
        pendingNum = processCheck.getNum_PendingProcess("单向视频优先待办个数")
        if int(pendingNum) != 0:
            processCheck.goto_PendingProcess("进入单向视频优先待办流程列表")
        