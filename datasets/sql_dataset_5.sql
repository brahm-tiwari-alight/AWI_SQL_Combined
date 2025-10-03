
-- Sample SQL Dataset 5
CREATE TABLE dataset_5 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_5 (name, value) VALUES 
    ('Sample Record A', 52.5),
    ('Sample Record B', 76.5),
    ('Test Data 5', 39.0);

SELECT * FROM dataset_5 WHERE value > 25;
