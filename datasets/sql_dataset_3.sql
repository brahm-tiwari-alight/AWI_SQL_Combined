
-- Sample SQL Dataset 3
CREATE TABLE dataset_3 (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    value DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dataset_3 (name, value) VALUES 
    ('Sample Record A', 31.5),
    ('Sample Record B', 45.900000000000006),
    ('Test Data 3', 23.4);

SELECT * FROM dataset_3 WHERE value > 15;
