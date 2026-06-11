from pydantic import BaseModel
from datetime import date
from typing import Optional

# Employee model for Task 2
class Employee(BaseModel):
    emp_id: int
    emp_name: str
    department: str
    salary: float
    hire_date: Optional[date] = None

# Salary update model for Task 5
class SalaryUpdate(BaseModel):
    salary: float

# Product model (existing)
class Product(BaseModel):
    id: int
    name: str
    price: float