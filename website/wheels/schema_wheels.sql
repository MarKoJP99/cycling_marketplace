-- removed the DROP TABLE IF EXISTS products as i 
-- dont want to update the table each time i run upload 
-- a new csv file

-- DROP TABLE IF EXISTS products;


CREATE TABLE wheels (
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
);
