from typing import List, Dict, Optional
from models import Employee


class EmployeeRepository:
    """Repo for managing employee data"""

    def __init__(self, employees: List[Employee]):
        """
            InsufficientEmployeesException: If less than 2 employees
            DuplicateEmailException: If duplicate emails found
        """
        self.employees = employees
        self._validate_employees()
        self._email_to_employee: Dict[str, Employee] = {
            emp.email: emp for emp in employees
        }

    def _validate_employees(self):
        """Validate employee data"""
        if len(self.employees) < 2:
            raise InsufficientEmployeesException(
                "At least 2 employees are required for Secret Santa"
            )
        
        # Check for duplicate emails
        emails = [emp.email for emp in self.employees]
        if len(emails) != len(set(emails)):
            duplicates = [email for email in emails if emails.count(email) > 1]
            raise DuplicateEmailException(
                f"Duplicate email(s) found: {', '.join(set(duplicates))}"
            )

    def get_all_employees(self) -> List[Employee]:
        """Get all employees"""
        return self.employees.copy()

    def find_by_email(self, email: str) -> Optional[Employee]:
        """Find employee by email"""
        return self._email_to_employee.get(email)

    def get_employee_count(self) -> int:
        """Get total number of employees"""
        return len(self.employees)
