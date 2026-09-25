import os

from dotenv import load_dotenv
from mssql_python import connect
from datetime import date, timedelta

load_dotenv()

connection_string = (
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "Encrypt=no;"
)

connection = connect(connection_string)

print("Database connection successfull!")

cursor = connection.cursor()

cursor.execute("""
    SELECT Id, Name, Email, StartDate, IsActive
    FROM Contacts
""")

rows = cursor.fetchall()
today = date.today()

for row in rows:
    contact_id = row[0]
    name = row[1]
    email = row[2]
    start_date = row[3]
    is_active = row[4]

    end_date = start_date + timedelta(days=2)

    cursor.execute("""
    SELECT COUNT(*)
    FROM EmailLogs
    WHERE ContactId = ?
    AND SendDate = ?
""", (contact_id, today))

    log_count = cursor.fetchone()[0]

    if is_active and start_date <= today <= end_date and log_count == 0:
        print(f"Send email to {name} - {email}")
    else:
        print(f"Do not send email to {name}")
    print(row)

cursor.close()
connection.close()