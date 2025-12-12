import random
from typing import List
from models import Employee, Assignment
from employee_repository import EmployeeRepository
from assignment_history import AssignmentHistory
from assignment_validator import AssignmentValidator


class SecretSantaAssigner:
    """Core logic for assigning Secret Santa pairs"""

    def __init__(self, repository: EmployeeRepository, history: AssignmentHistory):
        self.repository = repository
        self.history = history
        self.validator = AssignmentValidator()
        self.max_attempts = 1000

    def assign(self) -> List[Assignment]:
        for attempt in range(self.max_attempts):
            try:
                assignments = self._attempt_assignment()
                if self._validate_all_assignments(assignments):
                    return assignments
            except Exception:
                continue
        
        raise AssignmentFailedException(
            f"Could not generate valid assignments after {self.max_attempts} attempts. "
            "This may happen if constraints are too restrictive."
        )

    def _attempt_assignment(self) -> List[Assignment]:
        employees = self.repository.get_all_employees()
        givers = employees.copy()
        receivers = employees.copy()
        
        # Shuffle receivers for randomization
        random.shuffle(receivers)
        
        assignments = []
        for giver, receiver in zip(givers, receivers):
            is_valid, error_msg = self.validator.validate(giver, receiver, self.history)
            if not is_valid:
                raise ValueError(error_msg)
            
            assignments.append(Assignment(
                employee_name=giver.name,
                employee_email=giver.email,
                secret_child_name=receiver.name,
                secret_child_email=receiver.email
            ))
        
        return assignments

    def _validate_all_assignments(self, assignments: List[Assignment]) -> bool:

        # Check each person is assigned exactly once as receiver
        receivers = set()
        for assignment in assignments:
            if assignment.secret_child_email in receivers:
                return False
            receivers.add(assignment.secret_child_email)
        
        # Check we have the right number of assignments
        return len(receivers) == self.repository.get_employee_count()
