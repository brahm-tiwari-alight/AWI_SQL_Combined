
-- Sample SQL Dataset 6
CREATE TABLE dataset_6 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_6 (name, value) VALUES 
    ('Sample Record A', 63.0),
    ('Sample Record B', 91.80000000000001),
    ('Test Data 6', 46.8);

SELECT * FROM dataset_6 WHERE value > 30;
