# Week 03 · Day 2 · Practice
## Auth, Secrets, SQL Fundamentals & Your First Security Bug

### Learning objectives
By the end of today, you should be able to:
- Explain the difference between *authentication* (who are you) and *authorization* (what are you allowed to do), and place API keys, JWT, OAuth, and RBAC correctly on that map.
- Guard a FastAPI endpoint with a simple API-key dependency, with the key loaded from an environment variable — never hardcoded.
- Hash a password with a purpose-built slow hash (bcrypt via `passlib`) instead of storing plaintext or using a fast general-purpose hash, and explain why the difference matters.
- Design a normalized relational schema for a real resource, and explain what a foreign key and an index each actually buy you.
- Write raw SQL directly against SQLite — `CREATE TABLE`, parameterized `INSERT`/`SELECT`/`UPDATE`/`DELETE` — and wrap a multi-statement write in a transaction.
- Reproduce a SQL-injection vulnerability yourself, then fix it — and explain exactly why the fix works.

### Lesson

**1. Authentication vs. authorization — and where today's tools each sit**
**Authentication** answers "who are you"; **authorization** answers "what are you allowed to do, now that I know." Conflating the two is the most common auth mistake. Today's four tools map onto that split differently:
- **API keys** — the simplest authentication mechanism: the client sends a static secret in a header (`X-API-Key`), the server checks it against a known value. No sessions, no expiry by default, and if the key leaks, everyone holding it is compromised at once. Good for server-to-server calls; today's kata implements this one for real.
- **JWT (JSON Web Token)** — a *signed* (not encrypted, by default) token containing claims about who the client is. The client authenticates once, the server issues a token, and every request after that carries it (`Authorization: Bearer <token>`) instead of re-checking a password each time — with no server-side session storage needed, since the signature alone proves it wasn't tampered with.
- **OAuth** — solves a different problem entirely: *delegation* ("let this app act on my behalf using my Google account, without ever handing it my password"), not a new way to prove identity from scratch. JWTs are commonly the token format OAuth issues underneath — OAuth is the handshake protocol, JWT is often the envelope.
- **RBAC (Role-Based Access Control)** — an *authorization* model: assign users roles (`admin`, `editor`, `viewer`) and check the role instead of hand-maintaining a permissions list per user, or worse, a single `is_admin` boolean that can't express "editor" once a third tier shows up.
Today you *implement* API-key auth and *understand* JWT/OAuth/RBAC precisely enough to reason about them — hand-rolling JWT signing correctly is its own rabbit hole, not today's kata.

**2. Password hashing & secrets management**
A password is never stored in plaintext, and it's never hashed with a *fast* general-purpose hash like MD5 or plain SHA-256 either — fast is exactly the wrong property for a password hash, because it's what makes brute-forcing billions of guesses per second feasible on stolen hashes. `bcrypt` (via `passlib`) and `argon2` are deliberately slow, tunable, and salt automatically, which is why they're the actual standard. Hashing is one-way by design: you never "unhash" a password to check it, you hash the login attempt again and compare the two hashes. This connects directly to the program rule already in force since this week: **no credentials in code, ever** — your API key, DB password, and any signing secret all belong in environment variables (`os.environ`, `.env` + `python-dotenv` locally), never committed to source, git history included.

**3. SQL fundamentals — schema design & normalization**
Monday's `Task` lived in a Python list that vanished every time the server restarted. Today it moves into a real table: `CREATE TABLE tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, done BOOLEAN NOT NULL DEFAULT 0, created_at TEXT NOT NULL)`. **Normalization**, in plain terms: one fact per column, no repeating groups crammed into a single field (a comma-separated `tags` column is the classic violation — that becomes its own `tags` table, related back to `tasks` by a **foreign key**), and every non-key column should depend on the whole primary key, not just part of it. You're not memorizing 1NF/2NF/3NF by name today — you're internalizing the instinct: if you're about to split a value with `.split(",")` after reading it back out of a column, that value shouldn't have been one column.

**4. Indexes & transactions**
An **index** is a lookup structure the database maintains so it doesn't have to scan every row to satisfy a `WHERE` clause — the primary key is indexed automatically; anything else you filter or join on frequently is a candidate for `CREATE INDEX`. The cost isn't free: every index speeds up reads but slows down writes (the index itself has to be updated) and takes storage — not "always add more indexes." A **transaction** (`BEGIN` / `COMMIT` / `ROLLBACK`) bundles multiple SQL statements into one all-or-nothing unit. This matters the moment one *logical* operation is actually several SQL statements — if the second statement fails or the process crashes between them, a transaction guarantees you're left with either both changes or neither, never a half-applied mess.

