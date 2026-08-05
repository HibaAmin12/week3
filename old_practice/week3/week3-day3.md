# Week 03 · Day 3 · Build
## The ORM Layer — SQLAlchemy Models, Relationships & Alembic Migrations

### Learning objectives
By the end of today, you should be able to:
- Explain what an ORM actually does (maps classes to tables, instances to rows) and why it doesn't replace knowing raw SQL, just shortens the common case.
- Define SQLAlchemy declarative models, including a real foreign-key relationship between two tables.
- Wire FastAPI endpoints to a SQLAlchemy session via a `Depends()`-based dependency, preserving yesterday's status codes.
- Explain what Alembic actually solves (versioned, repeatable schema change across environments) and why "just editing the table by hand" stops working once real data and other people are involved.
- Generate, apply, and reverse a real migration.

### Lesson

**1. What an ORM actually buys you — and doesn't**
An ORM (Object-Relational Mapper) maps a Python class to a table, an instance to a row, and attribute access to column values. `select(Task).where(Task.id == 3)` compiles down to essentially the same parameterized SQL you wrote by hand yesterday — the ORM isn't magic, it's generating the same kind of query you already know how to write, using the same parameter-binding mechanism, which is why it's just as injection-safe as your hand-written version. What it buys you: far less boilerplate for the common case, and objects you can pass around your codebase instead of raw tuples/dicts. What it doesn't buy you: an excuse to stop understanding SQL — debugging a slow ORM query eventually means reading the SQL it actually generated, and some things (complex reporting queries, bulk operations) are still clearer written by hand. Yesterday came first on purpose.

**2. Declarative models — the class *is* the schema**
```python
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    done = Column(Boolean, default=False)
```
Compare this directly to yesterday's hand-written `CREATE TABLE tasks (...)` — same information, generated instead of typed by hand. This is Week 1's dataclass lesson, echoing a third time: a class whose real job is describing a data shape, with a base class doing extra work behind the scenes (there, `__init__`/`__repr__`/`__eq__`; here, a full table mapping) — except this time what's generated isn't just Python behavior, it's the actual database schema.

**3. Relationships — foreign keys, without writing the JOIN by hand**
Add a second model, `Category`, and connect it to `Task` with a real foreign key: `category_id = Column(Integer, ForeignKey("categories.id"))` plus `relationship("Category")` on the `Task` side. Once that's wired up, `task.category.name` reads across the join without you writing `JOIN` anywhere — SQLAlchemy generates it. This isn't a black box: run with `create_engine(..., echo=True)` once and watch the actual SQL scroll by for a query you wrote as plain attribute access. Yesterday's foreign-key concept just became something you use instead of something you know the name of.

**4. Sessions — the ORM's version of a connection and a transaction**
A `Session` wraps a database connection and tracks pending changes: `session.add(obj)` stages a change, `session.commit()` writes it, `session.rollback()` undoes it — this is yesterday's transaction guarantee (`BEGIN`/`COMMIT`/`ROLLBACK`), now managed by an object instead of hand-typed SQL. The FastAPI-idiomatic pattern is a `get_db()` dependency that yields a session for the lifetime of one request and closes it afterward — the exact same `Depends()` shape as yesterday's auth guard, except this dependency's job is setup/teardown around a resource instead of a pass/fail check.

**5. Alembic — versioned schema change, not hand-editing tables**
The problem Alembic solves: once a table has real data in it, you can't just drop and redefine it, and every other environment — a teammate's laptop, staging, production — needs the *exact same* change applied, in the *exact same order*, exactly once. Hand-editing tables works until there's a second environment or a second person; then it stops working immediately and silently. Alembic's workflow: `alembic init` sets up a migrations folder; `alembic revision --autogenerate -m "add priority to tasks"` compares your current models against the actual database and writes the difference as a migration script; `alembic upgrade head` applies every migration that hasn't run yet. Every migration script has both an `upgrade()` and a `downgrade()` — the second is what lets you undo a bad migration on command instead of restoring from a backup.

### Resources
- [SQLAlchemy — ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Alembic — Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Alembic — Auto Generating Migrations](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)

### Build tasks today
Today is independent build time — apply this directly on top of yesterday's `Task` API and database, not a disconnected exercise:

1. **Warm-up.** Get yesterday's `Task` API (raw SQL, API-key-guarded writes) running again from memory.
2. **Define the models.** Write a declarative `Task` model matching yesterday's hand-written table exactly — same columns, same constraints. Add a `Category` model with a `ForeignKey`/`relationship()` connecting it to `Task`.
3. **Wire the endpoints to SQLAlchemy.** Replace the raw `sqlite3` calls in all five endpoints with a `get_db()` session dependency. Re-run yesterday's `curl` checks and confirm the exact same status codes still come back.
4. **Prove the relationship works.** Create a `Category`, create a `Task` pointing at it, then read `task.category.name` without writing a `JOIN`. Turn on `echo=True` for one request and read the SQL SQLAlchemy actually generated.
5. **Set up Alembic.** `alembic init`, point it at your existing database, and generate + apply an initial migration from your current models.
6. **A real schema change, both directions.** Add a `priority` column to the `Task` model. Autogenerate a migration for just that change, apply it with `alembic upgrade head`, confirm the column exists, then run `alembic downgrade -1` and confirm it's gone again.

## Target deliverable
API + auth prototype, DB schema, SQL assignment, Dockerfile, PR history — today's work (ORM models, a real relationship, and a working migration history) is the DB-schema half of that deliverable.


