from locust import HttpUser, task


class UserBehavior(HttpUser):

    # @task(1)
    # def say_hello(self):
    #     self.client.get("/hello")
    #
    # @task(2)
    # def say_world(self):
    #     self.client.get("/world")
    @task
    def get_token(self):
        header = {'content-type': 'application/json'}
        data = {'grant_type': 'client_credential', 'appid': 'wx74a8627810cfa328', 'secret': 'e40a02f9d79a8097df497e6aaf93ab60'}
        self.client.post(url="/cgi-bin/token", params=data, headers=header)
