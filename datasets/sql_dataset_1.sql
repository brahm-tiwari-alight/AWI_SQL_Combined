
-- Sample SQL Dataset 1
CREATE TABLE dataset_1 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_1 (name, value) VALUES 
    ('Sample Record A', 10.5),
    ('Sample Record B', 15.3),
    ('Test Data 1', 7.8);

SELECT * FROM dataset_1 WHERE value > 5;
