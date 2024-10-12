import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

products_df = pd.read_csv('northwind/products.csv', usecols=[0, 1, 2, 3, 4, 5], header=0)

products_df.columns = products_df.columns.str.strip()

print("DataFrame Contents:")
print(products_df.head())

print("Column names:", products_df.columns)
print("Data types:", products_df.dtypes)


for index, row in products_df.iterrows():
    product_id = index + 1  
    product_name = str(row['ProductName']).strip() if pd.notnull(row['ProductName']) else None
    supplier_id = int(row['SupplierID']) if pd.notnull(row['SupplierID']) else None  
    category_id = int(row['CategoryID']) if pd.notnull(row['CategoryID']) else None  
    quantity_per_unit = str(row['Unit']).strip() if pd.notnull(row['Unit']) else None
    unit_price = float(row['Price']) if pd.notnull(row['Price']) else None

    print(f"Inserting row {index}: ProductID='{product_id}', ProductName='{product_name}', "
          f"SupplierID='{supplier_id}', CategoryID='{category_id}', QuantityPerUnit='{quantity_per_unit}', "
          f"UnitPrice='{unit_price}'")

    try:
        cursor.execute(
            """INSERT INTO Products (ProductID, ProductName, SupplierID, CategoryID, QuantityPerUnit, 
               UnitPrice, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued) 
               VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, NULL, 0)""",
            (product_id, product_name, supplier_id, category_id, quantity_per_unit, unit_price)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")

conn.commit()
conn.close()

print("Data inserted successfully!")
