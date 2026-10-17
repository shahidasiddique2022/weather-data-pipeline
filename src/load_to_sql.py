
import sqlite3
import pandas as pd
import os

DB_PATH = "database/weather.db"
SILVER_DIR = "data/silver"


def get_latest_silver_file():
    """Return the most recent CSV file from the Silver folder."""

    if not os.path.exists(SILVER_DIR):
        raise FileNotFoundError(
            "Silver folder not found. Run your transformation script first."
        )

    files = [
        f for f in os.listdir(SILVER_DIR)
        if f.endswith(".csv")
    ]

    if not files:
        raise FileNotFoundError(
            "No CSV files found in data/silver."
        )

    # Sort by filename, assuming filenames contain dates
    files.sort()
    latest = files[-1]

    return os.path.join(SILVER_DIR, latest)


def create_connection():
    """Create a connection to the SQLite database."""

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    return conn


def create_table(conn):
    """Create the weather table if it does not exist."""

    create_sql = """
    CREATE TABLE IF NOT EXISTS weather (
        timestamp TEXT,
        temp REAL,
        city TEXT
    );
    """

    cursor = conn.cursor()
    cursor.execute(create_sql)
    conn.commit()


def load_csv_to_sql(conn, csv_path):
    """Load CSV data into the SQLite weather table."""

    print(f"Loading data from {csv_path} into SQLite...")

    df = pd.read_csv(csv_path)

    # Display the first five rows
    print(df.head())

    # Append CSV rows to the weather table
    df.to_sql(
        "weather",
        conn,
        if_exists="append",
        index=False
    )

    print("Data loaded into the weather table.")


def quick_check(conn):
    """Check the number of rows and display the latest records."""

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM weather;")
    count = cursor.fetchone()[0]

    print(f"Rows in weather table: {count}")

    cursor.execute("""
        SELECT timestamp, temp, city
        FROM weather
        ORDER BY timestamp DESC
        LIMIT 5;
    """)

    rows = cursor.fetchall()

    print("Last 5 records:")

    for row in rows:
        print(row)


def main():
    print("Connecting to SQLite database...")

    conn = create_connection()

    try:
        create_table(conn)

        csv_path = get_latest_silver_file()

        load_csv_to_sql(conn, csv_path)

        quick_check(conn)

    finally:
        conn.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
