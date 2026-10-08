# GenAI Projects Using LangChain

A collection of 5 beginner-friendly Generative AI projects built with **Python**, **LangChain** and **Streamlit**. Each project lives in its own folder and can be run on its own. They get a little more advanced as you go, from a simple Q&A bot to an AI agent that manages a database.

## Projects

| # | Project | What it does |
|---|---------|--------------|
| 1 | [QnA Bot](./Project1_QnA_Bot) | A chatbot that answers your questions using an LLM. |
| 2 | [Blog Generator](./Project2_Blog_Generator) | Writes a blog post for any topic you give it. |
| 3 | [Search & Weather Agent](./Project3_Search_Weather_Agent) | An AI agent that uses tools to search the web and get the weather. |
| 4 | [Email Agent](./Project4_Email_Agent) | An AI agent that uses tools to help write and send emails. |
| 5 | [AI Task Manager](./Project5_AI_Task_Manager) | A todo app with a task board and an AI assistant that manages tasks stored in a database. |

> Tip: edit the "What it does" column so it matches exactly what your projects do.

## Featured: AI Task Manager (Project 5)

Plan your work on a Kanban-style board, or just tell the AI what you need in plain English.

**Features**

- Task board with three columns: Pending, In Progress and Done
- Add, edit, move and delete tasks with simple buttons
- Search tasks and filter them by priority
- Progress bar and overdue warnings
- AI chat assistant, for example *"Add a high priority task to call the bank"* or *"Mark task 2 as done"*
- Tasks are saved in a local SQLite database

**How the files fit together**

| File | Job |
|------|-----|
| `database.py` | Creates the SQLite database and the `todos` table |
| `tools.py` | The 4 tools the AI can use: create, list, update, delete |
| `agent.py` | The AI agent: LLM + tools + system prompt + memory |
| `app.py` | The Streamlit frontend (what the user sees) |

## Tech Stack

- Python 3.10 or newer
- [LangChain](https://www.langchain.com/) and [LangGraph](https://www.langchain.com/langgraph) for building the AI agents
- [Groq](https://groq.com/) as the LLM provider
- [Streamlit](https://streamlit.io/) for the web interface
- [SQLAlchemy](https://www.sqlalchemy.org/) and SQLite for the database (Project 5)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac / Linux
source .venv/bin/activate
```

### 3. Install the requirements

```bash
pip install -r requirements.txt
```

### 4. Add your API key

Create a file named `.env` in the main folder and add your key (you can get a free one from the [Groq Console](https://console.groq.com/)):

```
GROQ_API_KEY=your_key_here
```

Never share this file or upload it to GitHub. It is already listed in `.gitignore`.

### 5. Run a project

Go into the project folder and start it with Streamlit. For example, for the AI Task Manager:

```bash
cd Project5_AI_Task_Manager
streamlit run app.py
```

Your browser will open at `http://localhost:8501`. The same steps work for the other projects, just change the folder name.

## Notes

- The Task Manager creates its own `todos.db` file the first time you run it, so there is nothing to set up.
- If you deploy the Task Manager online, a SQLite file on a free host can be erased when the app restarts, and all visitors share the same tasks. For real use, switch to a cloud database and add user login.

## Future Ideas

- User login, so every person has their own private tasks
- Cloud database (PostgreSQL) so data is never lost
- Due-date reminders
- Deploy all projects online

## Author

**Your Name**
GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)

If you like this project, please give it a star ⭐
