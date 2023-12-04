import os

from locust import HttpUser, task


class UserBehavior(HttpUser):

    # @task
    # def get_token(self):
    #     header = {'content-type': 'application/json'}
    #     data = {'grant_type': 'client_credential', 'appid': 'wx74a8627810cfa328', 'secret': 'e40a02f9d79a8097df497e6aaf93ab60'}
    #     self.client.post(url="/cgi-bin/token", params=data, headers=header)

    @task
    def layout_get_customer_businessList(self):
        header = {'Content-Type': "application/json"}
        data = {
            "fundAcct": "1633000091",
            "beginDate": "2023-06-17",
            "endDate": "2023-06-17",
            "idNum": "",
            "mobile": ""
        }
        self.client.get(url="/layout/v1/unify/business/handle/list", params=data, headers=header)


if __name__ == "__main__":
    os.system("locust -f load_locust.py --host=http://192.168.27.43:98  -u=10 -r=3 -t=60s")

    # os.chdir("C:\\Users\\Zhou\\apache-jmeter-5.6.2\\apache-jmeter-5.6.2\\bin")
    # print(os.getcwd())
    # os.system(r"jmeter -n -t C:\Users\EDY\Desktop\layout.jmx -l C:\Users\Zhou\apache-jmeter-5.6.2\results.html -e -o C:\Users\Zhou\apache-jmeter-5.6.2\result")
