import streamlit as st
from datetime import datetime, timedelta
import pytz

from agent.parser import parse_command, resolve_due_datetime
from agent.db import add_task, list_tasks, set_status, delete_task, update_calendar_event_id
from agent.calendar import create_event, delete_event

st.set_page_config(page_title="Task Manager Agent", page_icon="✅", layout="centered")

st.title("Task Manager Agent")
st.caption("Add tasks in natural language, store them, and auto-create calendar reminders.")

# Add Task Section
st.subheader("Add a task")
user_text = st.text_input("Describe your task", placeholder="e.g., Remind me to submit the monthly report next Friday at 10am, high priority")

col1, col2 = st.columns([1,1])
with col1:
    tz_name = st.selectbox("Timezone", ["Asia/Kolkata", "UTC", "US/Pacific"], index=0)
with col2:
    create_calendar_event = st.checkbox("Create Google Calendar reminder", value=True)

if st.button("Add Task", type="primary"):
    if not user_text.strip():
        st.warning("Please enter a task description.")
    else:
        parsed = parse_command(user_text)
        due_dt = resolve_due_datetime(parsed.get("due_text"))
        if due_dt:
            tz = pytz.timezone(tz_name)
            due_dt = tz.localize(due_dt) if due_dt.tzinfo is None else due_dt.astimezone(tz)
        event_id = None
        if create_calendar_event and due_dt:
            try:
                event_id = create_event(parsed["title"], parsed.get("description"), due_dt)
                st.success("Calendar event created.")
            except Exception as e:
                st.error(f"Calendar error: {e}")
        try:
            add_task(
                title=parsed["title"],
                description=parsed.get("description"),
                due_at=due_dt.isoformat() if due_dt else None,
                priority=parsed.get("priority", "medium"),
                status="pending",
                calendar_event_id=event_id
            )
            st.success("Task added.")
        except Exception as e:
            st.error(f"Database error: {e}")

st.divider()

# Task List
st.subheader("Your tasks")
filter_status = st.selectbox("Filter", ["all", "pending", "done"], index=0)

try:
    if filter_status == "all":
        res = list_tasks()
    else:
        res = list_tasks(status=filter_status)
    tasks = res.data or []
except Exception as e:
    st.error(f"Failed to load tasks: {e}")
    tasks = []

def task_row(t):
    due_str = t.get("due_at")
    priority = t.get("priority", "medium")
    status = t.get("status", "pending")
    st.write(f"• {t['title']}  —  Priority: {priority}  —  Status: {status}")
    if due_str:
        st.caption(f"Due: {due_str}")
    if t.get("description"):
        st.caption(f"Details: {t['description']}")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        if st.button("Mark done", key=f"done-{t['id']}"):
            try:
                set_status(t["id"], "done")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    with c2:
        if st.button("Delete", key=f"del-{t['id']}"):
            try:
                if t.get("calendar_event_id"):
                    try:
                        delete_event(t["calendar_event_id"])
                    except Exception:
                        pass
                delete_task(t["id"])
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    with c3:
        if st.button("Pending", key=f"pend-{t['id']}"):
            try:
                set_status(t["id"], "pending")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    st.divider()

if tasks:
    for t in tasks:
        task_row(t)
else:
    st.info("No tasks yet. Add one above!")

st.subheader("About")
st.markdown("- Natural language parsing using GPT\n- Stores tasks in Supabase\n- Optional Google Calendar reminders\n- Timezone-aware due dates")
