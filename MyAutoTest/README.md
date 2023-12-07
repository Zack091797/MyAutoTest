# MyAutoTest

集成接口和UI自动化测试框架
框架：
1.引用allure报告
2.引用pytest-check断言
3.引用pytest-sugar终端运行进度条
4.日志记录，使用pytest的logging
5.数据库连接方式，在fixture中返回conn连接对象，每个用例

api:
1.接口api参数化 yaml文件作为数据模板，csv作为数据来源
2.requests封装，目前是简单封装，后续还需完善

UI：
1.PO的基类basepage，大部分已封装

修改源码：
1.\site-packages\_pytest\logging.py 579 修改文件的读写模式覆写"w"变更为追加读写"a+"