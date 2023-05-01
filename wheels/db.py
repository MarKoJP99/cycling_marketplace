import os
import sqlite3
import csv

# DATABASE is the path to the database file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "wheels_database.db")


def get_db(database=DATABASE):
    conn = sqlite3.connect(database)
    return conn


def init_db(app):
    with app.app_context():
        conn = get_db("wheels_database.db")
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='wheels'")
        if not cur.fetchone():
            create_wheels_table()
            with open(os.path.join(BASE_DIR, "schema_wheels.sql"), "r") as f:
                conn.executescript(f.read())

        conn.commit()

def search_products(database, query):
    conn = get_db(database)
    cur = conn.cursor()
    query = f"%{query}%"
    cur.execute("SELECT DISTINCT * FROM products WHERE product_name LIKE ? OR description LIKE ?", (query, query))
    results = cur.fetchall()
    return results

def create_wheels_table():
    conn = get_db("wheels_database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS wheels (
            id INTEGER PRIMARY KEY,
            brand TEXT,
            model_name TEXT,
            package_set TEXT,
            brake_type TEXT,
            tyres_type TEXT,
            weight_set REAL,
            weight_front REAL,
            weight_rear REAL,
            rim_depth REAL,
            rim_internal_width REAL,
            rim_external_width REAL,
            rim_material TEXT,
            sproks_material_front TEXT,
            sproks_material_rear TEXT,
            hub_material_front TEXT,
            hub_material_rear TEXT,
            bearings_type TEXT,
            suggested_price_euro REAL,
            url_maker TEXT,
            url_shop TEXT,
            item_component TEXT,
            item_price REAL,
            discount REAL,
            colour TEXT,
            edition TEXT
        )
    """)
    conn.commit()
    conn.close()

def search_wheels(query):
    conn = get_db("wheels_database.db")
    cur = conn.cursor()
    query = f"%{query}%"
    cur.execute("""SELECT DISTINCT * FROM wheels WHERE brand LIKE ? 
                OR model_name LIKE ? 
                OR package_set LIKE ? 
                OR brake_type LIKE ? 
                OR tyres_type LIKE ? 
                OR rim_material LIKE ? 
                OR sproks_material_front LIKE ? 
                OR sproks_material_rear LIKE ? 
                OR hub_material_front LIKE ? 
                OR hub_material_rear LIKE ? 
                OR bearings_type LIKE ? 
                OR colour LIKE ? 
                OR edition LIKE ?""",
                (query, query, query, query, query, query, query, query, query, query, query, query, query))
    results = cur.fetchall()
    return results

def import_wheels_data(csv_file_path):
    conn = get_db("wheels_database.db")
    cur = conn.cursor()

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cur.execute("""
                INSERT INTO wheels (
                    brand, model_name, package_set, brake_type, tyres_type, weight_set,
                    weight_front, weight_rear, rim_depth, rim_internal_width, rim_external_width,
                    rim_material, sproks_material_front, sproks_material_rear, hub_material_front,
                    hub_material_rear, bearings_type, suggested_price_euro, url_maker, url_shop,
                    item_component, item_price, discount, colour, edition
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['brand'], row['model_name'], row['package_set'], row['brake_type'], row['tyres_type'],
                row['weight_set'], row['weight_front'], row['weight_rear'], row['rim_depth'],
                row['rim_internal_width'], row['rim_external_width'], row['rim_material'],
                row['sproks_material_front'], row['sproks_material_rear'], row['hub_material_front'],
                row['hub_material_rear'], row['bearings_type'], row['suggested_price_euro'],
                row['url_maker'], row['url_shop'], row['item_component'], row['item_price'],
                row['discount'], row['colour'], row['edition']
            ))

    conn.commit()
    conn.close()
