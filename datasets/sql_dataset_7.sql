
-- Sample SQL Dataset 7
CREATE TABLE dataset_7 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_7 (name, value) VALUES 
    ('Sample Record A', 73.5),
    ('Sample Record B', 107.10000000000001),
    ('Test Data 7', 54.6);

SELECT * FROM dataset_7 WHERE value > 35;
