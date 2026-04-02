from locust import HttpUser, task, between
import json
import random

class ComponentUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def create_component(self):
        payload = {
            "name": f"Wing-{random.randint(1000, 9999)}",
            "material": random.choice(["aluminum", "carbon_fiber"]),
            "dimensions": {
                "length": random.uniform(1.0, 10.0),
                "width": random.uniform(0.1, 2.0),
                "height": random.uniform(0.05, 0.5),
                "tolerance": 0.001
            },
            "mass": random.uniform(10.0, 500.0)
        }
        self.client.post("/api/v1/components/", json=payload)

    @task(5)
    def get_component(self):
        # Assume we have some IDs, in real test we'd fetch first
        self.client.get("/api/v1/components/")

    @task(2)
    def heavy_query(self):
        # Simulate a complex query
        self.client.get("/api/v1/components/?skip=0&limit=100")
