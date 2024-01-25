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
        logHelper.info(f"打开页面:{base_url}")
        home.login_account("UI", "UItest@123")
        logHelper.info(f"输入账号:UI, 密码:UItest@123")
        page_title = home.get_title()
        check.is_not_in("登录", page_title)
        # 处理密码过期弹框场景
        if home.is_element_exist("//*[@id='jbox-state-state0']/div[2]/button"):
            home.click_element("//*[@id='jbox-state-state0']/div[2]/button")
        else:
            pass
        home.windows_PropScale(4)
        sleep(3)

    @pytest.mark.skip
    @pytest.mark.dependency(depends=["test_log_in"], scope="class")
    def test_view_loopViewPage(self, get_page_dict, init_page, base_url, cache):
        """循环查看业务页面加载是否报错"""
        processView: ProcessView_Page = get_page_dict.get("processView", init_page(ProcessView_Page, "processView"))
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
                processView.set_obviously_wait(6, loc="/html/body/ul/li/a", value="流程列表")
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
        executeTime1 = timeit.default_timer()
        processView.click_btnSubmit()
        tableTrue = processView.is_element_exist("//*[@id='contentTable']/tbody/tr")
        # processView.set_obviously_wait(2, obviously_time=20.0, loc="//*[@id='contentTable']/tbody/tr")  # 显示等待首行在页面中存在
        executeTime2 = timeit.default_timer()
        executeTime = executeTime2 - executeTime1
        logHelper.info(f"查询执行时长: {executeTime}秒")
        check.is_true(tableTrue, "手机号搜索")
        check.less(executeTime, 3, "查询时间小于3s.")
        sleep(1)
        processView.click_btnReset()

        processView.input_custName("陈大大")
        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        processView.click_btnSubmit()
        tableTrue = processView.is_element_exist("//*[@id='contentTable']/tbody/tr")
        # tableTrue = processView.set_obviously_wait(2, obviously_time=20.0, loc="//*[@id='contentTable']/tbody/tr")
        check.is_true(tableTrue, "客户名称搜索")
        sleep(1)
        processView.click_btnReset()

        processView.input_fundAcct("1647039913")
        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        processView.click_btnSubmit()
        tableTrue = processView.is_element_exist("//*[@id='contentTable']/tbody/tr")
        # tableTrue = processView.set_obviously_wait(2, obviously_time=20.0, loc="//*[@id='contentTable']/tbody/tr")
        check.is_true(tableTrue, "资金账号搜索")
        sleep(1)
        processView.click_btnReset()

        processView.input_timeInterval(("2023", "十二", "1"), ("2023", "十二", "28"))
        processView.click_btnSubmit()
        processStatuslen = processView.getLen_processStatus("办理成功")
        processView.click_btnProcessStatus("办理成功")
        tableLen = processView.getLen_tableInstance()
        check.equal(processStatuslen, tableLen, "流程状态单数与列表筛选单数一致")

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

        formXpath = lambda \
            formTxt: f"//*[@id='tab_cont2']/div[3]/table/tbody//tr/td[text()='{formTxt}']/following-sibling::td[1]"
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

    @pytest.mark.skip
    def test_check_(self, get_page_dict, init_page):
        """单向视频优先待办流程"""
        processCheck: ProcessCheck_Page = get_page_dict.get("processView", init_page(ProcessCheck_Page, "processCheck"))
        processCheck.choose_top_menu("流程审核")
        processCheck.choose_left_menu("待办流程", "待办流程")
        pendingNum = processCheck.getNum_PendingProcess("单向视频优先待办个数")
        if int(pendingNum) != 0:
            processCheck.goto_PendingProcess("进入单向视频优先待办流程列表")
            processCheck.click_element(
                "//*[@id='contentTable']/tbody/tr/td[contains(text(), '审核中') or contains(text(), '未审核')]/following-sibling::th/a",
                2)

    # @pytest.mark.skip
    def test_check_processed_UnidirectionalVideo(self, get_page_dict, init_page):
        """已办流程-双向视频(新)"""
        processCheck: ProcessCheck_Page = get_page_dict.get("processView", init_page(ProcessCheck_Page, "processCheck"))
        processCheck.choose_top_menu("流程审核")
        processCheck.choose_left_menu("已办流程", "双向视频（新）")

        processCheck.input_custOrgName("新昌路")
        processCheck.input_custName("张天天")
        processCheck.input_custMobile("13957594644")
        processCheck.input_fundAcct("1653114382")
        processCheck.input_businessStatus("流程结束(成功)")
        processCheck.input_sysChannel("大赢家")
        processCheck.input_timeInterval(("2024", "一月", "1"), ("2024", "一月", "20"))
        processCheck.input_staffId("20230608")
        processCheck.input_auditStatus("审核通过")
        processCheck.input_auditTimeInterval(("2024", "一月", "1"), ("2024", "一月", "20"))
        processCheck.click_btnSubmit()

        sleep(3)

        searchHasResult = processCheck.is_element_exist("//*[@id='contentTable']/tbody/tr[1]")
        check.is_true(searchHasResult, "搜索存在至少一条结果")

        firstResultProcessNum = processCheck.get_text("//*[@id='contentTable']/tbody/tr[1]/td[1]/a")  # 获取第一条结果的流水号
        print(firstResultProcessNum)
        processCheck.set_obviously_wait(3, loc="//*[@id='contentTable']/tbody/tr[1]/td[1]/a")
        processCheck.click_element("//*[@id='contentTable']/tbody/tr[1]/td[1]/a")
        # sleep(3)
        while True:
            processCheck.switch_default_content()
            warning = processCheck.is_element_exist("//*[@id='jbox-state-state0']/div[2]/button")
            if warning:
                processCheck.js_click_element("//*[@id='jbox-state-state0']/div[2]/button")
            else:
                processCheck.iframe_into_Main()
                break
        processCheck.set_obviously_wait(3, loc = "/html/body/div[1]/h2")
        detailsTitle = processCheck.get_text("/html/body/div[1]/h2")

        check.is_in(firstResultProcessNum, detailsTitle, "详情标题包含目标流水号")



