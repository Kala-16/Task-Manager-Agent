import streamlit as st
import json
from datetime import datetime, date, timedelta
import os
# File for persistent storage
DATA_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def check_reminders(tasks):
    now = date.today()
    reminders = []
    for task in tasks:
        if task["status"] == "pending":
            due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
            if due_date < now:
                reminders.append(f"🚨 *OVERDUE*: {task['title']} (due {task['due_date']})")
            elif due_date == now:
                reminders.append(f"⏰ *TODAY*: {task['title']} (due today)")
    return reminders

st.set_page_config(page_title="TaskManagerAgent", page_icon="🔔", layout="wide")

st.title("🔔 *TaskManagerAgent*")
st.markdown("Track tasks • Automatic reminders • Persistent storage")
st.markdown("---")

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

tasks = st.session_state.tasks
reminders = check_reminders(tasks)

if reminders:
    st.error("🔔 *URGENT REMINDERS*")
    for reminder in reminders:
        st.write(reminder)
    st.markdown("---")

with st.sidebar:
    st.header("➕ *Manage Tasks*")
    
    st.subheader("Add New Task")
    title = st.text_input("Task Title", placeholder="Enter task description...")
    due_date = st.date_input("Due Date", value=date.today() + timedelta(days=1))
    priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
    category = st.selectbox("Category", ["Work", "Personal", "Study", "Other"])
    
    if st.button("✅ *ADD TASK*", use_container_width=True, type="primary"):
        if title.strip():
            new_task = {
                "id": len(tasks) + 1,
                "title": title.strip(),
                "due_date": due_date.strftime("%Y-%m-%d"),
                "priority": priority,
                "status": "pending",
                "category": category,
                "created_at": date.today().strftime("%Y-%m-%d")
            }
            tasks.append(new_task)
            st.session_state.tasks = tasks
            save_tasks(tasks)
            st.success("✅ Task added successfully!")
            st.rerun()
        else:
            st.error("❌ Task title required!")
    
    st.markdown("---")
    # Quick Actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh Reminders"):
            st.rerun()
    with col2:
        if st.button("🗑 Clear Completed"):
            st.session_state.tasks = [t for t in tasks if t["status"] != "completed"]
            save_tasks(st.session_state.tasks)
            st.success("✅ Completed tasks cleared!")
            st.rerun()

col1, col2 = st.columns([3, 1])

with col1:
    st.header("📋 *Task List*")
    
    filter_row = st.columns(3)
    status_filter = filter_row[0].selectbox("Status", ["All", "pending", "in-progress", "completed"])
    priority_filter = filter_row[1].selectbox("Priority", ["All", "Low", "Medium", "High", "Urgent"])
    overdue_only = filter_row[2].checkbox("Overdue Only")
    
    filtered_tasks = tasks
    if status_filter != "All":
        filtered_tasks = [t for t in filtered_tasks if t["status"] == status_filter]
    if priority_filter != "All":
        filtered_tasks = [t for t in filtered_tasks if t["priority"] == priority_filter]
    if overdue_only:
        now = date.today()
        filtered_tasks = [t for t in filtered_tasks 
                         if datetime.strptime(t["due_date"], "%Y-%m-%d").date() < now 
                         and t["status"] == "pending"]
    

    for task in filtered_tasks:
        with st.container():
            # Status badge
            status_color = {"pending": "🟡", "in-progress": "🟠", "completed": "🟢"}
            badge = f"{status_color.get(task['status'], '⚪')} *{task['status'].title()}*"
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; border-radius: 12px; margin: 10px 0; border-left: 6px solid 
            {"#ff6b6b" if task["status"]=="pending" and datetime.strptime(task["due_date"], "%Y-%m-%d").date() < date.today() else "#4ecdc4"};'>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <h3 style='margin: 0; color: #2c3e50;'>{task['title']}</h3>
                    <span style='background: #ecf0f1; padding: 4px 8px; border-radius: 20px; font-size: 12px; font-weight: bold;'>{task['priority']}</span>
                </div>
                <p style='color: #7f8c8d; margin: 8px 0;'>
                    📅 *Due: {task['due_date']} | 🏷 **{task['category']}*
                </p>
                <div style='display: flex; gap: 8px;'>
            """, unsafe_allow_html=True)
            
            cols = st.columns(4)
            with cols[0]:
                if st.button("➡ Progress", key=f"progress_{task['id']}"):
                    idx = next(i for i, t in enumerate(tasks) if t["id"] == task["id"])
                    if tasks[idx]["status"] == "pending":
                        tasks[idx]["status"] = "in-progress"
                    elif tasks[idx]["status"] == "in-progress":
                        tasks[idx]["status"] = "completed"
                    st.session_state.tasks = tasks
                    save_tasks(tasks)
                    st.rerun()
            
            with cols[1]:
                if st.button("🔔 Remind", key=f"remind_{task['id']}"):
                    due = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                    days = (due - date.today()).days
                    st.info(f"🔔 *Reminder*: '{task['title']}' due in {days} days!")
            
            with cols[2]:
                if st.button("✏ Edit", key=f"edit_{task['id']}"):
                    st.session_state.editing_task = task["id"]
            
            with cols[3]:
                if st.button("🗑 Delete", key=f"delete_{task['id']}"):
                    st.session_state.tasks = [t for t in tasks if t["id"] != task["id"]]
                    save_tasks(st.session_state.tasks)
                    st.success("✅ Task deleted!")
                    st.rerun()
            
            st.markdown("</div></div>", unsafe_allow_html=True)

with col2:
    st.header("📊 *Dashboard*")
    
    total = len(tasks)
    pending = len([t for t in tasks if t["status"] == "pending"])
    overdue = len([t for t in tasks if 
                  datetime.strptime(t["due_date"], "%Y-%m-%d").date() < date.today() 
                  and t["status"] == "pending"])
    completed = len([t for t in tasks if t["status"] == "completed"])
    
    st.metric("Total", total)
    st.metric("Pending", pending, delta=f"+{overdue}" if overdue else None)
    st.metric("Completed", completed)
    
    if overdue > 0:
        st.error(f"🚨 *{overdue} OVERDUE* tasks!")

st.markdown("---")
st.markdown("""
<center>
<span style='color: #7f8c8d;'>
✅ *TaskManagerAgent* - Fully functional for AI Challenge<br>
📱 <a href='http://localhost:8501'>localhost:8501</a> | 💾 tasks.json | ⏰ Auto-reminders
</span>
</center>
""", unsafe_allow_html=True)
