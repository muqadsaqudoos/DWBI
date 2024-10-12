import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

order_details_df = pd.read_csv('northwind/Order_details.csv', usecols=[0, 1, 2, 3], header=0)

order_details_df.columns = order_details_df.columns.str.strip()

cursor.execute("SELECT OrderID FROM Orders")
valid_order_ids = {row[0] for row in cursor.fetchall()}

cursor.execute("SELECT ProductID FROM Products")
valid_product_ids = {row[0] for row in cursor.fetchall()}

print("DataFrame Contents:")
print(order_details_df.head())
print("Valid Order IDs:", valid_order_ids)
print("Valid Product IDs:", valid_product_ids)

print("Column names:", order_details_df.columns)
print("Data types:", order_details_df.dtypes)

for index, row in order_details_df.iterrows():
    order_id = int(row['OrderID']) if pd.notnull(row['OrderID']) else None
    product_id = int(row['ProductID']) if pd.notnull(row['ProductID']) else None
    quantity = int(row['Quantity']) if pd.notnull(row['Quantity']) else None
    unit_price = float(row.get('UnitPrice', 0)) 
    discount = float(row.get('Discount', 0))  

    if order_id not in valid_order_ids:
        print(f"Skipping row {index}: Invalid OrderID='{order_id}'")
        continue  
    
    if product_id not in valid_product_ids:
        print(f"Skipping row {index}: Invalid ProductID='{product_id}'")
        continue 

    print(f"Inserting row {index}: OrderID='{order_id}', ProductID='{product_id}', "
          f"Quantity='{quantity}', UnitPrice='{unit_price}', Discount='{discount}'")

    try:
       
        cursor.execute(
            """INSERT INTO OrderDetails (OrderID, ProductID, UnitPrice, Quantity, Discount) 
               VALUES (?, ?, ?, ?, ?)""",
            (order_id, product_id, unit_price, quantity, discount)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")

conn.commit()
conn.close()

print("Data inserted successfully!")
