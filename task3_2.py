import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

customers_df = pd.read_csv('northwind/Customers.csv', usecols=[0, 1, 2, 3, 4, 5, 6], header=0)

customers_df.columns = customers_df.columns.str.strip()

print("DataFrame Contents:")
print(customers_df.head())

print("Column names:", customers_df.columns)
print("Data types:", customers_df.dtypes)

for index, row in customers_df.iterrows():
    customer_id = str(row['CustomerID']).strip() if pd.notnull(row['CustomerID']) else None
    
    if customer_id is None or not customer_id.isalnum():
        print(f"Skipping row {index}: Invalid CustomerID '{customer_id}'")
        continue

    company_name = str(row['CustomerName']).strip() if pd.notnull(row['CustomerName']) else None
    contact_name = str(row['ContactName']).strip() if pd.notnull(row['ContactName']) else None
    address = str(row['Address']).strip() if pd.notnull(row['Address']) else None
    city = str(row['City']).strip() if pd.notnull(row['City']) else None
    postal_code = str(row['PostalCode']).strip() if pd.notnull(row['PostalCode']) else None
    
    country = str(row['Country']).strip() if pd.notnull(row['Country']) else None
    
    if not isinstance(row['Country'], str):
        country = None

    print(f"Inserting row {index}: CustomerID='{customer_id}', CompanyName='{company_name}', "
          f"ContactName='{contact_name}', Address='{address}', City='{city}', "
          f"PostalCode='{postal_code}', Country='{country}'")

    try:
        cursor.execute(
            """INSERT INTO Customers (CustomerID, CompanyName, ContactName, ContactTitle, Address, 
               City, Region, PostalCode, Country, Phone, Fax) 
               VALUES (?, ?, ?, NULL, ?, ?, NULL, ?, ?, NULL, NULL)""",
            (customer_id, company_name, contact_name, address, city, postal_code, country)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")

conn.commit()
conn.close()

print("Data inserted successfully!")
