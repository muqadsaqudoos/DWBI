import pyodbc
import time
import matplotlib.pyplot as plt


conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)
cursor = conn.cursor()

pk_queries = {
    "Order by OrderID": "SELECT * FROM Orders WHERE OrderID = 10248",
    "Customer by CustomerID": "SELECT * FROM Customers WHERE CustomerID = 'ALFKI'",
    "Supplier by SupplierID": "SELECT * FROM Suppliers WHERE SupplierID = 1",
    "Product by ProductID": "SELECT * FROM Products WHERE ProductID = 1",
    "Employee by EmployeeID": "SELECT * FROM Employees WHERE EmployeeID = 1"
}

non_pk_queries = {
    "Customer by CustomerName": "SELECT * FROM Customers WHERE CompanyName = 'Alfreds Futterkiste'",
    "Shipper by CompanyName": "SELECT * FROM Shippers WHERE CompanyName = 'Speedy Express'",
    "Orders by OrderDate": "SELECT * FROM Orders WHERE OrderDate = '1996-07-04'",
    "Orders by CustomerName": "SELECT * FROM Orders INNER JOIN Customers ON Orders.CustomerID = Customers.CustomerID WHERE CompanyName = 'Alfreds Futterkiste'",
    "Orders by ShipperCompanyName": "SELECT * FROM Orders INNER JOIN Shippers ON Orders.ShipVia = Shippers.ShipperID WHERE CompanyName = 'Speedy Express'"
}

execution_times_pk = {}
execution_times_non_pk = {}


for query_name, query in pk_queries.items():
    start_time = time.time()
    cursor.execute(query)
    cursor.fetchall()  
    end_time = time.time()
    execution_times_pk[query_name] = (end_time - start_time) * 1000  

for query_name, query in non_pk_queries.items():
    start_time = time.time()
    cursor.execute(query)
    cursor.fetchall()  
    end_time = time.time()
    execution_times_non_pk[query_name] = (end_time - start_time) * 1000  

conn.close()


execution_times = {**execution_times_pk, **execution_times_non_pk}

plt.figure(figsize=(10, 6))
plt.bar(execution_times.keys(), execution_times.values(), color=['blue' if 'Order' in k else 'green' for k in execution_times.keys()])
plt.xticks(rotation=90)
plt.xlabel('Queries')
plt.ylabel('Execution Time (ms)')
plt.title('Query Execution Times for PK and Non-PK Indexes')
plt.tight_layout()
plt.show()