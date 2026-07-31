import sqlite3

# Database connection
connection = sqlite3.connect("tasks.db")

# Cursor for executing SQL commands
cursor = connection.cursor()


##Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
)
""")


# Insert 3 tasks
tasks = [
    ("Learn FastAPI", False, "2026-07-31"),
    ("Practice SQL", True, "2026-07-31"),
    ("Build API", False, "2026-07-31")
]

cursor.executemany(
    """
    INSERT INTO tasks (title, done, created_at)
    VALUES (?, ?, ?)
    """,
    tasks
)
cursor.execute(
    """
    UPDATE tasks
    SET done = ?
    WHERE id = ?
    """,
    (True, 1)
)

cursor.execute(
    """
    DELETE FROM tasks
    WHERE id = ?
    """,
    (1,)
)

connection.commit()

print("Task deleted")




# Read data
cursor.execute("SELECT * FROM tasks")

rows = cursor.fetchall()

print("All Tasks:")
for row in rows:
    print(row)


# Close connection
connection.close()


import sqlite3


def get_connection():
    connection = sqlite3.connect("tasks.db")
    return connection


def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    connection.commit()
    connection.close()


create_table()

##TRANSACTION+ ROLLBACK
import sqlite3


def get_connection():
    return sqlite3.connect("tasks.db")


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    # Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL DEFAULT 0,
        created_at TEXT NOT NULL
    )
    """)

    # Audit log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS task_audit_log (
        id INTEGER PRIMARY KEY,
        task_id INTEGER,
        action TEXT,
        created_at TEXT
    )
    """)

    connection.commit()
    connection.close()


create_tables()