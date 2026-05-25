import unittest
import json
from app import create_app

TEST_CONFIG = {
    "TESTING": True,
    "DATABASE": ":memory:",
}

VALID_EMPLOYEE = {
    "full_name": "Alice Smith",
    "job_title": "Engineer",
    "country": "India",
    "salary": 75000.00,
    "doj": "2022-03-15",
    "dob": "1990-07-20",
}


class EmployeeCreateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_create_employee_returns_201(self):
        response = self.client.post(
            "/employees",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)

    def test_create_employee_returns_empid(self):
        response = self.client.post(
            "/employees",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        data = json.loads(response.data)
        self.assertIn("empid", data)
        self.assertIsInstance(data["empid"], int)

    def test_create_employee_missing_field_returns_400(self):
        incomplete = {k: v for k, v in VALID_EMPLOYEE.items() if k != "salary"}
        response = self.client.post(
            "/employees",
            data=json.dumps(incomplete),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_create_employee_non_json_returns_415(self):
        response = self.client.post(
            "/employees",
            data="not json",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 415)


class EmployeeListTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_list_employees_empty_returns_200_and_empty_list(self):
        response = self.client.get("/employees")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_list_employees_after_create_returns_one_record(self):
        self.client.post(
            "/employees",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        response = self.client.get("/employees")
        data = json.loads(response.data)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["full_name"], VALID_EMPLOYEE["full_name"])
        self.assertIn("empid", data[0])


class EmployeeGetOneTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()
        resp = self.client.post(
            "/employees",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        self.empid = json.loads(resp.data)["empid"]

    def test_get_existing_employee_returns_200(self):
        response = self.client.get(f"/employees/{self.empid}")
        self.assertEqual(response.status_code, 200)

    def test_get_existing_employee_returns_correct_data(self):
        response = self.client.get(f"/employees/{self.empid}")
        data = json.loads(response.data)
        self.assertEqual(data["full_name"], VALID_EMPLOYEE["full_name"])
        self.assertEqual(data["job_title"], VALID_EMPLOYEE["job_title"])
        self.assertEqual(data["country"], VALID_EMPLOYEE["country"])
        self.assertEqual(float(data["salary"]), VALID_EMPLOYEE["salary"])
        self.assertEqual(data["doj"], VALID_EMPLOYEE["doj"])
        self.assertEqual(data["dob"], VALID_EMPLOYEE["dob"])

    def test_get_nonexistent_employee_returns_404(self):
        response = self.client.get("/employees/99999")
        self.assertEqual(response.status_code, 404)


class EmployeeUpdateTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()
        resp = self.client.post(
            "/employees",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        self.empid = json.loads(resp.data)["empid"]

    def test_update_employee_returns_200(self):
        update_payload = {**VALID_EMPLOYEE, "salary": 90000.00}
        response = self.client.put(
            f"/employees/{self.empid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_employee_persists_change(self):
        update_payload = {**VALID_EMPLOYEE, "job_title": "Senior Engineer"}
        self.client.put(
            f"/employees/{self.empid}",
            data=json.dumps(update_payload),
            content_type="application/json",
        )
        response = self.client.get(f"/employees/{self.empid}")
        data = json.loads(response.data)
        self.assertEqual(data["job_title"], "Senior Engineer")

    def test_update_nonexistent_employee_returns_404(self):
        response = self.client.put(
            "/employees/99999",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_update_missing_field_returns_400(self):
        incomplete = {k: v for k, v in VALID_EMPLOYEE.items() if k != "full_name"}
        response = self.client.put(
            f"/employees/{self.empid}",
            data=json.dumps(incomplete),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)


class EmployeeDeleteTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()
        resp = self.client.post(
            "/employees",
            data=json.dumps(VALID_EMPLOYEE),
            content_type="application/json",
        )
        self.empid = json.loads(resp.data)["empid"]

    def test_delete_employee_returns_200(self):
        response = self.client.delete(f"/employees/{self.empid}")
        self.assertEqual(response.status_code, 200)

    def test_delete_employee_removes_record(self):
        self.client.delete(f"/employees/{self.empid}")
        response = self.client.get(f"/employees/{self.empid}")
        self.assertEqual(response.status_code, 404)

    def test_delete_nonexistent_employee_returns_404(self):
        response = self.client.delete("/employees/99999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
