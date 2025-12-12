import csv
import io
from typing import List
from models import Employee, Assignment


class CSVHandler:
    """Handles CSV file parsing and generation"""

    @staticmethod
    def parse_employees(csv_content: str) -> List[Employee]:
        try:
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            employees = []
            for row in reader:
                if 'Employee_Name' not in row or 'Employee_EmailID' not in row:
                    raise InvalidEmployeeDataException(
                        "CSV must contain 'Employee_Name' and 'Employee_EmailID' columns"
                    )
                
                employees.append(Employee(
                    name=row['Employee_Name'].strip(),
                    email=row['Employee_EmailID'].strip()
                ))
            
            if not employees:
                raise InvalidEmployeeDataException("CSV file contains no employee data")
            
            return employees
            
        except csv.Error as e:
            raise InvalidEmployeeDataException(f"CSV parsing error: {str(e)}")
        except KeyError as e:
            raise InvalidEmployeeDataException(f"Missing required column: {str(e)}")

    @staticmethod
    def parse_previous_assignments(csv_content: str) -> List[Assignment]:
        try:
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            assignments = []
            for row in reader:
                assignments.append(Assignment(
                    employee_name=row['Employee_Name'].strip(),
                    employee_email=row['Employee_EmailID'].strip(),
                    secret_child_name=row['Secret_Child_Name'].strip(),
                    secret_child_email=row['Secret_Child_EmailID'].strip()
                ))
            
            return assignments
            
        except (csv.Error, KeyError) as e:
            raise InvalidEmployeeDataException(f"Previous assignments parsing error: {str(e)}")

    @staticmethod
    def generate_csv(assignments: List[Assignment]) -> str:
        output = io.StringIO()
        fieldnames = ['Employee_Name', 'Employee_EmailID', 'Secret_Child_Name', 'Secret_Child_EmailID']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        for assignment in assignments:
            writer.writerow({
                'Employee_Name': assignment.employee_name,
                'Employee_EmailID': assignment.employee_email,
                'Secret_Child_Name': assignment.secret_child_name,
                'Secret_Child_EmailID': assignment.secret_child_email
            })
        
        return output.getvalue()
