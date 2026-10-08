from dotenv import load_dotenv
load_dotenv()
import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools import ALL_TOOLS
from langgraph.checkpoint.memory import InMemorySaver       # This module is used to save the state of the agent in memory, 
  # allowing it to remember previous interactions and maintain context across multiple queries.

def get_agent():
    "Get Agent with google search and weather search abilities"
    return create_agent(
        model= ChatGroq(model= "openai/gpt-oss-20b"),
        tools= ALL_TOOLS,
        system_prompt=(
            "You are a research assistant with google search and weather tools.\n"
            "Use 'google_search' for quick search on google"
            "for deep research that may take several minutes."
            "If user is looking for weather details like temperature, humidity or any other details"
            "then call the 'weather_tool' to get the real time weather data"
        ),
        checkpointer=InMemorySaver()
    )



# ===========================================
# ===========================================
# THis is for testing the agent in the console. 
# Create an agent:
# agent = get_agent()

# # Start a loop to interact with the agent. The loop will continue until the user types "exit".
# while True:
#     query = input("User : ")
#     if query == "exit":
#         break
# # The agent is invoked with the user's query, and the response is printed to the console. 
#     response = agent.invoke({"messages": [ {"role": "user", "content":query} ]})
#     ans = response["messages"][-1].content
#     print("AI :", ans)





