import pytest
from pydantic import ValidationError
from models import Employee, Assignment


class TestEmployee:
    """Test cases for Employee model"""

    def test_valid_employee_creation(self):
        """Test creating a valid employee"""
        employee = Employee(name="John Doe", email="john@acme.com")
        assert employee.name == "John Doe"
        assert employee.email == "john@acme.com"

    def test_employee_name_whitespace_stripped(self):
        """Test that employee names have whitespace stripped"""
        employee = Employee(name="  John Doe  ", email="john@acme.com")
        assert employee.name == "John Doe"

    def test_invalid_email_format(self):
        """Test that invalid email raises validation error"""
        with pytest.raises(ValidationError):
            Employee(name="John Doe", email="not-an-email")

    def test_empty_name_rejected(self):
        """Test that empty name is rejected"""
        with pytest.raises(ValidationError):
            Employee(name="", email="john@acme.com")

    def test_whitespace_only_name_rejected(self):
        """Test that whitespace-only name is rejected"""
        with pytest.raises(ValidationError):
            Employee(name="   ", email="john@acme.com")

    def test_missing_fields(self):
        """Test that missing fields raise validation error"""
        with pytest.raises(ValidationError):
            Employee(name="John Doe")
        
        with pytest.raises(ValidationError):
            Employee(email="john@acme.com")


class TestAssignment:
    """Test cases for Assignment model"""

    def test_valid_assignment_creation(self):
        """Test creating a valid assignment"""
        assignment = Assignment(
            employee_name="John Doe",
            employee_email="john@acme.com",
            secret_child_name="Jane Smith",
            secret_child_email="jane@acme.com"
        )
        assert assignment.employee_name == "John Doe"
        assert assignment.employee_email == "john@acme.com"
        assert assignment.secret_child_name == "Jane Smith"
        assert assignment.secret_child_email == "jane@acme.com"

    def test_invalid_email_in_assignment(self):
        """Test that invalid emails raise validation error"""
        with pytest.raises(ValidationError):
            Assignment(
                employee_name="John Doe",
                employee_email="invalid-email",
                secret_child_name="Jane Smith",
                secret_child_email="jane@acme.com"
            )