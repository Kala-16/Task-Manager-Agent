# Task Manager Agent

A GPT-powered Task Manager that parses natural language commands into structured tasks, stores them in Supabase, and optionally creates Google Calendar reminders. Built for a 48-hour AI Agent challenge.

## Overview
- Add tasks via natural language (e.g., "Submit report next Friday 10am, high priority").
- Tasks are saved with title, description, due datetime, priority, and status.
- Optional Google Calendar reminders for due dates.
- Simple Streamlit UI to view, complete, and delete tasks.

## Features
- Natural Language → Structured Task parsing
- Task CRUD (create, list, mark done/pending, delete)
- Google Calendar event creation
- Timezone handling
- Minimal, deployable UI

## Limitations
- Parsing quality depends on the model; edge cases may need manual adjustment.
- Service Account works best for shared calendars; for personal calendars use OAuth flow.
- No user authentication (can be added via Supabase Auth).
- Basic priority and status only (no subtasks or recurrence by default).

## Tech stack
- Streamlit (UI)
- OpenAI (GPT for parsing)
- LangChain (prompt orchestration)
- Supabase (database)
- Google Calendar API (reminders)
- dateparser, pytz (time handling)

## Setup & run
1. Create `.env`:
