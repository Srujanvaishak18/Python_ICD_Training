from pydantic import BaseModel
from datetime import date
from typing import Optional

class Employee(BaseModel):
    emp_id: int
    emp_name: str
    department: str
    salary: float
    hire_date: Optional[date] = None

class SalaryUpdate(BaseModel):
    salary: float