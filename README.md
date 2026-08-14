# Mahanaayak OS - Backend

Phase 1 backend architecture using Flask and Clean Architecture principles.

## Prerequisites
- Python 3.12+
- PostgreSQL (for production via Turso/etc)
- SQLite (built-in for development)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Mahanaayak_OS
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy `.env.example` to `.env` and update the values for your database connection.
   ```bash
   cp .env.example .env
   ```

5. **Initialize Database Migrations:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
   *(This will automatically create `mahanaayak.db` in the root folder).*

6. **Run the Server:**
   ```bash
   python run.py
   ```

The application will be running at `http://127.0.0.1:5000/`.
Health Check endpoint: `GET /api/v1/health`
