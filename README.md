# 🧠 SilverBullet SQL Challenge — My Take

Hi there! 👋 I'm Bartłomiej, and this is my personal fork + solution to the `wasb_sql_test` repo from SilverBullet. I kept it clean, reproducible, and fun to work with.

---

## 🚀 Quickstart (30 seconds)

### Requirements:

* Docker Desktop (running)
* Python 3.9+
* Git Bash (for `chmod +x`) or WSL

### 1. Clone this repo and go into it:

```bash
git clone https://github.com/francessco12/wasb_sql_test.git
cd wasb_sql_test
```

### 2. Create virtual environment and install requirements:

```bash
python -m venv venv
source venv/Scripts/activate  # or . venv/bin/activate on Unix
pip install -r requirements.txt  # optional (no heavy deps used)
```

### 3. Run Trino in Docker:

```bash
docker run --name=sexi-silverbullet -d trinodb/trino
```

### 4. Load all SQL into Trino:

```bash
chmod +x load_all.sh
./load_all.sh
```

### 5. Explore! 🕵️

```bash
docker exec -it sexi-silverbullet trino
```

Then:

```sql
USE memory.default;
SHOW TABLES;
SELECT * FROM employee;
```

---

## 📁 Project Structure

```
wasb_sql_test/
├── finance/
│   ├── invoices_due/
│   │   └── *.txt         # raw invoice files
│   └── receipts_from_last_night/
│       └── *.txt         # raw expense data
├── hr/
│   └── employee_index.csv
├── scripts/
│   └── generate_*.py     # all Python scripts to convert raw -> SQL
├── sql/
│   └── *.sql             # final SQL scripts (CTEs, inserts, queries)
├── load_all.sh           # load everything into Trino
├── README.md             # you're here!
└── .gitignore
```

---

## ✨ Highlights (a.k.a. Why this repo might stand out)

✅ **Automation**: One-click loader (`load_all.sh`) and SQL generators via Python.
✅ **Readable SQL**: All `.sql` files have comments, spacing, and clean CTEs.
✅ **CI/CD Mindset**: Easy to plug into future pipelines (data validation included).
✅ **Edge Cases**: Monthly truncation, leap years, bad data parsing — handled.
✅ **Git Hygiene**: Logical commits, one-liners like `feat: add invoice ingestion`.

---

## 🧪 Final Output

This repo includes working implementations for:

* `employee` hierarchy (with cycle detection)
* `expense` aggregation from multiple raw files
* `invoice` parsing with due dates
* `supplier_payments` monthly plan generator
* recursive CTEs, joins, and analytical logic

All queries tested directly in Trino engine.

---

📊 Answers & Final Results
Here are the final answers and outputs for the SExI system:

✅ 1. EMPLOYEE table
Created from employee_index.csv

Includes employee_id, first_name, last_name, job_title, manager_id

Type-safe: TINYINT, VARCHAR

Data inserted manually via SQL

✅ 2. EXPENSE table
Aggregated data from 7 messy .txt files under finance/receipts_from_last_night

Extracted fields: employee_id, unit_price, quantity

Validated with SELECT COUNT(*), 7 rows loaded

✅ 3. INVOICE & SUPPLIER tables
Data parsed from .txt files in finance/invoices_due/

Suppliers matched alphabetically to IDs

Due dates normalized to end-of-month using last_day() logic

Inserted into supplier and invoice tables

✅ 4. Manager loop detection
Recursive CTE used to trace reporting chains

✅ No loops found (SELECT * FROM ... WHERE has_loop = TRUE returned 0 rows)

✅ 5. Big spenders report
employee_id	employee_name	manager_id	manager_name	total_expensed_amount
3	Alex Jacobson	2	Umberto Torrielli	1682.00

✅ 6. Monthly supplier payment plan
Based on invoice_amount and due_date

Generates monthly payments starting at end of current month

Ensures full repayment before each invoice’s deadline

All suppliers receive one payment per month, even if they have multiple invoices


## 📫 Wanna chat?

Open to feedback, contributions, or job chats. You can find me on [LinkedIn](https://www.linkedin.com/in/bartlomiejwojcik) or GitHub ✌️

---

Thanks for reading!

> Made with ❤️ and SQL.
