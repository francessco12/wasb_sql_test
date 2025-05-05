-- Monthly payment plan for all suppliers
CREATE TABLE memory.default.supplier_payments (
    supplier_id TINYINT,
    supplier_name VARCHAR,
    payment_amount DECIMAL(8,2),
    balance_outstanding DECIMAL(8,2),
    payment_date DATE
);

INSERT INTO memory.default.supplier_payments VALUES
(4, 'Party Animals', 1200.00, 4800.00, DATE '2025-05-31'),
(4, 'Party Animals', 1200.00, 3600.00, DATE '2025-06-30'),
(4, 'Party Animals', 1200.00, 2400.00, DATE '2025-07-31'),
(4, 'Party Animals', 1200.00, 1200.00, DATE '2025-08-31'),
(4, 'Party Animals', 1200.00, 0.00, DATE '2025-09-30'),
(1, 'Catering Plus', 500.00, 1500.00, DATE '2025-05-31'),
(1, 'Catering Plus', 500.00, 1000.00, DATE '2025-06-30'),
(1, 'Catering Plus', 500.00, 500.00, DATE '2025-07-31'),
(1, 'Catering Plus', 500.00, 0.00, DATE '2025-08-31'),
(1, 'Catering Plus', 300.00, 1200.00, DATE '2025-05-31'),
(1, 'Catering Plus', 300.00, 900.00, DATE '2025-06-30'),
(1, 'Catering Plus', 300.00, 600.00, DATE '2025-07-31'),
(1, 'Catering Plus', 300.00, 300.00, DATE '2025-08-31'),
(1, 'Catering Plus', 300.00, 0.00, DATE '2025-09-30'),
(2, 'Entertainment tonight', 1200.00, 4800.00, DATE '2025-05-31'),
(2, 'Entertainment tonight', 1200.00, 3600.00, DATE '2025-06-30'),
(2, 'Entertainment tonight', 1200.00, 2400.00, DATE '2025-07-31'),
(2, 'Entertainment tonight', 1200.00, 1200.00, DATE '2025-08-31'),
(2, 'Entertainment tonight', 1200.00, 0.00, DATE '2025-09-30'),
(3, 'Ice Ice Baby', 571.43, 3428.57, DATE '2025-05-31'),
(3, 'Ice Ice Baby', 571.43, 2857.14, DATE '2025-06-30'),
(3, 'Ice Ice Baby', 571.43, 2285.71, DATE '2025-07-31'),
(3, 'Ice Ice Baby', 571.43, 1714.28, DATE '2025-08-31'),
(3, 'Ice Ice Baby', 571.43, 1142.85, DATE '2025-09-30'),
(3, 'Ice Ice Baby', 571.43, 571.42, DATE '2025-10-31'),
(3, 'Ice Ice Baby', 571.42, 0.00, DATE '2025-11-30');
