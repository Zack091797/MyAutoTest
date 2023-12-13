import pytest

if __name__ == "__main__":
    # pytest.main(["./testcases/test_api/test_company_api.py"])
    pytest.main(["./testcases/test_ui/OnlineManagement/test_online_management.py", "--envCode", "uat"])