# Architecture Diagram Description

1. Client (Browser)
   - Interacts with Streamlit UI.

2. Streamlit App (app.py)
   - Handles user input and displays tasks.
   - Calls Agent modules.

3. Agent Modules
   - parser.py
     - Sends user text to GPT (OpenAI).
     - Returns structured JSON: title, description, due_text, priority.
     - Resolves due_text to datetime using dateparser.
   - db.py
     - CRUD operations to Supabase `tasks` table.
   - calendar.py
     - Creates/Deletes events via Google Calendar API.

4. Data Stores
   - Supabase (Postgres): task records (title, due_at, status, priority, calendar_event_id).

5. External Services
   - OpenAI: language parsing.
   - Google Calendar: reminders.

Flow:
Browser → Streamlit → parser(GPT) → db(Supabase)
                         ↘ calendar(Google) → event_id → db
