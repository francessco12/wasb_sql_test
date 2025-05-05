import re
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

# Paths
base_path = Path(__file__).resolve().parents[1]
input_folder = base_path / "finance" / "invoices_due"
output_sql = base_path / "sql" / "create_invoices.sql"

# Helper: get last day of month
def last_day_of_month(dt):
    next_month = dt.replace(day=28) + relativedelta(days=4)
    return next_month - relativedelta(days=next_month.day)

# Parse invoice files
records = []
for file in input_folder.glob("*.txt"):
    with open(file, "r", encoding="utf-8") as f:
        lines = f.read()
        company = re.search(r"Company Name:\s*(.+)", lines)
        amount = re.search(r"Invoice Amount:\s*([\d.]+)", lines)
        due = re.search(r"Due Date:\s*(\d+)\s+months\s+from\s+now", lines)
        if company and amount and due:
            name = company.group(1).strip()
            value = float(amount.group(1).strip())
            months = int(due.group(1).strip())
            due_date = last_day_of_month(datetime.now() + relativedelta(months=months))
            records.append((name, value, due_date.date()))

# Assign supplier_id alphabetically
df = pd.DataFrame(records, columns=["name", "invoice_amount", "due_date"])
unique_suppliers = sorted(df["name"].unique())
supplier_map = {name: idx + 1 for idx, name in enumerate(unique_suppliers)}
df["supplier_id"] = df["name"].map(supplier_map)

# Build supplier DataFrame
suppliers = pd.DataFrame([
    {"supplier_id": sid, "name": name}
    for name, sid in supplier_map.items()
]).sort_values("supplier_id")

# Generate SQL
sql = "-- Create SUPPLIER table\n"
sql += "CREATE TABLE memory.default.supplier (\n"
sql += "    supplier_id TINYINT,\n"
sql += "    name VARCHAR\n);\n\n"

sql += "-- Insert suppliers\n"
sql += "INSERT INTO memory.default.supplier VALUES\n"
sql += ",\n".join(
    f"({row['supplier_id']}, '{str(row['name']).replace('\'', '\'\'')}')"
    for _, row in suppliers.iterrows()
)
sql += ";\n\n"

sql += "-- Create INVOICE table\n"
sql += "CREATE TABLE memory.default.invoice (\n"
sql += "    supplier_id TINYINT,\n"
sql += "    invoice_amount DECIMAL(8,2),\n"
sql += "    due_date DATE\n);\n\n"

sql += "-- Insert invoices\n"
sql += "INSERT INTO memory.default.invoice VALUES\n"
sql += ",\n".join(
    f"({row.supplier_id}, {row.invoice_amount:.2f}, DATE '{row.due_date}')"
    for _, row in df.iterrows()
)
sql += ";\n"

# Save to file
output_sql.write_text(sql, encoding="utf-8")
print(f"✅ SQL generated: {output_sql}")
