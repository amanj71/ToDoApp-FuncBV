import random
from faker import Faker
from locust import HttpUser, TaskSet, task, between, constant_pacing
# from Accounts.models import MyUser, Profile
# from Tasks.models import Task, Category

fake = Faker()
# --------------------------------------------------
# CONFIG
# --------------------------------------------------

REGULAR_USERS = [
    {"email": "ncarson@example.net", "password": "123"},
    {"email": "carterjames@example.org", "password": "123"},
    {"email": "komo@jomo.com", "password": "Zxc123456!"},
]

ADMIN_USERS = [
    {"email": "am@am.com", "password": "123"},
]

# --------------------------------------------------
# BASE USER (JWT LOGIN)
# --------------------------------------------------

class JWTUser(HttpUser):
    abstract = True

    def login(self, payload):
        with self.client.post("/accounts/api/v0/api-jwt-login/",json=payload,
                              catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure("Login failed")
                return False

            token = resp.json().get("access")
            if not token:
                resp.failure("No JWT token returned")
                return False

            self.client.headers.update({
                "Authorization": f"Bearer {token}"
            })
            return True

# --------------------------------------------------
# REGULAR USER
# --------------------------------------------------

class RegularUser(JWTUser):
    wait_time = between(0.5, 2)
    weight = 3

    def on_start(self):
        creds = random.choice(REGULAR_USERS)
        if not self.login(creds):
            self.environment.runner.quit()

        self.task_ids = []
        self.load_task_ids()

    def load_task_ids(self):
        with self.client.get("/tasks/api/v0/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure("Failed to load task list")
                return

            self.task_ids = [t["id"] for t in resp.json()]

    @task(3)
    def list_tasks(self):
        self.client.get("/tasks/api/v0/")

    @task(1)
    def view_task_detail(self):
        if not self.task_ids:
            return

        task_id = random.choice(self.task_ids)
        self.client.get(f"/tasks/api/v0/{task_id}/")

# --------------------------------------------------
# ADMIN USER
# --------------------------------------------------

class AdminUser(JWTUser):
    wait_time = constant_pacing(2)
    weight = 1

    def on_start(self):
        creds = random.choice(ADMIN_USERS)
        if not self.login(creds):
            self.environment.runner.quit()

        self.category_ids = []
        self.load_categories()

    def load_categories(self):
        with self.client.get("/tasks/api/v0/categories/", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure("Failed to load categories")
                return

            self.category_ids = [c["id"] for c in resp.json()]

    @task
    def create_task(self):
        if not self.category_ids:
            return

        payload = {
            "title": fake.sentence(nb_words=4),
            "status": random.choice(["F", "P", "C"]),
            "category": random.choice(self.category_ids),
            "importance": random.choice(["H", "M", "L"])
        }

        with self.client.post(
            "/tasks/api/v0/",
            json=payload,
            catch_response=True
        ) as resp:
            if resp.status_code not in (200, 201):
                resp.failure("Task creation failed")