**5. OWASP — SQL injection, hands-on; XSS/CSRF, by name**
**SQL injection**: building a query by concatenating untrusted input directly into the SQL string lets an attacker supply *SQL*, not just data — `f"SELECT * FROM tasks WHERE title = '{title}'"` with `title = "'; DROP TABLE tasks; --"` is the textbook example, and today's kata reproduces exactly this against a throwaway copy of your database so it stops being abstract. The fix is **parameterized queries** — `cursor.execute("SELECT * FROM tasks WHERE title = ?", (title,))` — where the driver treats the placeholder's value strictly as data and never as code, no matter what's inside it. **XSS** (a malicious script running in another user's browser) and **CSRF** (tricking a logged-in user's browser into firing a request they never intended) matter most once a frontend with cookies/sessions is in the picture — you'll meet both directly in Week 4; today, know the names and the one-sentence threat each describes.

**6. Wiring it together — Monday's API, now for real**
Take the five `Task` endpoints from Monday and: swap the in-memory list for real parameterized reads/writes against the SQLite `tasks` table (same status codes — `201`/`404`/`204`/`422` — don't regress those); add an API-key `Depends()` guard on the write endpoints (`POST`/`PUT`/`DELETE`), with the key read from an environment variable. Two weeks' worth of `Depends`-shaped thinking (Monday's decorator lineage, Week 2's "don't repeat what's already correct") converges here: a dependency is just a function FastAPI calls before your handler, the same "wrap behavior around a function" idea, now checking a header instead of timing a block.

### Resources
- [FastAPI — Security: First Steps](https://fastapi.tiangolo.com/tutorial/security/first-steps/)
- [FastAPI — OAuth2 with Password (and hashing), Bearer with JWT tokens](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Real Python — Data Management With Python, SQLite, and SQLAlchemy](https://realpython.com/python-sqlite-sqlalchemy/)
- [SQLite docs — Transactions](https://www.sqlite.org/lang_transaction.html)
- [OWASP Cheat Sheet — SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Cheat Sheet — Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [passlib — Quickstart](https://passlib.readthedocs.io/en/stable/narr/quickstart.html)

### Kata set
1. **Warm-up.** Get Monday's `Task` app running again from memory — no notes if you can manage it.
2. **Schema + raw SQL, no FastAPI yet.** Create `tasks.db`. Write the `CREATE TABLE tasks (...)` statement by hand. Using the `sqlite3` module directly in a script or REPL, insert three rows, then run one `SELECT`, one `UPDATE`, and one `DELETE` — all with `?` placeholders, none with string formatting.
3. **Break it, then fix it.** Against a throwaway copy of your database, write the naive f-string version of a `SELECT` that takes user-supplied `title` and interpolates it directly into the query. Feed it `"; DROP TABLE tasks; --` as the "title" and watch it happen. Now rewrite the same query using a parameterized placeholder and confirm that exact same input just gets stored/searched as a harmless literal string.
4. **Wire the API to the database.** Replace the in-memory list in Monday's five endpoints with real parameterized reads/writes to `tasks`. Re-run Monday's `curl` checks and confirm the same status codes still come back — plus confirm state now survives a server restart.
5. **Guard it with an API key.** Add a FastAPI dependency that checks an `X-API-Key` header against a value loaded from an environment variable (not a string literal in `main.py`). Apply it to `POST`, `PUT`, and `DELETE`; return `401` on a missing or wrong key. Confirm `GET` still works unauthenticated, on purpose.
6. **Hash a password, properly.** In a small standalone script (no need to wire this into the Task API), take a plaintext password, hash it with `passlib`'s bcrypt handler, then verify one correct and one incorrect attempt against that hash. Never print or log the plaintext once it's hashed.
7. **Transactions, proven with a deliberate failure.** Add a second table, `task_audit_log`. Wrap "mark a task done" + "insert an audit-log row" in a single transaction. Deliberately raise an exception between the two statements and confirm — by querying afterward — that *neither* change persisted.
8. **Concept check, one sentence each, out loud.** API key vs. JWT: what's actually different? OAuth: what problem does it solve that isn't "prove who you are from scratch"? RBAC: what does it let you express that a single `is_admin` boolean can't?

### Today's tasks
- [ ] Monday's `Task` app running again, confirmed from memory
- [ ] `tasks` table created; three rows inserted, one `SELECT`/`UPDATE`/`DELETE` run via raw parameterized SQL
- [ ] SQL-injection kata done — attack reproduced, then neutralized with parameterized queries
- [ ] All five endpoints wired to the real database; same status codes confirmed; state survives a restart
- [ ] API-key dependency guarding `POST`/`PUT`/`DELETE`, key loaded from an environment variable, `401` confirmed on a bad key
- [ ] Password hashed and verified via `passlib`/bcrypt, correct and incorrect attempts both checked
- [ ] Transaction kata done — deliberate mid-transaction failure confirmed to roll back both statements
- [ ] API key vs. JWT vs. OAuth vs. RBAC — one sentence each, stated out loud


