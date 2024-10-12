import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

suppliers_df = pd.read_csv('northwind/Suppliers.csv', usecols=[0, 1, 2, 3, 4, 5, 6, 7], header=0)

suppliers_df.columns = suppliers_df.columns.str.strip()

print("DataFrame Contents:")
print(suppliers_df.head())

print("Column names:", suppliers_df.columns)
print("Data types:", suppliers_df.dtypes)

for index, row in suppliers_df.iterrows():
    supplier_id = index + 1 
    company_name = str(row['SupplierName']).strip() if pd.notnull(row['SupplierName']) else None
    contact_name = str(row['ContactName']).strip() if pd.notnull(row['ContactName']) else None
    address = str(row['Address']).strip() if pd.notnull(row['Address']) else None
    city = str(row['City']).strip() if pd.notnull(row['City']) else None
    postal_code = str(row['PostalCode']).strip() if pd.notnull(row['PostalCode']) else None
    country = str(row['Country']).strip() if pd.notnull(row['Country']) else None
    phone = str(row['Phone']).strip() if pd.notnull(row['Phone']) else None

    print(f"Inserting row {index}: SupplierID='{supplier_id}', CompanyName='{company_name}', "
          f"ContactName='{contact_name}', Address='{address}', City='{city}', "
          f"PostalCode='{postal_code}', Country='{country}', Phone='{phone}'")

    try:
    
        cursor.execute(
            """INSERT INTO Suppliers (SupplierID, CompanyName, ContactName, ContactTitle, Address, 
               City, Region, PostalCode, Country, Phone, Fax, Homepage) 
               VALUES (?, ?, ?, NULL, ?, ?, NULL, ?, ?, ?, NULL, NULL)""",
            (supplier_id, company_name, contact_name, address, city, postal_code, country, phone)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")

conn.commit()
conn.close()

print("Data inserted successfully!")
