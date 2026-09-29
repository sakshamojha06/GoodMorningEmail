import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "Database"
DATABASE_DIR.mkdir(exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "goodmorning.db"

connection = sqlite3.connect(DATABASE_PATH)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Topics
    (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL UNIQUE,
        IsActive INTEGER NOT NULL DEFAULT 1
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Contacts
    (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NUll,
        EMAIL TEXT NOT NULL,
        StartDate TEXT NOT NULL,
        IsActive INTEGER NOT NULL DEFAULT 1,
        TopicId INTEGER NOT NULL,

        FOREIGN KEY (TopicId)
            REFERENCES Topics(Id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS DailyFacts
    (
       Id INTEGER PRIMARY KEY AUTOINCREMENT,
       Topic TEXT NOT NULL,
       FactDate TEXT NOT NULL,
       Fact TEXT NOT NULL,
       CreatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

       UNIQUE(Topic, FactDate) 
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS EmailLogs
    (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        ContactId INTEGER NOT NULL,
        SentDate TEXT NOT NULL,
        SentAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FactId INTEGER,

        FOREIGN KEY (ContactId)
            REFERENCES Contacts(Id),

        FOREIGN KEY (FactId)
            REFERENCES DailyFacts(Id)

        UNIQUE(ContactId, SentDate)
    )
""")

connection.commit()
connection.close()

print("SQLite database created successfully!")
print(f"Database location: {DATABASE_PATH}")