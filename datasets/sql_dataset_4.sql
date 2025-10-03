
-- Sample SQL Dataset 4
CREATE TABLE dataset_4 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_4 (name, value) VALUES 
    ('Sample Record A', 42.0),
    ('Sample Record B', 61.2),
    ('Test Data 4', 31.2);

SELECT * FROM dataset_4 WHERE value > 20;
