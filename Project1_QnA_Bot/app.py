from dotenv import load_dotenv
load_dotenv()                        # Load environment variables from .env file
from langchain_groq import ChatGroq  # IMport the ChatGroq class from langchain_groq
import streamlit as st

llm = ChatGroq(model = "openai/gpt-oss-20b")  # Create the LLM instance with the specified model


# Create UI:
if "messages" not in st.session_state:
    st.session_state.messages = []    # Initialize the messages list in session state if it doesn't exist


st.subheader("🤖 Qna Bot")                   # Display the subheader for the chat interface

query = st.chat_input("Ask anything ....")

for msg in st.session_state.messages:
    st.chat_message(msg.get("role")).markdown(msg.get("content"))   # Display each message in the conversation history in the chat interface without overwriting the previous messages.


# Handle the user's query and generate a response from the LLM:
if query:
    st.session_state.messages.append({"role": "user", "content": query})      # Append the user's query to the conversation history
    st.chat_message("user").markdown(query)                # Display the user's query in the chat interface in the frontend
    response = llm.invoke(st.session_state.messages)       # Invoke the LLM with the conversation history
    st.session_state.messages.append({"role": "ai", "content": response.content})    # Append the AI's response to the conversation history
    st.chat_message("ai").markdown(response.content)        # Display the AI's response in the chat interface


print(st.session_state.messages)        # Print the conversation history to the console for debugging purposes







# ===========================================
# ===========================================
# THIS IS THE OLD CODE THAT WAS USED TO DISPLAY THE CONVERSATION HISTORY IN THE CONSOLE INSTEAD OF THE CHAT INTERFACE.
# THIS IS THE BASE CODE THAT WAS MODIFIED TO DISPLAY THE CONVERSATION HISTORY IN THE CHAT INTERFACE INSTEAD OF THE CONSOLE.
# WE DON'T NEED THIS CODE BECAUSE WE ARE USING STREAMLIT TO DISPLAY THE CONVERSATION HISTORY IN THE CHAT INTERFACE INSTEAD OF THE CONSOLE.
# while True:
#     query = input("User: ")          # Prompt the user for input
#     if query == "exit":             # If the user types "exit", break the loop and end the program
#         break
#     history.append([{"role": "user", "content": query}])      # Append the user's query to the conversation history
#     response = llm.invoke(history)                            # Invoke the LLM with the conversation history
#     print("AI: ", response.content)                           # Print the AI's response to the console
#     history.append([{"role": "ai", "content": response.content}])    # Append the AI's response to the conversation history
