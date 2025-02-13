import sqlite3
import pandas as pd

DB_PATH = "qr_usage.db"
ICAMSD_FILE = "ICAMSD_QR_With_Images.xlsx"
ICSMMI_FILE = "ICSMMI_QR_With_Images.xlsx"

# Connect to SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    paper_id TEXT PRIMARY KEY,
    title TEXT,
    author TEXT,
    email TEXT,
    institute TEXT,
    phone TEXT,
    presenter TEXT,
    mode TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS qr_status (
    paper_id TEXT PRIMARY KEY,
    scanned INTEGER DEFAULT 0
)
""")

conn.commit()

# Function to load data
def load_data(file):
    df = pd.read_excel(file)
    for _, row in df.iterrows():
        cursor.execute("INSERT OR IGNORE INTO members VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (row["Paper ID"], row["Paper Title"], row["Author"], row["Email"], row["Institute"], 
                        row["Phone"], row["Presenter"], row["Mode"]))
        cursor.execute("INSERT OR IGNORE INTO qr_status (paper_id) VALUES (?)", (row["Paper ID"],))
    conn.commit()

# Load data from both Excel files
load_data(ICAMSD_FILE)
load_data(ICSMMI_FILE)

conn.close()
print("Database setup complete.")