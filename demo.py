import pyodbc
from faker import Faker
import random

# Database connection
conn = pyodbc.connect(
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=Muqadsa-123\\MUQADSA_QUDOOS;"  # Replace with your actual server name
    "Database=NorthWind_1;"               # Replace with your database name
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()

# Initialize Faker
fake = Faker()

# Function to populate Regions
def populate_regions(n):
    for _ in range(n):
        region_id = random.randint(1, 1000)  # Generate random region_id
        region_desc = fake.city_suffix()     # Fake city suffix for region description
        cursor.execute(
            "INSERT INTO Regions (RegionID, RegionDescription) VALUES (?, ?)",
            region_id, region_desc
        )

# Function to populate Territories
def populate_territories(n):
    cursor.execute("SELECT RegionID FROM Regions")  # Get available RegionIDs
    region_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        territory_id = fake.unique.zipcode()          # Fake and unique territory id
        territory_desc = fake.city()                 # Fake city name for description
        region_id = random.choice(region_ids)        # Randomly pick a RegionID
        cursor.execute(
            "INSERT INTO Territories (TerritoryID, TerritoryDescription, RegionID) VALUES (?, ?, ?)",
            territory_id, territory_desc, region_id
        )

# Populate the tables
populate_regions(10)  # Populate 10 regions
populate_territories(20)  # Populate 20 territories

# Commit the transactions
conn.commit()

# Close the connection
conn.close()

print("Data inserted successfully!")
