import sys
import csv
import sqlite3

from db import create_wheels_table, get_db

def update_database(filename):
    conn = get_db()
    cur = conn.cursor()
    try:
        create_wheels_table()
        
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for row in reader:
                cur.execute(
                    "INSERT OR IGNORE INTO wheels (brand, model_name, package_set, brake_type, tyres_type, weight_set, weight_front, weight_rear, rim_depth, rim_internal_width, rim_external_width, rim_material, sproks_material_front, sproks_material_rear, hub_material_front, hub_material_rear, bearings_type, suggested_price_euro, url_maker, url_shop, item_component, item_price, discount, colour, edition) "
                    "SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM wheels WHERE brand = ? AND model_name = ?)",
                    (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[0], row[1])
                )

        conn.commit()
    finally:
        conn.close()


# Run the script from the command line
if len(sys.argv) > 1:
    csv_file = sys.argv[1]
    update_database(csv_file)
    print("Database updated successfully.")
    
else:
    print("Please provide a CSV file as an argument.")
