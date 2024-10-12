import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

orders_df = pd.read_csv('northwind/orders.csv', usecols=[0, 1, 2, 3, 4], header=0)

orders_df.columns = orders_df.columns.str.strip()

cursor.execute("SELECT CustomerID FROM Customers")
valid_customer_ids = {row[0] for row in cursor.fetchall()}

print("DataFrame Contents:")
print(orders_df.head())
print("Valid Customer IDs:", valid_customer_ids)

print("Column names:", orders_df.columns)
print("Data types:", orders_df.dtypes)

for index, row in orders_df.iterrows():
    order_id = int(row['OrderID']) if pd.notnull(row['OrderID']) else None
    customer_id = str(row['CustomerID']).strip() if pd.notnull(row['CustomerID']) else None
    employee_id = int(row['EmployeeID']) if pd.notnull(row['EmployeeID']) else None
    order_date = pd.to_datetime(row['OrderDate']).date() if pd.notnull(row['OrderDate']) else None
    shipper_id = int(row['ShipperID']) if pd.notnull(row['ShipperID']) else None

    if customer_id not in valid_customer_ids:
        print(f"Skipping row {index}: Invalid CustomerID='{customer_id}'")
        continue 

    print(f"Inserting row {index}: OrderID='{order_id}', CustomerID='{customer_id}', "
          f"EmployeeID='{employee_id}', OrderDate='{order_date}', ShipperID='{shipper_id}'")

    try:
        cursor.execute(
            """INSERT INTO Orders (OrderID, CustomerID, EmployeeID, OrderDate, RequiredDate, 
               ShippedDate, ShipVia, Freight, ShipName, ShipAddress, ShipCity, ShipRegion, 
               ShipPostalCode, ShipCountry) 
               VALUES (?, ?, ?, ?, NULL, NULL, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL)""",
            (order_id, customer_id, employee_id, order_date, shipper_id)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")


conn.commit()
conn.close()

print("Data inserted successfully!")
