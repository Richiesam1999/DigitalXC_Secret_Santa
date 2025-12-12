from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional


class Employee(BaseModel):
    """Employee model representing an employee"""
    name: str
    email: EmailStr

    @validator('name')
    def name_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Employee name cannot be empty')
        return v.strip()


class Assignment(BaseModel):
    """Assignment model representing a Secret Santa assignment"""
    employee_name: str
    employee_email: EmailStr
    secret_child_name: str
    secret_child_email: EmailStr


class AssignmentRequest(BaseModel):
    """Request model for creating Secret Santa assignments"""
    current_employees: List[Employee]
    previous_assignments: Optional[List[Assignment]] = None


class AssignmentResponse(BaseModel):
    """Response model for Secret Santa assignments"""
    success: bool
    message: str
    assignments: Optional[List[Assignment]] = None
    total_assignments: Optional[int] = None
