import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAPIEndpoints:
    """Test cases for API endpoints"""

    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_check(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_assign_with_valid_json(self):
        """Test assignment endpoint with valid JSON"""
        data = {
            "current_employees": [
                {"name": "Alice", "email": "alice@acme.com"},
                {"name": "Bob", "email": "bob@acme.com"},
                {"name": "Charlie", "email": "charlie@acme.com"}
            ]
        }
        response = client.post("/assign", json=data)
        assert response.status_code == 200
        result = response.json()
        assert result["success"] is True
        assert len(result["assignments"]) == 3

    def test_assign_with_previous_assignments(self):
        """Test assignment with previous year data"""
        data = {
            "current_employees": [
                {"name": "Alice", "email": "alice@acme.com"},
                {"name": "Bob", "email": "bob@acme.com"},
                {"name": "Charlie", "email": "charlie@acme.com"}
            ],
            "previous_assignments": [
                {
                    "employee_name": "Alice",
                    "employee_email": "alice@acme.com",
                    "secret_child_name": "Bob",
                    "secret_child_email": "bob@acme.com"
                }
            ]
        }
        response = client.post("/assign", json=data)
        assert response.status_code == 200
        result = response.json()
        
        # Verify Alice is not assigned to Bob
        alice_assignment = next(
            a for a in result["assignments"]
            if a["employee_email"] == "alice@acme.com"
        )
        assert alice_assignment["secret_child_email"] != "bob@acme.com"

    def test_assign_insufficient_employees(self):
        """Test error with insufficient employees"""
        data = {
            "current_employees": [
                {"name": "Alice", "email": "alice@acme.com"}
            ]
        }
        response = client.post("/assign", json=data)
        assert response.status_code == 400

    def test_assign_duplicate_emails(self):
        """Test error with duplicate emails"""
        data = {
            "current_employees": [
                {"name": "Alice", "email": "alice@acme.com"},
                {"name": "Bob", "email": "alice@acme.com"}
            ]
        }
        response = client.post("/assign", json=data)
        assert response.status_code == 400

    def test_assign_invalid_email(self):
        """Test error with invalid email"""
        data = {
            "current_employees": [
                {"name": "Alice", "email": "not-an-email"},
                {"name": "Bob", "email": "bob@acme.com"}
            ]
        }
        response = client.post("/assign", json=data)
        assert response.status_code == 422  # Validation error

    def test_csv_upload_endpoint(self, sample_csv_employees):
        """Test CSV upload endpoint"""
        files = {
            'employees_file': ('employees.csv', sample_csv_employees, 'text/csv')
        }
        response = client.post("/assign/csv", files=files)
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
