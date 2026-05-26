import unittest
import json
from io import BytesIO
from werkzeug.datastructures import FileStorage
from app import create_app

TEST_CONFIG = {
    "TESTING": True,
    "DATABASE": ":memory:",
}

VALID_FIRST_NAMES = "Alice\nBob\nCharlie"
VALID_LAST_NAMES = "Smith\nJohnson\nWilson"
VALID_CSV = """job_title,country,salary,doj,dob
Engineer,India,75000.00,2022-03-15,1990-07-20
Manager,USA,95000.00,2021-01-10,1988-05-12
Designer,UK,65000.00,2023-06-01,1995-02-14"""


def create_import_request(first_names=None, last_names=None, employee_data=None):
    """Helper to create multipart form data dict using FileStorage"""
    files = {}
    if first_names is not None:
        files['first_names'] = FileStorage(
            stream=BytesIO(first_names.encode('utf-8')),
            filename='first_names.txt',
            content_type='text/plain'
        )
    if last_names is not None:
        files['last_names'] = FileStorage(
            stream=BytesIO(last_names.encode('utf-8')),
            filename='last_names.txt',
            content_type='text/plain'
        )
    if employee_data is not None:
        files['employee_data'] = FileStorage(
            stream=BytesIO(employee_data.encode('utf-8')),
            filename='employee_data.csv',
            content_type='text/csv'
        )
    return files


class TestEmployeeImportValidation(unittest.TestCase):
    """Test file presence validation"""

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_import_missing_first_names_returns_400(self):
        files = create_import_request(
            first_names=None,
            last_names=VALID_LAST_NAMES,
            employee_data=VALID_CSV
        )
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("first_names.txt", data["error"])

    def test_import_missing_last_names_returns_400(self):
        files = create_import_request(
            first_names=VALID_FIRST_NAMES,
            last_names=None,
            employee_data=VALID_CSV
        )
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("last_names.txt", data["error"])

    def test_import_missing_employee_data_returns_400(self):
        files = create_import_request(
            first_names=VALID_FIRST_NAMES,
            last_names=VALID_LAST_NAMES,
            employee_data=None
        )
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("employee_data.csv", data["error"])

    def test_import_lists_all_missing_files_in_error(self):
        files = create_import_request(
            first_names=None,
            last_names=None,
            employee_data=None
        )
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("first_names.txt", data["error"])
        self.assertIn("last_names.txt", data["error"])
        self.assertIn("employee_data.csv", data["error"])


class TestEmployeeImportLineCountMismatch(unittest.TestCase):
    """Test line count validation"""

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_import_first_names_count_mismatch_returns_400(self):
        first_names = "Alice\nBob"  # 2 names
        last_names = VALID_LAST_NAMES  # 3 names
        csv_data = VALID_CSV  # 3 records

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Line count mismatch", data["error"])

    def test_import_last_names_count_mismatch_returns_400(self):
        first_names = VALID_FIRST_NAMES  # 3 names
        last_names = "Smith\nJohnson"  # 2 names
        csv_data = VALID_CSV  # 3 records

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Line count mismatch", data["error"])

    def test_import_csv_row_count_mismatch_returns_400(self):
        first_names = VALID_FIRST_NAMES  # 3 names
        last_names = VALID_LAST_NAMES  # 3 names
        csv_data = """job_title,country,salary,doj,dob
Engineer,India,75000.00,2022-03-15,1990-07-20
Manager,USA,95000.00,2021-01-10,1988-05-12"""  # 2 records

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("Line count mismatch", data["error"])


class TestEmployeeImportCSVValidation(unittest.TestCase):
    """Test CSV column validation"""

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_import_invalid_csv_missing_job_title_returns_400(self):
        csv_data = """country,salary,doj,dob
India,75000.00,2022-03-15,1990-07-20
USA,95000.00,2021-01-10,1988-05-12
UK,65000.00,2023-06-01,1995-02-14"""

        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("job_title", data["error"])

    def test_import_invalid_csv_missing_country_returns_400(self):
        csv_data = """job_title,salary,doj,dob
Engineer,75000.00,2022-03-15,1990-07-20
Manager,95000.00,2021-01-10,1988-05-12
Designer,65000.00,2023-06-01,1995-02-14"""

        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("country", data["error"])

    def test_import_invalid_csv_missing_salary_returns_400(self):
        csv_data = """job_title,country,doj,dob
Engineer,India,2022-03-15,1990-07-20
Manager,USA,2021-01-10,1988-05-12
Designer,UK,2023-06-01,1995-02-14"""

        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("salary", data["error"])

    def test_import_invalid_csv_missing_doj_returns_400(self):
        csv_data = """job_title,country,salary,dob
Engineer,India,75000.00,1990-07-20
Manager,USA,95000.00,1988-05-12
Designer,UK,65000.00,1995-02-14"""

        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("doj", data["error"])

    def test_import_invalid_csv_missing_dob_returns_400(self):
        csv_data = """job_title,country,salary,doj
Engineer,India,75000.00,2022-03-15
Manager,USA,95000.00,2021-01-10
Designer,UK,65000.00,2023-06-01"""

        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("dob", data["error"])


