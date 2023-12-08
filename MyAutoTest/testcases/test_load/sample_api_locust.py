import os

from locust import FastHttpUser, task, TaskSet


class UserBehavior(FastHttpUser):

    @task
    def layout_get_customer_businessList(self):
        header = {'Content-Type': "application/json"}
        data = {
            "fundAcct": "1653066308",
            "beginDate": "2019-06-27",
            "endDate": "2019-06-27",
            "idNum": "",
            "mobile": ""
        }
        self.client.get(url="/layout/v1/unify/business/handle/list", params=data, headers=header)


# class UserTasks(TaskSet):
#
#     @task
#     def layout_get_customer_businessList(self):
#         url = "/layout/v1/unify/business/handle/list"
#         header = {'Content-Type': "application/json"}
#         data = {
#             "fundAcct": "1653066308",
#             "beginDate": "2019-06-27",
#             "endDate": "2019-06-27",
#             "idNum": "",
#             "mobile": ""
#         }
#         self.client.get(url=url, params=data, header=header)
#
#
# class WebUser(FastHttpUser):
#     tasks = [UserTasks]
#     min_wait = 0
#     max_wait = 1000


if __name__ == "__main__":
    os.system("locust -f sample_api_locust.py --host=http://192.168.145.21:8007  -u=50 -r=50 -t=180s")
