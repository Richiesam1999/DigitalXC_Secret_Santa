from models import Employee
from assignment_history import AssignmentHistory


class AssignmentValidator:
    """Validates Secret Santa assignment rules"""

    @staticmethod
    def validate(giver: Employee, receiver: Employee, history: AssignmentHistory) -> tuple[bool, str]:

        # Rule 1: Cannot assign to self
        if giver.email == receiver.email:
            return False, f"{giver.name} cannot be assigned to themselves"
        
        if giver.name == receiver.name:
            return False, f"Cannot assign {giver.name} ({giver.email}) to {receiver.name} ({receiver.email}) - same name"
        
        # Rule 2: Cannot have same assignment as previous year
        if not history.can_assign(giver.email, receiver.email):
            return False, f"{giver.name} had {receiver.name} as their secret child last year"
        
        return True, ""
