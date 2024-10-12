import pandas as pd
import pyodbc

conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"
    "Database=NorthWind_1;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

categories_df = pd.read_csv('northwind/categories.csv', usecols=[0, 1, 2], header=0)

print("DataFrame Contents:")
print(categories_df.head())

for index, row in categories_df.iterrows():
    category_id_str = str(row['CategoryID']).strip() if pd.notnull(row['CategoryID']) else None
    
    if category_id_str is None or not category_id_str.isdigit():
        print(f"Skipping row {index}: Invalid CategoryID '{category_id_str}'")
        continue

    category_id = int(category_id_str)

    category_name = str(row['CategoryName']).strip() if pd.notnull(row['CategoryName']) else None

    description_parts = []
    for value in row[2:]:
        if pd.notnull(value):
            cleaned_value = str(value).strip()
            if cleaned_value:
                description_parts.append(cleaned_value)

    description = ' '.join(description_parts)

    if category_name is None or description.strip() == "":
        print(f"Skipping row {index}: Missing CategoryName or Description")
        continue

    print(f"Inserting row {index}: CategoryID={category_id}, CategoryName='{category_name}', Description='{description}'")

    try:
        cursor.execute(
            """INSERT INTO Categories (CategoryID, CategoryName, Description, Picture) 
               VALUES (?, ?, ?, NULL)""",
            (category_id, category_name, description)
        )
    except pyodbc.Error as db_error:
        raise RuntimeError(f"Error inserting row {index}: {db_error}")

conn.commit()
conn.close()

print("Data inserted successfully!")
