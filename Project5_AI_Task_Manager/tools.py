# AFTER CREATING THE DATABASE AND TABLES, WE NEED TO CREATE TOOLS :-
from langchain.tools import tool
from sqlalchemy import func
from database import LocalSession, Todo     # "LocalSession" → lets us communicate with the database.
from datetime import datetime               # "datetime" → gets the current date and time.

# We need '4 tools' to perform CRUD operations on the database. 

# ========== TOOL 1 =============
@tool
def create_todo(
    title: str, description: str = "", priority: str = "medium", due_date: str = ""    
):      # This line defines the parameters for the create_todo function, which will be used to create a new todo task. The title is required, while description, priority, and due_date are optional with default values.      
    
    """
    Create and save a new todo task.            

    Args:
        title: Short title for the task (required)
        description: Optional detailed note of the task
        priority: 'low', 'medium', or 'high' (default medium)
        due_date: Optional due date of the task. e.g. '25-03-2026'
    """     # This is docstring 

    task_priority = "medium"            # THis part sets the default priority to "Medium" and checks if the provided priority is valid (i.e., "Low", "Medium", or "High"). If it is valid, it updates task_priority accordingly.
    if priority.lower() in ["low", "high", "medium"]:
        task_priority = priority.lower()

    with LocalSession() as session:     # This line creates a new database session using the LocalSession context manager. It ensures that the session is properly closed after the block of code is executed, even if an error occurs.
        todo = Todo(                    # This line creates a new instance of the Todo class, which represents a new todo task. It initializes the task with the provided title, description, priority, due date, and the current timestamp for created_at.
            title= title,
            description= description,
            priority= task_priority,
            due_date= due_date,
            created_at= datetime.now().strftime("%d-%m-%Y %H:%M"),      # This line sets the created_at attribute of the todo task to the current date and time, formatted as "day-month-year hour:minute". 
        )

        session.add(todo)           # THis will add the newly created todo task to the current database session, marking it for insertion into the database when the session is committed.
        session.commit()            # THis will commit the current transaction, saving the new todo task to the database. If there are any issues during the commit, an exception will be raised, and the session will be rolled back.

        session.refresh(todo)       # This line refreshes the todo object with the latest data from the database, ensuring that any auto-generated fields (like the id) are updated in the todo instance.

        return f"""
            Todo created !
            Id: {todo.id} | Title: {todo.title}, | priority: {todo.priority}
        """         # This line returns a formatted string confirming the creation of the todo task, including its id, title, and priority.


# ========== TOOL 2 =============

@tool                                      
def list_todos(status: str = "all", priority: str = "all"):    # Function to get todos, optionally filtered by status/priority

    """                                      
    List all todos. Optionally filter by status or priority.   

    Args:                                    
        status:   'pending', 'in_progress', 'done', or 'all'  
        priority: 'low', 'medium', 'high', or 'all'            
    """                                      # End of the tool description


    with LocalSession() as sesion:           # Open a database session
        query = sesion.query(Todo)           # Create a query to get Todo records from the database

        if status.lower() != "all":
            query = query.filter(func.lower(Todo.status) == status.lower())

        if priority.lower() != "all":
            query = query.filter(func.lower(Todo.priority) == priority.lower())

        todos = query.order_by(Todo.id).all()                   # Get all matching todos and arrange them by their ID

        if not todos:                                           # Check whether any todo was found
            return f"No todos found for your filter values"     # Return a message if no todo matches

        allTodos = [todo.to_dict() for todo in todos]           # Convert every Todo object into a dictionary

        return allTodos                       # Return the list of todos


# ========== TOOL 3 =============

@tool                                     
def update_todos(                            # Function used to update an existing todo
    todo_id: int,                            # ID of the todo that needs to be updated
    title: str = "",                         # New title of the todo
    description: str = "",                   # New description; empty means no description
    status: str = "",                        # New status; empty means don't change it
    priority: str = "",                      # New priority; empty means don't change it
    due_date: str = "",                      # New due date; empty means don't change it
):                                           # End of function parameters

    """                                     
    Update an existing todo by its ID.       
    Only provide the fields you want to change.  

    Args:                                    
        todo_id:     ID of the todo to update (required)  
        title:       New title (leave empty to keep current)  
        description: New description (leave empty to keep current)  
        status:      New status — 'pending', 'in_progress', or 'done'  
        priority:    New priority — 'low', 'medium', or 'high'  
        due_date:    New due date e.g. '2025-12-25' 
    """                                      # End of the tool description

    with LocalSession() as session:          # Open a database session
        todo = session.get(Todo, todo_id)    # Find the Todo using its ID

        if not todo:                         # Check if the Todo does not exist
            return f"Todo with id {todo_id} not found"  # Tell the user that the Todo was not found

        if title:                            # Check if a new title was provided
            todo.title = title               # Update the Todo's title

        if description:                      # Check if a new description was provided
            todo.description = description   # Update the Todo's description

        if status:                           # Check if a new status was provided
            todo.status = status             # Update the Todo's status

        if priority:                         # Check if a new priority was provided
            todo.priority = priority         # Update the Todo's priority

        if due_date:                         # Check if a new due date was provided
            todo.due_date = due_date         # Update the Todo's due date

        session.commit()                     # Save all the changes permanently in the database
        session.refresh(todo)                # Get the latest updated information from the database

        return f"""                          
            Todo: {todo.id} updated!!        
            {todo.to_dict()}                 
        """         # ^^ Show all updated Todo information as a dictionary                         


# ========== TOOL 4 =============

@tool                                     
def delete_todo(todo_id: int):           # Function used to delete a Todo using its ID

    """                                      
    Permanently delete a todo by its ID.     
                                            
    Args:                                    
        todo_id: ID of the todo to delete (required)  
    """                                      

    with LocalSession() as session:          # Open a database session
        todo = session.get(Todo, todo_id)    # Find the Todo using its ID

        if not todo:                         # Check if the Todo does not exist
            return f"Todo with id {todo_id} not found"  # Tell the user that the Todo was not found

        title = todo.title                   # Save the Todo's title before deleting it

        session.delete(todo)                 # Mark the Todo for deletion

        session.commit()                     # Permanently delete the Todo from the database

        return f"Todo #{title} deleted successfully!!"  # Return a success message


all_tools = [create_todo, list_todos, update_todos, delete_todo]    # --> Tools
