import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from mssql_python import connect


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR/ "database" / "goodmorning.db"


sqlite_connection = sqlite3.connect(DATABASE_PATH)
sqlite_connection.execute("PRAGMA foreign_keys = ON")

sqlite_cursor = sqlite_connection.cursor()


connection_string = (
    f"Server={os.getenv('DB_SERVER')};"
    f"Database={os.getenv('DB_NAME')};"
    f"UID={os.getenv('DB_USER')};"
    f"PWD={os.getenv('DB_PASSWORD')};"
    "Encrypt=no;"
)

sql_connection = connect(connection_string)
sql_cursor = sql_connection.cursor()

print("SQL Server connected successfully!")
print("SQLite connected successfully!")


print("\nMigrating Topics...")

sql_cursor.execute("""
    SELECT Id, Name, IsActive
    FROM Topics
    ORDER BY Id
""")

topics = sql_cursor.fetchall()

for row in topics:
    topic_id = row[0]
    name = row[1]
    is_active = row[2]

    sqlite_cursor.execute("""
        INSERT INTO Topics
        (
            Id, Name, IsActive
        )
        VALUES (?, ?, ?)
    """, (topic_id, name, int(is_active)       
    ))

print(f"Topics migrated: {len(topics)}")


print("\nMigrating DailyFacts...")

sql_cursor.execute("""
    SELECT Id, Topic, FactDate, Fact, CreatedAt
    FROM DailyFacts
    ORDER BY Id
""")

daily_facts = sql_cursor.fetchall()

for row in daily_facts:
    fact_id = row[0]
    topic = row[1]
    fact_date = row[2]
    fact = row[3]
    created_at = row[4]

    if hasattr(fact_date, "isoformat"):
        fact_date = fact_date.isoformat()
    if hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()

    sqlite_cursor.execute("""
        INSERT INTO DailyFacts
        (
            Id, Topic, FactDate, Fact, CreatedAt
        )
        VALUES (?, ?, ?, ?, ?)
""", (fact_id, topic, fact_date, fact, created_at))

print(f"DailyFacts migrated: {len(daily_facts)}")


print("\nMigrating Contacts...")

sql_cursor.execute("""
    SELECT Id, Name, Email, StartDate, IsActive, TopicId
    FROM Contacts
    ORDER BY Id
""")

contacts = sql_cursor.fetchall()

for row in contacts:
    contact_id = row[0]
    name = row[1]
    email = row[2]
    start_date = row[3]
    is_active = row[4]
    topic_id = row[5]

    if hasattr(start_date, "isoformat"):
        start_date = start_date.isoformat()

    sqlite_cursor.execute("""
        INSERT INTO Contacts
        (
            Id, Name, Email, StartDate, IsActive, TopicId
        )
        VALUES (?, ?, ?, ?, ?, ?)
""", (contact_id, name, email, start_date, is_active, topic_id))

print(f"Contact migrated: {len(contacts)}")


print("\nMigrating EmailLogs...")

sql_cursor.execute("""
    SELECT Id, ContactId, SentDate, SentAt, FactId
    FROM EmailLogs
    ORDER by Id
""")

email_logs = sql_cursor.fetchall()

for row in email_logs:
    log_id = row[0]
    contact_id = row[1]
    sent_date = row[2]
    sent_at = row[3]
    fact_id = row[4]

    if hasattr(sent_date, "isoformat"):
        sent_date = sent_date.isoformat()
    if hasattr(sent_at, "isoformat"):
        sent_at = sent_at.isoformat()

    sqlite_cursor.execute("""
        INSERT INTO EmailLogs
        (
            Id, ContactId, SentDate, SentAt, FactId
        )
        VALUES (?, ?, ?, ?, ?)
""", (log_id, contact_id, sent_date, sent_at, fact_id))

print(f"EmailLogs migrated: {len(email_logs)}")


sqlite_connection.commit()

print("\n=======================================")
print("Migration completed successfully!")
print("=========================================")


sql_cursor.close()
sql_connection.close()

sqlite_cursor.close()
sqlite_connection.close()