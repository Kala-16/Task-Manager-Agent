from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_ANON_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def add_task(title, description=None, due_at=None, priority="medium", status="pending", calendar_event_id=None):
    data = {
        "title": title,
        "description": description,
        "due_at": due_at,
        "priority": priority,
        "status": status,
        "calendar_event_id": calendar_event_id
    }
    return supabase.table("tasks").insert(data).execute()

def list_tasks(status=None):
    query = supabase.table("tasks").select("*").order("due_at", desc=False)
    if status:
        query = query.eq("status", status)
    return query.execute()

def set_status(task_id, status):
    return supabase.table("tasks").update({"status": status}).eq("id", task_id).execute()

def delete_task(task_id):
    return supabase.table("tasks").delete().eq("id", task_id).execute()

def update_calendar_event_id(task_id, event_id):
    return supabase.table("tasks").update({"calendar_event_id": event_id}).eq("id", task_id).execute()
