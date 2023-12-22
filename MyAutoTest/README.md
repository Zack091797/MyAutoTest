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
3.${get_cache("cache_key", None)} 获取pytest的cache缓存中的value

UI：
1.PO的基类basepage，大部分已封装

修改源码：
1.\site-packages\_pytest\logging.py 579 修改文件的读写模式覆写"w"变更为追加读写"a+"




cache存储提取的字段，单条用例执行OK，批量执行可能存在重复的key导致覆盖的情况，需要优化
2.base_url 工厂化
3.SchemaJson校验
4.data多段，提取符合要求的参数, 提取的正则表达式和jsonpath要进行封装，处理提取可能的异常
5.设置一些元件接口，快速引用