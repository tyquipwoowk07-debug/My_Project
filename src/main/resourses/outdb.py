import sqlite3
import json
import csv
import xml.etree.ElementTree as ET
import os
from pathlib import Path

DB_PATH = r"C:\Users\888\Desktop\main\src\main\mainDataBase.db"
TABLE_NAME = "Booking"

output_dir = Path("out")
output_dir.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(f"SELECT * FROM {TABLE_NAME}")
main_data = cursor.fetchall()

cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
columns = [col[1] for col in cursor.fetchall()]

cursor.execute(f"PRAGMA foreign_key_list({TABLE_NAME})")
foreign_keys = cursor.fetchall()

result_data = []

for row in main_data:
    record = {}

    for i, col_name in enumerate(columns):
        record[col_name] = row[i]

    for fk in foreign_keys:
        fk_column = fk[3]
        fk_table = fk[2]
        fk_primary = fk[4]

        if record[fk_column]:
            cursor.execute(f"SELECT * FROM {fk_table} WHERE {fk_primary} = ?", (record[fk_column],))
            foreign_data = cursor.fetchone()

            if foreign_data:
                cursor.execute(f"PRAGMA table_info({fk_table})")
                foreign_columns = [col[1] for col in cursor.fetchall()]

                record[fk_table] = {}
                for j, fk_col in enumerate(foreign_columns):
                    record[fk_table][fk_col] = foreign_data[j]

    result_data.append(record)

conn.close()

with open(output_dir / "data.json", 'w', encoding='utf-8') as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)
print("Данные экспортированы в data.json")

with open(output_dir / "data.csv", 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    headers = []
    for col in columns:
        headers.append(col)

    writer.writerow(headers)

    for row in result_data:
        csv_row = []
        for col in columns:
            csv_row.append(row[col])
        writer.writerow(csv_row)
print("Данные экспортированы в data.csv")

root = ET.Element('data')
root.set('table', TABLE_NAME)

for row in result_data:
    record_elem = ET.SubElement(root, 'record')

    for key, value in row.items():
        if isinstance(value, dict):
            foreign_elem = ET.SubElement(record_elem, key)
            for fk_key, fk_value in value.items():
                field_elem = ET.SubElement(foreign_elem, fk_key)
                field_elem.text = str(fk_value) if fk_value is not None else ''
        else:
            field_elem = ET.SubElement(record_elem, key)
            field_elem.text = str(value) if value is not None else ''

tree = ET.ElementTree(root)
tree.write(output_dir / "data.xml", encoding='utf-8', xml_declaration=True)
print("Данные экспортированы в data.xml")

yaml_content = ""
for record in result_data:
    yaml_content += "-\n"
    for key, value in record.items():
        if isinstance(value, dict):
            yaml_content += f"  {key}:\n"
            for sub_key, sub_value in value.items():
                yaml_content += f"    {sub_key}: {sub_value}\n"
        else:
            yaml_content += f"  {key}: {value}\n"

with open(output_dir / "data.yaml", 'w', encoding='utf-8') as f:
    f.write(yaml_content)
print("Данные экспортированы в data.yaml")
print("Все файлы успешно созданы в папке 'out'!")
