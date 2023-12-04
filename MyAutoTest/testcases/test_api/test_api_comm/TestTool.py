import pytest

from Utils.LogConfig.LogConfig import logHelper


@pytest.mark.usefixtures("disconn_database")
class TestConn:

    def test_query_open_follow(self, get_conn_database):
        mysql_info = {"host": "192.168.144.240", "port": 15202, "user": "ubsp_customer", "password": "swhy1234",
                      "database": "ubsp_customer"}
        db = get_conn_database(mysql_info)
        res = db.query_data("select * from t_open_follow t where PROCESS_ID = 210527000229;")
        logHelper.info(f"{res}")

    def test_query_(self, get_conn_database):
        mysql_info = {"host": "192.168.130.42", "port": 15018, "user": "demeter_trade", "password": "swhy1234",
                      "database": "demeter_trade"}
        db = get_conn_database(mysql_info)
        res = db.query_data("select * from trade_business_result t where PROCESS_ID = 191023000072;")
        logHelper.info(f"{res}")
