from fastapi import FastAPI, HTTPException, status
from app.database import get_db_connection, verify_connection
from app.models import Employee, SalaryUpdate
from typing import List
import oracledb

app = FastAPI(title="Employee Management API")

# Verify database connection on startup
@app.on_event("startup")
async def startup_event():
    verify_connection()

# ========== TASK 2: POST /employees - Create Employee ==========
@app.post("/employees", status_code=status.HTTP_201_CREATED)
def create_employee(emp: Employee):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO EMPLOYEES (EMP_ID, EMP_NAME, DEPARTMENT, SALARY, HIRE_DATE)
            VALUES (:1, :2, :3, :4, SYSDATE)
        """, (emp.emp_id, emp.emp_name, emp.department, emp.salary))
        conn.commit()
        return {"message": "Employee created successfully", "employee": emp.dict()}
    except Exception as e:
        conn.rollback()
        raise HTTPException(400, f"Error: {str(e)}")
    finally:
        cursor.close()
        conn.close()

# ========== TASK 3: GET /employees - Get All Employees ==========
@app.get("/employees", response_model=List[dict])
def get_all_employees():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    
    cursor = conn.cursor()
    cursor.execute("SELECT EMP_ID, EMP_NAME, DEPARTMENT, SALARY, TO_CHAR(HIRE_DATE, 'YYYY-MM-DD') FROM EMPLOYEES")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    employees = []
    for row in rows:
        employees.append({
            "emp_id": row[0],
            "emp_name": row[1],
            "department": row[2],
            "salary": row[3],
            "hire_date": row[4]
        })
    return employees

# ========== TASK 4: GET /employees/{emp_id} - Get Employee by ID ==========
@app.get("/employees/{emp_id}")
def get_employee_by_id(emp_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT EMP_ID, EMP_NAME, DEPARTMENT, SALARY, TO_CHAR(HIRE_DATE, 'YYYY-MM-DD') 
        FROM EMPLOYEES WHERE EMP_ID = :1
    """, (emp_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not row:
        raise HTTPException(404, f"Employee with ID {emp_id} not found")
    
    return {
        "emp_id": row[0],
        "emp_name": row[1],
        "department": row[2],
        "salary": row[3],
        "hire_date": row[4]
    }

# ========== TASK 5: PUT /employees/{emp_id} - Update Salary ==========
@app.put("/employees/{emp_id}")
def update_salary(emp_id: int, salary_update: SalaryUpdate):
    # Validate salary
    if salary_update.salary <= 0:
        raise HTTPException(400, "Salary must be greater than 0")
    
    conn = get_db_connection()
    if not conn:
        raise HTTPException(500, "Database connection failed")
    
    cursor = conn.cursor()
    
    # Check if employee exists
    cursor.execute("SELECT EMP_ID FROM EMPLOYEES WHERE EMP_ID = :1", (emp_id,))
    exists = cursor.fetchone()
    
    if not exists:
        cursor.close()
        conn.close()
        raise HTTPException(404, f"Employee with ID {emp_id} not found")
    
    # Update salary
    cursor.execute("UPDATE EMPLOYEES SET SALARY = :1 WHERE EMP_ID = :2", (salary_update.salary, emp_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    return {
        "message": "Salary updated successfully",
        "emp_id": emp_id,
        "new_salary": salary_update.salary
    }

# ========== Keep your existing Product APIs ==========
@app.get("/")
def root():
    return {"message": "Employee Management API", "endpoints": [
        "POST /employees - Create employee",
        "GET /employees - Get all employees",
        "GET /employees/{id} - Get employee by ID",
        "PUT /employees/{id} - Update salary"
    ]}