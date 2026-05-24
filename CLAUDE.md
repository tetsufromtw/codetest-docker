# Claude Code Instructions

## Coding Rules

* Read `README.md` first.
* Do not modify `main_test.go`.
* Do not modify the test behavior.
* Do not modify `db/init.sql` unless explicitly instructed.
* Do not refactor unrelated files.
* Do not rename existing files unless necessary.
* Do not add unnecessary architecture or abstractions.
* Use the existing MySQL schema under `db/`.
* Keep the implementation simple and readable.
* Write code comments in English only.

## Tech Stack

* Python
* FastAPI
* uv
* MySQL
* Docker Compose

The application must listen on port `8888`.

## Required Behavior

Implement only the behavior required by the tests.

* `POST /transactions`
* Return `201 Created` when a transaction is registered.
* Return `402 Payment Required` when the user's total transaction amount would exceed `1000`.
* The tests send requests concurrently, so the amount check and insert must be safe under concurrent requests.

## Code Organization

Use a lightweight structure.

Preferred files:

* `app/main.py`: FastAPI routes and HTTP response handling
* `app/schemas.py`: Pydantic request / response models
* `app/db.py`: database connection helper
* `app/transaction_service.py`: transaction registration logic

Do not put all business logic directly inside route handlers.
