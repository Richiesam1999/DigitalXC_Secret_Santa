from typing import Dict, List, Set, Optional
from models import Assignment


class AssignmentHistory:

    def __init__(self, previous_assignments: List[Assignment] = None):
    
        self._history: Dict[str, str] = {}
        if previous_assignments:
            self._load_history(previous_assignments)

    def _load_history(self, assignments: List[Assignment]):
        """Load previous assignments into history"""
        for assignment in assignments:
            self._history[assignment.employee_email] = assignment.secret_child_email

    def can_assign(self, giver_email: str, receiver_email: str) -> bool:
        return self._history.get(giver_email) != receiver_email

    def get_previous_child(self, giver_email: str) -> Optional[str]:
        """Get previous secret child for a giver"""
        return self._history.get(giver_email)
