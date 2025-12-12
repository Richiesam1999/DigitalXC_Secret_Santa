from typing import List
from models import Employee, Assignment
from employee_repository import EmployeeRepository
from assignment_history import AssignmentHistory
from secret_santa_assigner import SecretSantaAssigner


class SecretSantaService:
    """Service layer for ops"""

    def generate_assignments(
        self,
        employees: List[Employee],
        previous_assignments: List[Assignment] = None
    ) -> List[Assignment]:
        # Create repository and validate employees
        repository = EmployeeRepository(employees)
        
        # Load assignment history
        history = AssignmentHistory(previous_assignments)
        
        # Generate assignments
        assigner = SecretSantaAssigner(repository, history)
        assignments = assigner.assign()
        
        return assignments