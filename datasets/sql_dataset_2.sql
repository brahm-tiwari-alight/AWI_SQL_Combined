
-- Sample SQL Dataset 2
CREATE TABLE dataset_2 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_2 (name, value) VALUES 
    ('Sample Record A', 21.0),
    ('Sample Record B', 30.6),
    ('Test Data 2', 15.6);

SELECT * FROM dataset_2 WHERE value > 10;
