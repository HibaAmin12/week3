# Week 03 · Mon · Learn
## REST Fundamentals, the HTTP Lifecycle & Your First FastAPI Endpoint

### Learning objectives
By the end of today, you should be able to:
- Explain REST's actual constraints (resources, a fixed set of verbs, statelessness) and tell a genuinely RESTful API apart from "an API that happens to use HTTP."
- Walk through the full HTTP request/response lifecycle at a level useful for debugging — not just "the browser talks to the server."
- Choose the correct HTTP status code for a given outcome instead of defaulting to 200 for everything.
- Explain what API versioning is for, and compare URL-based versioning against the alternatives.
- Stand up a working FastAPI endpoint, and explain why its request handlers being `async def` isn't an accident.

### Lesson

**1. REST — what it actually constrains, not just "using HTTP"**
REST (Representational State Transfer) is an architectural *style*, not a protocol — HTTP is just the transport most REST APIs happen to use. Its real constraints: resources are identified by URLs that are **nouns**, not verbs (`/accounts/42`, never `/getAccount`); a small fixed set of HTTP methods map onto CRUD (`GET` = read, `POST` = create, `PUT`/`PATCH` = update, `DELETE` = delete) instead of every operation getting its own custom endpoint name; and the server is **stateless** — every request must carry everything needed to handle it, with no per-client session remembered between requests. A huge number of APIs calling themselves "REST" actually violate this constantly (`/getUserData`, `/user/update-email` as a `POST`) — that's RPC-over-HTTP wearing REST's name, not REST itself. Today's kata builds the real thing.

**2. The HTTP lifecycle — what actually happens between "send" and "response"**
A request doesn't teleport: the client resolves the server's domain to an IP (DNS), opens a connection (TCP handshake, plus a TLS handshake if it's HTTPS), then sends the actual HTTP request — a request line (method + path + HTTP version), headers (`Content-Type`, `Authorization`, etc.), and an optional body. The server processes it and sends back a response: a status line (the status code you'll cover next), response headers, and a body. Knowing these stages matters for debugging: "nothing loads" could be DNS, connectivity, or TLS; "I get a response but it's wrong" is a server-logic problem; "the server logged success but my client errored" is a client-side parsing problem — each stage points you at different tools.

**3. Status codes — communicating outcome precisely**
Five families: **2xx** success (`200 OK`, `201 Created` for a successful `POST`, `204 No Content` for a successful `DELETE` with nothing to return), **3xx** redirection, **4xx** client error (`400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity` for a well-formed request with invalid data), **5xx** server error (`500 Internal Server Error`). The anti-pattern worth naming directly: always returning `200 OK` with `{"error": "..."}` buried in the JSON body. This breaks every piece of HTTP-aware infrastructure that relies on the status code being honest — caches, retry logic, uptime monitors, even browser dev tools — because they all read the status line first and the body never.

**4. API versioning — because your API's shape will change and not every client upgrades at once**
The moment a real client depends on your API's current shape, changing that shape breaks them — versioning is the escape hatch. The most common strategy, and today's default, is **URL path versioning** (`/api/v1/accounts`) — simple to implement, trivial to test by hand, and immediately visible in every request. The alternatives: header-based versioning (`Accept: application/vnd.myapi.v1+json`) is arguably "more correct" REST (the URL identifies the resource, not the API generation) but harder to explore manually since it's invisible in the address bar; query-param versioning (`?version=1`) is simplest but easiest to forget and least favored in practice. Know the trade-off exists — today you're just implementing the common case.

**5. FastAPI — where this week's abstractions become a running server**
`@app.get("/accounts/{account_id}")` is the exact decorator shape from Week 1 Wednesday — a function that takes a function and changes what happens around it — except here it's registering a route instead of wrapping behavior. Two things about FastAPI specifically are not accidents:
- Its handlers are conventionally written `async def`. This is Week 2 Thursday's `asyncio` lesson, cashed in for real: while one request is `await`-ing a slow database call, FastAPI's event loop can start handling a second request on the same process instead of sitting idle. This is exactly the cooperative-concurrency mechanism you learned in the abstract three weeks ago.
- FastAPI reads your **type hints at runtime** to validate incoming request data and generate interactive docs automatically at `/docs`. Week 2 Wednesday's lesson was explicit that Python itself ignores type hints — FastAPI (via Pydantic underneath it) is the concrete example of a tool that doesn't. The hints you write aren't just documentation here; they're doing real, functional validation work.

### Resources
- [FastAPI — Tutorial: First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [MDN — An Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Overview)
- [MDN — HTTP Response Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
- [Real Python — What Are CRUD Operations?](https://realpython.com/crud-operations/)

### Kata set
1. **Hello, FastAPI.** `pip install fastapi uvicorn`, write a one-endpoint app (`GET /`), run it with `uvicorn main:app --reload`, and hit it from a browser and from `curl`.
2. **Design a resource, properly.** On paper or in comments (no code yet): design the URL scheme for a `Task` resource — list all, get one, create, update, delete — using only nouns and the correct HTTP verb per operation. No `/getTasks`, no `/createTask` anywhere.
3. **Build it, with real status codes.** Implement the five `Task` endpoints from Kata 2. Return `201` on create, `404` when a requested `id` doesn't exist, `204` on a successful delete. Let FastAPI's own Pydantic validation produce `422` on bad input — don't hand-roll that check yourself.
4. **Read a real request/response, annotated.** Run `curl -v` against one of your endpoints (or use your browser's Network tab). Annotate the output by hand: which part is the request line, which are headers, where's the status line, where's the body.
5. **Version it.** Mount your `Task` router under `/api/v1/tasks`. Write one sentence: if `v2` needed to rename a field without breaking existing `v1` clients, what would you actually do?
6. **Make the asyncio lesson concrete.** Write one endpoint as `async def` that does `await asyncio.sleep(2)` before responding — standing in for a slow database call. Fire two requests to it back-to-back (two terminal tabs, or a quick script) and confirm the second doesn't wait for the first to fully finish. This is Week 2 Thursday's lesson, now inside a real server.

### Today's tasks
- [ ] First FastAPI app running, hit via browser and `curl`
- [ ] `Task` resource URL scheme designed with correct nouns/verbs
- [ ] All five `Task` endpoints implemented with correct status codes (`201`, `404`, `204`, `422` via validation)
- [ ] One real request/response annotated by hand (request line, headers, status line, body)
- [ ] Router mounted under `/api/v1/`, one-sentence versioning-migration answer written
- [ ] `async def` endpoint kata done, concurrency confirmed with two overlapping requests

