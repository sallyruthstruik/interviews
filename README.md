# Payment Processing API

A simplified payment processing backend built with Django and PostgreSQL.

## Quick Start

```bash
docker-compose up --build
```

The API will be available at **http://localhost:8080**.

Seed data (3 users, ~28 payments) is loaded automatically on first run.

## API Endpoints

### Create Payment

```
POST /api/payments/
Content-Type: application/json

{
  "user_id": 1,
  "amount": "49.99",
  "currency": "USD",
  "idempotency_key": "unique-request-id",
  "description": "Order #1234"
}
```

Returns the created (or existing) payment object.

### List Payments

```
GET /api/payments/list/
GET /api/payments/list/?status=success
GET /api/payments/list/?user=1
GET /api/payments/list/?currency=USD
```

Returns a paginated list of all payments.

---

## Interview Tasks

You have **60 minutes**. Work through the tasks in order. It's fine to not finish everything — we care about your approach more than completion.

### Task 1 — Fix Duplicate Payments

There is a bug: when two concurrent requests arrive with the same `idempotency_key`, duplicate payments are created.

**Reproduce:**

```bash
python scripts/simulate_race.py
```

You can also check the seed data — look for payments sharing the same `idempotency_key`.

**Your goal:** Make `idempotency_key` truly prevent duplicates, even under concurrent load.

### Task 2 — Make the Endpoint Safe Under Concurrency

The `POST /api/payments/` endpoint has no transaction handling. If the payment processing step fails partway through, the system can be left in an inconsistent state.

**Your goal:** Ensure the create-payment flow is atomic and handles concurrent access safely.

### Task 3 — Fix the N+1 Query Problem

The listing endpoint (`GET /api/payments/list/`) has a performance issue. As the number of payments grows, response time degrades badly.

**Your goal:** Identify and fix the N+1 query problem. Explain what was happening and why your fix works.

### Task 4 — Production Readiness (Discussion)

No code required. Briefly answer (a few sentences each):

1. How would you handle idempotency at scale (millions of requests/day)?
2. What monitoring/alerting would you add to this service?
3. How would you handle payment retries and state machine transitions?
4. What would you change if this needed to support multiple payment providers?

---

## Project Structure

```
├── config/              # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── payments/            # Main application
│   ├── models.py        # User, PaymentTransaction
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # Route config
│   └── management/      # Management commands
│       └── commands/
│           └── seed_payments.py
├── scripts/
│   └── simulate_race.py # Race condition demo
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Useful Commands

```bash
# Run the project
docker-compose up --build

# Open a Django shell inside the container
docker-compose exec web python manage.py shell

# Re-seed the database (drop and recreate)
docker-compose exec web python manage.py flush --noinput
docker-compose exec web python manage.py seed_payments

# Run the race condition demo (while server is up)
python scripts/simulate_race.py
```
