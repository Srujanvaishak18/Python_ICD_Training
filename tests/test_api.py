import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_root():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("✅ Root endpoint test passed")

def test_create_employee():
    data = {
        "emp_id": 101,
        "emp_name": "John",
        "department": "IT",
        "salary": 50000
    }
    response = requests.post(f"{BASE_URL}/employees", json=data)
    assert response.status_code == 201
    print("✅ Create employee test passed")

def test_get_all_employees():
    response = requests.get(f"{BASE_URL}/employees")
    assert response.status_code == 200
    print("✅ Get all employees test passed")

def test_get_employee_by_id():
    response = requests.get(f"{BASE_URL}/employees/101")
    assert response.status_code == 200
    print("✅ Get employee by ID test passed")

def test_update_salary():
    data = {"salary": 60000}
    response = requests.put(f"{BASE_URL}/employees/101", json=data)
    assert response.status_code == 200
    print("✅ Update salary test passed")

if __name__ == "__main__":
    test_root()
    test_create_employee()
    test_get_all_employees()
    test_get_employee_by_id()
    test_update_salary()
    print("\n🎉 All tests passed!")