import pyodbc
from faker import Faker
import random

# Database connection
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"  
    "Database=NorthWind_1;"                   # Replace with your database name
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Initialize Faker
fake = Faker()

def populate_employees(n):
    employee_ids = []
    for _ in range(n):
        employee_id = random.randint(1, 1000)  
        last_name = fake.last_name()
        first_name = fake.first_name()
        title = fake.job()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=65)  
        hire_date = fake.date_this_decade() 
        address = fake.address().replace('\n', ', ')
        city = fake.city()
        region = fake.state()  
        postal_code = fake.zipcode()
        country = fake.country()
        home_phone = fake.phone_number()
        extension = str(random.randint(1000, 9999))  

      
        cursor.execute(
            """INSERT INTO Employees (EmployeeID, LastName, FirstName, Title, BirthDate, HireDate, 
                                       Address, City, Region, PostalCode, Country, HomePhone, Extension, ReportsTo) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)""",
            employee_id, last_name, first_name, title, birth_date, hire_date,
            address, city, region, postal_code, country, home_phone, extension
        )
        employee_ids.append(employee_id) 

    return employee_ids


def assign_supervisors(employee_ids):
    for employee_id in employee_ids:
        
        if len(employee_ids) > 1:  
            reports_to = random.choice(employee_ids)  
            while reports_to == employee_id:
                reports_to = random.choice(employee_ids)
            cursor.execute(
                "UPDATE Employees SET ReportsTo = ? WHERE EmployeeID = ?",
                reports_to, employee_id
            )

def populate_employee_territories(n):
    cursor.execute("SELECT EmployeeID FROM Employees")  
    employee_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT TerritoryID FROM Territories")  
    territory_ids = [row[0] for row in cursor.fetchall()]

    existing_combinations = set()  

    for _ in range(n):
        while True:
            employee_id = random.choice(employee_ids)          
            territory_id = random.choice(territory_ids)       
            combination = (employee_id, territory_id)

         
            if combination not in existing_combinations:
                cursor.execute(
                    "INSERT INTO EmployeeTerritories (EmployeeID, TerritoryID) VALUES (?, ?)",
                    employee_id, territory_id
                )
                existing_combinations.add(combination)  
                break  

employee_ids = populate_employees(10)  
assign_supervisors(employee_ids)  
populate_employee_territories(20)  

conn.commit()

conn.close()

print("Data inserted successfully!")
