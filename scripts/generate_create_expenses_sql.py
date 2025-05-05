import pandas as pd
from pathlib import Path

# Paths
base_path = Path(__file__).resolve().parents[1]
input_folder = base_path / "finance" / "receipts_from_last_night"
employee_csv = base_path / "hr" / "employee_index.csv"
output_sql = base_path / "sql" / "create_expenses.sql"

# Load employee name to ID map
employees = pd.read_csv(employee_csv)
name_to_id = {
    f"{row['first_name']} {row['last_name']}": int(row['employee_id'])
    for _, row in employees.iterrows()
}

# Parse all .txt files
expenses = []

for file in input_folder.glob("*.txt"):
    with open(file, encoding="utf-8") as f:
        lines = f.readlines()
        record = {}
        for line in lines:
            line = line.strip()
            if line.startswith("Employee:"):
                record["name"] = line.split("Employee:")[1].strip()
            elif line.startswith("Unit Price:"):
                record["price"] = float(line.split("Unit Price:")[1].strip())
            elif line.startswith("Quantity:"):
                record["quantity"] = int(line.split("Quantity:")[1].strip())

        if all(k in record for k in ["name", "price", "quantity"]):
            emp_id = name_to_id.get(record["name"])
            if emp_id:
                expenses.append((emp_id, record["price"], record["quantity"]))
            else:
                print(f"⚠️ Name not found in employee list: {record['name']}")

# Generate SQL
sql = "-- Creates the EXPENSE table from receipts_from_last_night\n"
sql += "CREATE TABLE memory.default.expense (\n"
sql += "    employee_id TINYINT,\n"
sql += "    unit_price DECIMAL(8, 2),\n"
sql += "    quantity TINYINT\n);\n\n"

if expenses:
    sql += "-- Inserts all parsed expenses\n"
    sql += "INSERT INTO memory.default.expense VALUES\n"
    sql += ",\n".join(f"({emp_id}, {price:.2f}, {qty})" for emp_id, price, qty in expenses)
    sql += ";\n"
else:
    sql += "-- ⚠️ No data to insert\n"

# Save
output_sql.write_text(sql, encoding="utf-8")
print(f"✅ SQL file created at: {output_sql}")

