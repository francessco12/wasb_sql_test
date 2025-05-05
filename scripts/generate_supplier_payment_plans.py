import pandas as pd
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta

# 📁 Paths
base_path = Path(__file__).resolve().parents[1]
invoice_path = base_path / "sql" / "create_invoices.sql"
output_path = base_path / "sql" / "generate_supplier_payment_plans.sql"

# 📅 Last day of month helper
def last_day_of_month(dt):
    next_month = dt.replace(day=28) + relativedelta(days=4)
    return next_month - relativedelta(days=next_month.day)

# 📥 Parse the invoice SQL file
invoices = []
suppliers = {}

with open(invoice_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Read supplier names
for line in lines:
    if line.strip().startswith("INSERT INTO memory.default.supplier VALUES"):
        supplier_lines = lines[lines.index(line)+1:]
        for l in supplier_lines:
            if l.strip().startswith("("):
                parts = l.strip().strip(",;").split(",")
                sid = int(parts[0].strip("() "))
                name = parts[1].strip("() ").strip("'")
                suppliers[sid] = name
            else:
                break

# Read invoice data
for line in lines:
    if line.strip().startswith("INSERT INTO memory.default.invoice VALUES"):
        invoice_lines = lines[lines.index(line)+1:]
        for l in invoice_lines:
            if l.strip().startswith("("):
                parts = l.strip().strip(",;").split(",")
                sid = int(parts[0].strip("() "))
                amount = float(parts[1].strip())
                due_str = parts[2].replace("DATE", "").replace("'", "").replace(")", "").strip()
                due = pd.to_datetime(due_str, format="%Y-%m-%d")
                invoices.append((sid, amount, due))
            else:
                break

df = pd.DataFrame(invoices, columns=["supplier_id", "invoice_amount", "due_date"])
df["supplier_name"] = df["supplier_id"].map(suppliers)

# 🧮 Generate payment plan
payment_rows = []
start_date = last_day_of_month(datetime.now())

for _, row in df.iterrows():
    total = row.invoice_amount
    months = 1
    current = start_date
    while current < row.due_date:
        months += 1
        current += relativedelta(months=1)
    monthly_payment = round(total / months, 2)

    balance = total
    for i in range(months):
        payment = monthly_payment if i < months - 1 else round(balance, 2)
        payment_date = last_day_of_month(start_date + relativedelta(months=i))
        balance -= payment
        payment_rows.append((
            row.supplier_id,
            row.supplier_name,
            f"{payment:.2f}",
            f"{max(balance, 0):.2f}",
            payment_date.strftime("%Y-%m-%d")
        ))

# 📝 Generate SQL
sql = "-- Monthly payment plan for all suppliers\n"
sql += "CREATE TABLE memory.default.supplier_payments (\n"
sql += "    supplier_id TINYINT,\n"
sql += "    supplier_name VARCHAR,\n"
sql += "    payment_amount DECIMAL(8,2),\n"
sql += "    balance_outstanding DECIMAL(8,2),\n"
sql += "    payment_date DATE\n);\n\n"

sql += "INSERT INTO memory.default.supplier_payments VALUES\n"
sql += ",\n".join(
    f"({sid}, '{name}', {amount}, {balance}, DATE '{date}')"
    for sid, name, amount, balance, date in payment_rows
)
sql += ";\n"

output_path.write_text(sql, encoding="utf-8")
print(f"✅ SQL payment plan generated at: {output_path}")
