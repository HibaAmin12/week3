import sqlite3


connection = sqlite3.connect("tasks.db")

cursor = connection.cursor()


try:

    # 1. Mark task done
    cursor.execute(
        """
        UPDATE tasks
        SET done = ?
        WHERE id = ?
        """,
        (True, 1)
    )


    # Deliberate error (testing rollback)
    raise Exception("Something failed")


    # 2. Insert audit log
    cursor.execute(
        """
        INSERT INTO task_audit_log(
            task_id,
            action,
            created_at
        )
        VALUES (?, ?, ?)
        """,
        (1, "Task completed", "2026-07-31")
    )


    connection.commit()

    print("Transaction successful")


except Exception as e:

    connection.rollback()

    print("Transaction failed:", e)


finally:

    connection.close()