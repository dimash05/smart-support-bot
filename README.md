smart-support-bot

A small support system built around a Telegram bot and a FastAPI admin backend. The bot lets users browse FAQ entries, create support tickets, and check their own requests. The admin API gives a simple interface for managing users, tickets, and FAQ content.

Project overview
smart-support-bot has two entry points:
• Telegram bot for end users
• FastAPI admin API for support or admin tasks
The main idea is straightforward: a user opens the bot, reads FAQ entries or creates a support request, the ticket is stored in PostgreSQL, and an admin reviews tickets and updates statuses through API endpoints.
Stack
• Python 3.12
• aiogram
• FastAPI
• PostgreSQL
• SQLAlchemy
• Alembic
• Pydantic
• Docker / Docker Compose
Features
Telegram bot
• /start
• /help
• /faq
• /new_ticket
• /my_tickets
• /cancel during ticket creation flow
Ticket flow
• Create a ticket with category, title, and description
• Track ticket status as open, in_progress, resolved, or closed
Admin API
• View users
• View tickets
• Update ticket status
• Create FAQ entries
• Edit FAQ entries
Technical notes
• Environment-based config
• Async SQLAlchemy session
• Service layer
• Basic logging
• Basic error handling
• Alembic migrations
• Dockerized PostgreSQL and API setup
Architecture
The project uses a simple layered structure.
Folder Responsibility
app/bot Telegram bot handlers, routers, FSM states, and keyboards.
app/api FastAPI routes, dependencies, and API error handlers.
app/services Business logic. Handlers and routes stay thin and call service classes.
app/models SQLAlchemy ORM models: User, Ticket, FAQEntry.
app/schemas Pydantic schemas for request validation and API responses.
app/db Database base class, session setup, model registration, and local DB init script.
app/config Settings and logging configuration.
app/utils Shared enums and small helpers.
Project structure
app/
├── api/
│ ├── routes/
│ ├── dependencies.py
│ ├── errors.py
│ └── router.py
├── bot/
│ ├── handlers/
│ ├── keyboards/
│ ├── states/
│ └── router.py
├── config/
│ ├── logging.py
│ └── settings.py
├── db/
│ ├── base.py
│ ├── models.py
│ ├── session.py
│ └── init_db.py
├── models/
├── schemas/
├── services/
├── utils/
├── api_main.py
└── bot_main.py

alembic/
tests/
Dockerfile
docker-compose.yml
alembic.ini
README.md
How the bot works
/start
Registers or updates the Telegram user in the database and shows the main keyboard.
/faq
Loads published FAQ entries from the database and sends them as a message.
/new_ticket
Starts an FSM-based flow.

1. Ask for category
2. Ask for title
3. Ask for description
4. Save the ticket to PostgreSQL
   /my_tickets
   Shows all tickets created by the current user.
   /cancel
   Stops the active ticket creation flow.
   API endpoints
   Health
   • GET /api/v1/health
   Users
   • GET /api/v1/users
   Tickets
   • GET /api/v1/tickets
   • PATCH /api/v1/tickets/{ticket_id}/status
   Example request body:
   {
   "status": "in_progress"
   }
   FAQ
   • GET /api/v1/faq
   • POST /api/v1/faq
   • PATCH /api/v1/faq/{faq_id}
   Example create body:
   {
   "question": "How long does support response take?",
   "answer": "Usually within one business day.",
   "is_published": true
   }
   Environment variables
   Example values are provided in .env.example.
   • APP_HOST
   • APP_PORT
   • API_PREFIX
   • BOT_TOKEN
   • DB_HOST
   • DB_PORT
   • DB_NAME
   • DB_USER
   • DB_PASSWORD
   • DATABASE_URL
   • LOG_LEVEL
   Example:
   APP_HOST=0.0.0.0
   APP_PORT=8000
   API_PREFIX=/api/v1

BOT_TOKEN=your_telegram_bot_token_here

DB_HOST=localhost
DB_PORT=5432
DB_NAME=smart_support_bot
DB_USER=postgres
DB_PASSWORD=postgres
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/smart_support_bot

LOG_LEVEL=INFO
Local setup 5. Clone the repository. 6. Create and activate a virtual environment. 7. Install dependencies. 8. Copy .env.example to .env and update values. 9. Create a PostgreSQL database named smart_support_bot. 10. Apply migrations with alembic upgrade head. 11. Run the API with uvicorn app.api_main:app --reload. 12. Run the bot with python -m app.bot_main.
Docker setup
A Docker-based setup was added for PostgreSQL and API startup.
Main command:
docker compose up --build -d
The API container runs two steps on startup: first alembic upgrade head, then uvicorn app.api_main:app --host 0.0.0.0 --port 8080.
In this project, the Docker environment was tested inside an Ubuntu virtual machine rather than directly on Windows. VirtualBox NAT port forwarding was used to expose the API from the guest machine.
Example bot workflow 13. Open the bot in Telegram. 14. Send /start. 15. Send /new_ticket. 16. Enter a category, for example Billing. 17. Enter a title, for example Payment was charged twice. 18. Enter a short description of the issue. 19. Receive the created ticket ID and status. 20. Use /my_tickets to check existing requests. 21. Use /faq to read published FAQ entries.
Logging and error handling
• Basic application logging is configured through the standard logging module.
• Database write operations use commit and rollback.
• FastAPI has centralized exception handlers for HTTPException, SQLAlchemyError, and unexpected exceptions.
Future improvements
• Add authentication for the admin API
• Let admins send responses back to users through the bot
• Add pagination and filtering for ticket lists
• Replace free-text category input with inline buttons
• Add automated tests for services and API routes
• Split Docker setup into dedicated services for API and bot
• Add CI checks
Why this project was built this way
The goal was not to imitate a huge enterprise system. The idea was to build something small but believable: clear folder structure, realistic bot flow, reusable services, PostgreSQL instead of a fake in-memory store, and API and bot sharing the same business layer.
Status
• Bot flow implemented
• Ticket creation implemented
• Admin API implemented
• PostgreSQL models and migrations implemented
• Docker setup added
• README finalized
