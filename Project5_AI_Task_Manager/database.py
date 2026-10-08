# IN THIS PROJECT WE FIRST WE CREATE A DATABASE(DATABASE.PY FILE) AND TABLES TO STORE THE TODOS:

from sqlalchemy import create_engine, Column, Integer, String, DateTime     # Import tools needed to create the database, columns, and data types
from sqlalchemy.orm import DeclarativeBase, sessionmaker    # Import Base class for defining tables and sessionmaker for database sessions


database_url = "sqlite:///todos.db"             # Define the SQLite database URL; todos.db will be created in the current project folder

engine = create_engine(database_url)            # Create a connection/engine that SQLAlchemy will use to communicate with the database
LocalSession = sessionmaker(bind=engine)        # Create a session factory connected to our database engine so you can add, update, delete, and query data.


class Base(DeclarativeBase):    # Create the base class that all our database table classes will inherit from
    pass                        # Nothing else needs to be added to the Base class


class Todo(Base):               # Create the Todo table model by inheriting from Base
    __tablename__ = "todos"     # Set the name of the table in the database to "todos"

    id = Column(Integer, primary_key=True, autoincrement=True)      # Create an integer ID column that is the primary key and automatically increases
    title = Column(String(200), nullable=False)                     # Create a title column that can contain up to 200 characters and cannot be empty
    description = Column(String(500), default="")                   # Create a description column with a maximum of 500 characters; default value is an empty string
    status = Column(String(20), default="pending")                  # Create a status column; its default value is "Pending"
    priority = Column(String(20), default="medium")  
    due_date = Column(String(20), default="")  
    created_at = Column(String(20), nullable=False)                 # Create a created_at column that cannot be empty


    def to_dict(self):          # Define a method to convert a Todo database object into a Python dictionary
        return {                # Return the Todo object's information as a dictionary
            "id": self.id,          # Store the Todo ID in the dictionary
            "title": self.title,    # Store the Todo title in the dictionary
            "description": self.description,  
            "status": self.status,  
            "priority": self.priority,  
            "due_date": self.due_date,  
            "created_at": self.created_at 
        }       # Finish and return the dictionary


def init_db():                  # Define a function that will initialize/create the database tables
    Base.metadata.create_all(engine)    # Create all tables defined using Base if they do not already exist


