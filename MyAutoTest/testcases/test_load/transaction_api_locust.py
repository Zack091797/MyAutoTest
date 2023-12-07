from locust import FastHttpUser, task, SequentialTaskSet


class UserTasks(SequentialTaskSet):

    @task
    def get_login_token(self):
        self.client.post()

    @task
    def handle_transaction(self):
        self.client.post()


class UserUserTasks(FastHttpUser):
    tasks = [UserTasks]
    min_wait = 1000
    max_wait = 2000
