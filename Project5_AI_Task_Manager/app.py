"""
app.py  -  The FRONTEND (what the user sees) of the AI TASK MANAGER.

How the project fits together:
    database.py  -> the storage room  (SQLite database + Todo table)
    tools.py     -> the AI's "hands"  (create / list / update / delete)
    agent.py     -> the AI's "brain"  (LLM + tools + system prompt)
    app.py       -> the screen        (THIS FILE, built with Streamlit)

Run it with:   streamlit run app.py
"""

import uuid
from datetime import datetime, date

import streamlit as st

# ---- Our own project files -------------------------------------------------
from database import LocalSession, Todo   # to read/write tasks directly (fast buttons)
from agent import CreateAgent             # the AI agent (for the chat tab)


# =============================================================================
# 1) PAGE SETTINGS  (must be the first Streamlit command)
# =============================================================================
st.set_page_config(
    page_title="Taskpad - AI Task Manager",
    page_icon="✅",
    layout="wide",
)


# =============================================================================
# 2) LOOK & FEEL  (CSS = the "paint and decoration" of a web page)
# =============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=Figtree:wght@400;500;600&display=swap');

    html, body, [class*="css"], .stMarkdown, button, input, textarea {
        font-family: 'Figtree', sans-serif;
    }
    h1, h2, h3, .app-title { font-family: 'Bricolage Grotesque', sans-serif !important; }

    .block-container { padding-top: 1.6rem; max-width: 1280px; }

    /* ---- Top banner ---- */
    .banner {
        background: #14213D;
        border-radius: 18px;
        padding: 26px 32px;
        margin-bottom: 18px;
        color: #fff;
    }
    .banner .app-title { font-size: 2.1rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; }
    .banner p { margin: 4px 0 0 0; color: #C9D1E8; font-size: 1.02rem; }

    /* ---- Board column headings: coloured top line shows the status ---- */
    .col-head {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 14px; margin-bottom: 10px;
        border-radius: 10px;
        background: rgba(128,128,128,0.10);
        font-family: 'Bricolage Grotesque', sans-serif;
        font-weight: 700; font-size: 1.05rem;
    }
    .col-head.pending     { border-top: 4px solid #8A94A6; }
    .col-head.in_progress { border-top: 4px solid #F2A900; }
    .col-head.done        { border-top: 4px solid #0F9D8A; }
    .col-count {
        background: rgba(128,128,128,0.25); border-radius: 20px;
        padding: 1px 11px; font-size: 0.85rem;
    }

    /* ---- Small coloured tags ---- */
    .tag {
        display: inline-block; padding: 2px 10px; margin: 0 6px 4px 0;
        border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    }
    .tag.high    { background: #FDE4DD; color: #B83A18; }
    .tag.medium  { background: #FFF1CC; color: #8A6100; }
    .tag.low     { background: #D9F2EE; color: #0B6E60; }
    .tag.due     { background: rgba(128,128,128,0.18); }
    .tag.overdue { background: #B83A18; color: #fff; }

    .task-title { font-weight: 700; font-size: 1.05rem; margin-bottom: 2px; }
    .task-desc  { opacity: 0.75; font-size: 0.92rem; margin-bottom: 8px; }
    .task-meta  { opacity: 0.55; font-size: 0.78rem; }
    .done-title { text-decoration: line-through; opacity: 0.6; }

    /* Make buttons a little rounder */
    .stButton > button { border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# 3) SMALL HELPER FUNCTIONS
# =============================================================================
# The database could contain "Pending", "pending", "In Progress", "in_progress"...
# (the AI and the code sometimes use different spellings).
# These helpers turn all the different spellings into ONE clean version.

STATUSES = {
    "pending":     {"label": "Pending",     "icon": "🕣"},
    "in_progress": {"label": "In Progress", "icon": "⏳"},
    "done":        {"label": "Done",        "icon": "✅"},
}
STATUS_ORDER = ["pending", "in_progress", "done"]
PRIORITIES = ["Low", "Medium", "High"]


def clean_status(value) -> str:
    """'In Progress' / 'in progress' / 'IN_PROGRESS'  ->  'in_progress'"""
    v = (value or "").strip().lower().replace(" ", "_")
    return v if v in STATUSES else "pending"


def clean_priority(value) -> str:
    """'high' / 'HIGH' -> 'High'. Unknown values become 'Medium'."""
    v = (value or "").strip().capitalize()
    return v if v in PRIORITIES else "Medium"


def parse_due(text: str):
    """Turn a due-date text like '25-03-2026' into a real date. Returns None if impossible."""
    for fmt in ("%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime((text or "").strip(), fmt).date()
        except ValueError:
            continue
    return None


# =============================================================================
# 4) DATABASE FUNCTIONS  (the buttons on the screen use these directly)
# =============================================================================
def get_all_todos() -> list[dict]:
    """Read every task from the database."""
    with LocalSession() as session:
        return [t.to_dict() for t in session.query(Todo).order_by(Todo.id).all()]


def add_todo(title, description, priority, due: date | None):
    with LocalSession() as session:
        session.add(
            Todo(
                title=title.strip(),
                description=description.strip(),
                status="pending",
                priority=priority.lower(),     # stored in small letters, same as tools.py
                due_date=due.strftime("%d-%m-%Y") if due else "",
                created_at=datetime.now().strftime("%d-%m-%Y %H:%M"),
            )
        )
        session.commit()


def set_status(todo_id: int, new_status: str):
    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if todo:
            todo.status = new_status
            session.commit()


def edit_todo(todo_id: int, title, description, priority, due_text):
    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if todo:
            todo.title = title.strip() or todo.title
            todo.description = description.strip()
            todo.priority = priority.lower()   # stored in small letters, same as tools.py
            todo.due_date = due_text
            session.commit()


def remove_todo(todo_id: int):
    with LocalSession() as session:
        todo = session.get(Todo, todo_id)
        if todo:
            session.delete(todo)
            session.commit()


# =============================================================================
# 5) THE AI AGENT  (cached = created once, then reused)
# =============================================================================
@st.cache_resource
def get_agent():
    return CreateAgent()


def ask_agent(question: str) -> str:
    """Send the user's message to the AI agent and return its text answer."""
    agent = get_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
        # thread_id = the "conversation id". Same id = the AI remembers earlier messages.
        {"configurable": {"thread_id": st.session_state.thread_id}},
    )
    return result["messages"][-1].content


# =============================================================================
# 6) SESSION STATE  (Streamlit forgets variables on every click,
#    so anything we want to remember must live in st.session_state)
# =============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []                 # chat history shown on screen
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())  # unique conversation id per visitor


# =============================================================================
# 7) LOAD DATA + CALCULATE NUMBERS
# =============================================================================
todos = get_all_todos()
for t in todos:                                    # tidy up spelling differences
    t["status"] = clean_status(t["status"])
    t["priority"] = clean_priority(t["priority"])

total = len(todos)
count = {s: sum(1 for t in todos if t["status"] == s) for s in STATUS_ORDER}
progress = (count["done"] / total) if total else 0
today = date.today()
overdue = sum(
    1 for t in todos
    if t["status"] != "done" and parse_due(t["due_date"]) and parse_due(t["due_date"]) < today
)


# =============================================================================
# 8) SIDEBAR  -  add a new task + quick stats
# =============================================================================
with st.sidebar:
    st.markdown("### ➕ Add a new task")

    # st.form groups the inputs, so nothing happens until the button is pressed
    with st.form("add_task_form", clear_on_submit=True):
        new_title = st.text_input("Task title *", placeholder="e.g. Finish project report")
        new_desc = st.text_area("Details (optional)", placeholder="Add a short note...", height=90)
        new_priority = st.select_slider("Priority", options=PRIORITIES, value="Medium")
        has_due = st.checkbox("Set a due date")
        new_due = st.date_input("Due date", value=today, format="DD/MM/YYYY")
        submitted = st.form_submit_button("Add task", type="primary", use_container_width=True)

    if submitted:
        if not new_title.strip():
            st.error("Please type a title for the task.")
        else:
            add_todo(new_title, new_desc, new_priority, new_due if has_due else None)
            st.toast("Task added", icon="✅")
            st.rerun()   # reload the page so the new task appears

    st.divider()
    st.markdown("### 📊 Your progress")
    st.progress(progress, text=f"{count['done']} of {total} tasks done")
    if overdue:
        st.warning(f"{overdue} task(s) are past their due date.")
    elif total:
        st.success("Nothing is overdue. Nice work!")

    st.divider()
    if st.button("🗑️ Clear chat history", use_container_width=True):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())   # also resets the AI's memory
        st.rerun()


# =============================================================================
# 9) MAIN PAGE  -  banner + numbers
# =============================================================================
st.markdown(
    """
    <div class="banner">
        <div class="app-title">Taskpad</div>
        <p>Plan your work on the board, or just tell the AI assistant what you need.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

m1, m2, m3, m4 = st.columns(4)
m1.metric("All tasks", total)
m2.metric("🕣 Pending", count["pending"])
m3.metric("⏳ In progress", count["in_progress"])
m4.metric("✅ Done", count["done"])

# Navigation between the two screens.
# (We use st.radio instead of st.tabs because radio REMEMBERS the selected screen
#  when the page reloads, while tabs jump back to the first one.)
view = st.radio(
    "View",
    ["📋 Task board", "🤖 AI assistant"],
    horizontal=True,
    label_visibility="collapsed",
    key="view",
)
st.write("")


# =============================================================================
# 10) SCREEN 1  -  TASK BOARD  (three columns: Pending / In Progress / Done)
# =============================================================================
def render_card(t: dict):
    """Draw ONE task card, with its buttons."""
    tid = t["id"]
    status = t["status"]
    due = parse_due(t["due_date"])
    is_overdue = bool(due and due < today and status != "done")

    with st.container(border=True):
        title_class = "task-title done-title" if status == "done" else "task-title"
        st.markdown(f'<div class="{title_class}">{t["title"]}</div>', unsafe_allow_html=True)

        if t["description"]:
            st.markdown(f'<div class="task-desc">{t["description"]}</div>', unsafe_allow_html=True)

        tags = f'<span class="tag {t["priority"].lower()}">{t["priority"]} priority</span>'
        if t["due_date"]:
            css = "overdue" if is_overdue else "due"
            label = "Overdue: " if is_overdue else "Due "
            tags += f'<span class="tag {css}">{label}{t["due_date"]}</span>'
        st.markdown(tags, unsafe_allow_html=True)
        st.markdown(
            f'<div class="task-meta">#{tid} · created {t["created_at"]}</div>',
            unsafe_allow_html=True,
        )

        # ---- Action buttons ----
        i = STATUS_ORDER.index(status)
        b1, b2, b3, b4 = st.columns(4)

        if i > 0 and b1.button("◀", key=f"back_{tid}", help="Move back", use_container_width=True):
            set_status(tid, STATUS_ORDER[i - 1])
            st.rerun()

        if i < 2 and b2.button("▶", key=f"next_{tid}", help="Move forward", use_container_width=True):
            set_status(tid, STATUS_ORDER[i + 1])
            st.rerun()

        # Edit button opens a small pop-up with a mini form
        with b3.popover("✏️", help="Edit task", use_container_width=True):
            e_title = st.text_input("Title", t["title"], key=f"et_{tid}")
            e_desc = st.text_area("Details", t["description"], key=f"ed_{tid}")
            e_pri = st.selectbox(
                "Priority", PRIORITIES, index=PRIORITIES.index(t["priority"]), key=f"ep_{tid}"
            )
            e_due = st.text_input("Due date (DD-MM-YYYY)", t["due_date"], key=f"edue_{tid}")
            if st.button("Save changes", key=f"save_{tid}", type="primary"):
                edit_todo(tid, e_title, e_desc, e_pri, e_due)
                st.rerun()

        if b4.button("🗑️", key=f"del_{tid}", help="Delete task", use_container_width=True):
            remove_todo(tid)
            st.toast("Task deleted", icon="🗑️")
            st.rerun()


if view == "📋 Task board":

    # ---- Search + filter ----
    f1, f2 = st.columns([2, 1])
    search = f1.text_input("Search", placeholder="🔎 Search tasks...", label_visibility="collapsed")
    pri_filter = f2.multiselect(
        "Priority", PRIORITIES, default=PRIORITIES, label_visibility="collapsed",
        placeholder="Filter by priority",
    )

    shown = [
        t for t in todos
        if t["priority"] in pri_filter
        and search.lower() in (t["title"] + " " + (t["description"] or "")).lower()
    ]

    if not todos:
        st.info("No tasks yet. Add your first one from the sidebar, or ask the AI assistant to do it.")
    else:
        board = st.columns(3)
        for col, s in zip(board, STATUS_ORDER):
            with col:
                items = [t for t in shown if t["status"] == s]
                st.markdown(
                    f'<div class="col-head {s}"><span>{STATUSES[s]["icon"]} {STATUSES[s]["label"]}</span>'
                    f'<span class="col-count">{len(items)}</span></div>',
                    unsafe_allow_html=True,
                )
                if not items:
                    st.caption("Nothing here.")
                for t in items:
                    render_card(t)


# =============================================================================
# 11) SCREEN 2  -  AI ASSISTANT CHAT
# =============================================================================
else:
    st.markdown("#### Talk to your task manager")
    st.caption("Type in plain English. The AI will create, show, update or delete tasks for you.")

    # Quick-start buttons: clicking one sends that sentence to the AI
    suggestions = [
        "List all my tasks",
        "Show high priority tasks",
        "Add a task: Buy groceries, due tomorrow",
        "What is still pending?",
    ]
    cols = st.columns(len(suggestions))
    quick = None
    for c, text in zip(cols, suggestions):
        if c.button(text, use_container_width=True):
            quick = text

    # Show earlier messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    if not st.session_state.messages:
        st.info("Try: *“Add a high priority task to call the bank”* or *“Mark task 2 as done”*.")

    # Chat box at the bottom
    typed = st.chat_input("Ask the AI to manage your tasks...")
    prompt = typed or quick

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Working on it..."):
                try:
                    answer = ask_agent(prompt)
                except Exception as err:   # e.g. missing GROQ_API_KEY, no internet
                    answer = (
                        "Sorry, I could not reach the AI. Check your internet connection "
                        f"and your GROQ_API_KEY in the .env file.\n\nDetails: `{err}`"
                    )
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()   # reload so the sidebar numbers and the board show the AI's changes