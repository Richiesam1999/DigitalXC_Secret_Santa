from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from typing import Optional

from models import AssignmentRequest, AssignmentResponse, Employee, Assignment
from secret_santa_service import SecretSantaService
from csv_handler import CSVHandler
from exceptions import (
    SecretSantaException,
    InvalidEmployeeDataException,
    InsufficientEmployeesException,
    AssignmentFailedException,
    DuplicateEmailException
)

app = FastAPI(
    title="Secret Santa API",
    description="API for generating Secret Santa assignments",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = SecretSantaService()


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Secret Santa API",
        "version": "1.0.0",
        "endpoints": {
            "POST /assign": "Generate assignments from JSON",
            "POST /assign/csv": "Generate assignments from CSV files",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/assign", response_model=AssignmentResponse)
async def create_assignments(request: AssignmentRequest):
    try:
        assignments = service.generate_assignments(
            employees=request.current_employees,
            previous_assignments=request.previous_assignments
        )
        
        return AssignmentResponse(
            success=True,
            message="Assignments generated successfully",
            assignments=assignments,
            total_assignments=len(assignments)
        )
        
    except InsufficientEmployeesException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateEmailException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AssignmentFailedException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except SecretSantaException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/assign/csv")
async def create_assignments_from_csv(
    employees_file: UploadFile = File(...),
    previous_assignments_file: Optional[UploadFile] = File(None)
):
    try:
        # Read and parse employees CSV
        employees_content = await employees_file.read()
        employees_str = employees_content.decode('utf-8')
        employees = CSVHandler.parse_employees(employees_str)
        
        # Read and parse previous assignments if provided
        previous_assignments = None
        if previous_assignments_file:
            prev_content = await previous_assignments_file.read()
            prev_str = prev_content.decode('utf-8')
            previous_assignments = CSVHandler.parse_previous_assignments(prev_str)
        
        # Generate assignments
        assignments = service.generate_assignments(employees, previous_assignments)
        
        # Generate CSV output
        csv_output = CSVHandler.generate_csv(assignments)
        
        # Return as downloadable file
        return StreamingResponse(
            io.StringIO(csv_output),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=secret_santa_assignments.csv"}
        )
        
    except InvalidEmployeeDataException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InsufficientEmployeesException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DuplicateEmailException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except AssignmentFailedException as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
