-- Create SUPPLIER table
CREATE TABLE memory.default.supplier (
    supplier_id TINYINT,
    name VARCHAR
);

-- Insert suppliers
INSERT INTO memory.default.supplier VALUES
(1, 'Catering Plus'),
(2, 'Entertainment tonight'),
(3, 'Ice Ice Baby'),
(4, 'Party Animals');

-- Create INVOICE table
CREATE TABLE memory.default.invoice (
    supplier_id TINYINT,
    invoice_amount DECIMAL(8,2),
    due_date DATE
);

-- Insert invoices
INSERT INTO memory.default.invoice VALUES
(4, 6000.00, DATE '2025-08-31'),
(1, 2000.00, DATE '2025-07-31'),
(1, 1500.00, DATE '2025-08-31'),
(2, 6000.00, DATE '2025-08-31'),
(3, 4000.00, DATE '2025-11-30');
