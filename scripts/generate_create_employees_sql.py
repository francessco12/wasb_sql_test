import pandas as pd
from pathlib import Path

# Define paths
base_path = Path(__file__).resolve().parents[1]  # goes up to /wasb_sql_test
input_csv = base_path / "hr" / "employee_index.csv"
output_sql = base_path / "sql" / "create_employees.sql"

# Load employee data
df = pd.read_csv(input_csv)

# Define column types based on actual CSV
column_types = {
    "employee_id": "TINYINT",
    "first_name": "VARCHAR",
    "last_name": "VARCHAR",
    "job_title": "VARCHAR",
    "manager_id": "TINYINT"
}

# Build CREATE TABLE statement
create_sql = "-- Creates the EMPLOYEE table based on employee_index.csv\n"
create_sql += "CREATE TABLE employee (\n"
create_sql += ",\n".join([f"    {col} {column_types[col]}" for col in df.columns])
create_sql += "\n);\n\n"

# Build INSERT statements
insert_sql = "-- Inserts all employees into the EMPLOYEE table\n"
insert_sql += "INSERT INTO employee VALUES\n"

values = []
for _, row in df.iterrows():
    row_parts = []
    for col in df.columns:
        val = row[col]
        if pd.isna(val):
            row_parts.append("NULL")
        elif column_types[col] == "TINYINT":
            row_parts.append(str(int(val)))
        else:
            row_parts.append(f"'{str(val)}'")
    values.append("(" + ", ".join(row_parts) + ")")

insert_sql += ",\n".join(values) + ";\n"

# Save to file
output_sql.write_text(create_sql + insert_sql, encoding="utf-8")
print(f"✅ File generated at: {output_sql}")
