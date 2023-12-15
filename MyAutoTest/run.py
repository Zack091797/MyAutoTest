import os
from time import sleep

import pytest

if __name__ == "__main__":
    # pytest.main(["./testcases/test_api/test_company_api.py"])
    # pytest.main(["./testcases/test_ui/OnlineManagement/test_online_management.py", "--envCode", "uat"])
    # pytest.main(["./testcases/test_ui/test_ui_demo.py", "--envCode", "dev"])
    pytest.main(["./testcases/test_api/test_swhy_message.py"])
    # sleep(3)
    # os.system("allure generate ./allure_result -o ./allure_reports --clean")