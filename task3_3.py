import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

shippers_df = pd.read_csv('northwind/shippers.csv', usecols=[0, 1, 2], header=0)

shippers_df.columns = shippers_df.columns.str.strip()

print("DataFrame Contents:")
print(shippers_df.head())

print("Column names:", shippers_df.columns)
print("Data types:", shippers_df.dtypes)

for index, row in shippers_df.iterrows():
    shipper_id = index + 1  
    company_name = str(row['CompanyName']).strip() if pd.notnull(row['CompanyName']) else None
    phone = str(row['Phone']).strip() if pd.notnull(row['Phone']) else None

    print(f"Inserting row {index}: ShipperID='{shipper_id}', CompanyName='{company_name}', Phone='{phone}'")

    try:
      
        cursor.execute(
            """INSERT INTO Shippers (ShipperID, CompanyName, Phone) 
               VALUES (?, ?, ?)""",
            (shipper_id, company_name, phone)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")


conn.commit()
conn.close()

print("Data inserted successfully!")
