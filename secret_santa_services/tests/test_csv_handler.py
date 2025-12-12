import pytest
from csv_handler import CSVHandler
from models import Employee, Assignment
from exceptions import InvalidEmployeeDataException


class TestCSVHandler:
    """Test cases for CSVHandler"""

    def test_parse_valid_employees_csv(self, sample_csv_employees):
        """Test parsing valid employee CSV"""
        employees = CSVHandler.parse_employees(sample_csv_employees)
        assert len(employees) == 3
        assert employees[0].name == "Alice Smith"
        assert employees[0].email == "alice@acme.com"

    def test_parse_employees_with_tab_delimiter(self):
        """Test parsing CSV with tab delimiter"""
        csv_content = "Employee_Name\tEmployee_EmailID\nJohn Doe\tjohn@acme.com"
        employees = CSVHandler.parse_employees(csv_content)
        assert len(employees) == 1
        assert employees[0].name == "John Doe"

    def test_parse_empty_csv_raises_error(self):
        """Test that empty CSV raises error"""
        with pytest.raises(InvalidEmployeeDataException):
            CSVHandler.parse_employees("Employee_Name,Employee_EmailID\n")

    def test_parse_csv_missing_columns(self):
        """Test that CSV missing required columns raises error"""
        csv_content = "Name,Email\nJohn Doe,john@acme.com"
        with pytest.raises(InvalidEmployeeDataException):
            CSVHandler.parse_employees(csv_content)

    def test_parse_previous_assignments(self, sample_csv_assignments):
        """Test parsing previous assignments CSV"""
        assignments = CSVHandler.parse_previous_assignments(sample_csv_assignments)
        assert len(assignments) == 2
        assert assignments[0].employee_name == "Alice Smith"
        assert assignments[0].secret_child_name == "Bob Jones"

    def test_generate_csv_from_assignments(self, sample_assignments):
        """Test generating CSV from assignments"""
        csv_content = CSVHandler.generate_csv(sample_assignments)
        lines = csv_content.strip().split('\n')
        
        assert len(lines) == 3  # Header + 2 data rows
        assert "Employee_Name" in lines[0]
        assert "Alice Smith" in lines[1]
        assert "Bob Jones" in lines[2]

    def test_csv_roundtrip(self, sample_csv_assignments):
        """Test that parsing and generating CSV maintains data integrity"""
        assignments = CSVHandler.parse_previous_assignments(sample_csv_assignments)
        regenerated_csv = CSVHandler.generate_csv(assignments)
        re_parsed = CSVHandler.parse_previous_assignments(regenerated_csv)
        
        assert len(assignments) == len(re_parsed)
        assert assignments[0].employee_name == re_parsed[0].employee_name
