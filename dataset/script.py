import sqlite3
import json
from datasets import datasets, two_pops

conn = sqlite3.connect('dataset.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS dataset
    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
    data TEXT,
    num_elements INTEGER
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS two_pops (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group1 TEXT,
    group2 TEXT,
    t_value REAL,
    assumption TEXT,
    num_elements INTEGER
)
''')

for data in datasets: 
    num_elements = len(data)
    cursor.execute("INSERT INTO dataset (data, num_elements) VALUES (?, ?)", (json.dumps(data),num_elements))

# Two Pops
for data in two_pops:
    num_elements = len(data)
    cursor.execute('INSERT INTO two_pops (group1, group2, t_value, assumption) VALUES (?, ?, ?, ?)', 
                   (json.dumps(data[0]), json.dumps(data[1]), data[2], data[3]))

conn.commit()
conn.close()
print("Data inserted successfully.")