class TestEmployeeImportSuccess(unittest.TestCase):
    """Test successful imports"""

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_import_three_files_correct_returns_201(self):
        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, VALID_CSV)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

    def test_import_returns_count_of_imported_records(self):
        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, VALID_CSV)
        response = self.client.post("/employees/import", data=files)
        data = json.loads(response.data)
        self.assertIn("imported", data)
        self.assertEqual(data["imported"], 3)

    def test_import_inserts_combined_full_name_correctly(self):
        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, VALID_CSV)
        self.client.post("/employees/import", data=files)

        response = self.client.get("/employees")
        employees = json.loads(response.data)

        self.assertEqual(employees[0]["full_name"], "Alice Smith")
        self.assertEqual(employees[1]["full_name"], "Bob Johnson")
        self.assertEqual(employees[2]["full_name"], "Charlie Wilson")

    def test_import_inserts_all_csv_data_correctly(self):
        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, VALID_CSV)
        self.client.post("/employees/import", data=files)

        response = self.client.get("/employees")
        employees = json.loads(response.data)

        self.assertEqual(employees[0]["job_title"], "Engineer")
        self.assertEqual(employees[0]["country"], "India")
        self.assertEqual(float(employees[0]["salary"]), 75000.00)
        self.assertEqual(employees[0]["doj"], "2022-03-15")
        self.assertEqual(employees[0]["dob"], "1990-07-20")

    def test_import_uses_correct_row_order_by_index(self):
        files = create_import_request(VALID_FIRST_NAMES, VALID_LAST_NAMES, VALID_CSV)
        self.client.post("/employees/import", data=files)

        response = self.client.get("/employees")
        employees = json.loads(response.data)

        # Verify order is preserved (by index matching)
        self.assertEqual(employees[0]["full_name"], "Alice Smith")
        self.assertEqual(employees[0]["country"], "India")

        self.assertEqual(employees[1]["full_name"], "Bob Johnson")
        self.assertEqual(employees[1]["country"], "USA")

        self.assertEqual(employees[2]["full_name"], "Charlie Wilson")
        self.assertEqual(employees[2]["country"], "UK")

    def test_import_large_file_10000_records_returns_201(self):
        """Stress test: 10,000 records with batching"""
        first_names = "\n".join([f"First{i}" for i in range(10000)])
        last_names = "\n".join([f"Last{i}" for i in range(10000)])

        csv_lines = ["job_title,country,salary,doj,dob"]
        for i in range(10000):
            csv_lines.append(f"Engineer,India,{75000.00 + i},2022-03-15,1990-07-20")
        csv_data = "\n".join(csv_lines)

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertEqual(data["imported"], 10000)


class TestEmployeeImportEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios"""

    def setUp(self):
        self.app = create_app(TEST_CONFIG)
        self.client = self.app.test_client()

    def test_import_empty_files_returns_400(self):
        files = create_import_request("", "", "job_title,country,salary,doj,dob")
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn("empty", data["error"].lower())

    def test_import_single_employee_returns_201_count_1(self):
        first_names = "John"
        last_names = "Doe"
        csv_data = """job_title,country,salary,doj,dob
Developer,Canada,80000.00,2023-01-15,1992-03-10"""

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertEqual(data["imported"], 1)

    def test_import_whitespace_in_names_preserved(self):
        first_names = "  Alice  \n  Bob  "
        last_names = "  Smith  \n  Johnson  "
        csv_data = """job_title,country,salary,doj,dob
Engineer,India,75000.00,2022-03-15,1990-07-20
Manager,USA,95000.00,2021-01-10,1988-05-12"""

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/employees")
        employees = json.loads(response.data)
        # Names should be stripped (leading/trailing whitespace removed)
        self.assertEqual(employees[0]["full_name"], "Alice Smith")
        self.assertEqual(employees[1]["full_name"], "Bob Johnson")

    def test_import_special_characters_in_data_preserved(self):
        first_names = "José\nMarie-Jeanne"
        last_names = "García\nD'Arcy"
        csv_data = """job_title,country,salary,doj,dob
Engineer,España,75000.00,2022-03-15,1990-07-20
Manager,France,95000.00,2021-01-10,1988-05-12"""

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

        response = self.client.get("/employees")
        employees = json.loads(response.data)
        self.assertEqual(employees[0]["full_name"], "José García")
        self.assertEqual(employees[1]["full_name"], "Marie-Jeanne D'Arcy")

    def test_import_csv_with_extra_columns_ignored(self):
        csv_data = """job_title,country,salary,doj,dob,extra_column,another_extra
Engineer,India,75000.00,2022-03-15,1990-07-20,ignored1,ignored2
Manager,USA,95000.00,2021-01-10,1988-05-12,ignored3,ignored4
Designer,UK,65000.00,2023-06-01,1995-02-14,ignored5,ignored6"""

        first_names = "Alice\nBob\nCharlie"
        last_names = "Smith\nJohnson\nWilson"

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertEqual(data["imported"], 3)

    def test_import_batch_boundary_at_1000_records(self):
        """Verify batching logic works at exactly 1000-record boundary"""
        first_names = "\n".join([f"First{i}" for i in range(1000)])
        last_names = "\n".join([f"Last{i}" for i in range(1000)])

        csv_lines = ["job_title,country,salary,doj,dob"]
        for i in range(1000):
            csv_lines.append(f"Engineer,India,{75000.00 + i},2022-03-15,1990-07-20")
        csv_data = "\n".join(csv_lines)

        files = create_import_request(first_names, last_names, csv_data)
        response = self.client.post("/employees/import", data=files)
        self.assertEqual(response.status_code, 201)

        data = json.loads(response.data)
        self.assertEqual(data["imported"], 1000)


if __name__ == "__main__":
    unittest.main()
