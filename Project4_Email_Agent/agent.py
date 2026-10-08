from dotenv import load_dotenv
load_dotenv()
import os
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools import ALL_TOOLS
from langgraph.checkpoint.memory import InMemorySaver 

MODEL = ChatGroq(model= "openai/gpt-oss-20b")


SYSTEM_PROMPT = """You are an email assistant. You can do one thing: send an email.

You need two things before you can write the email:
1. the recipient's email address
2. the reason for the email — what it is actually about

Rules:
- If either one is missing, ASK for it in one short sentence. Ask for one thing at a time.
- Never invent an email address and never invent a reason. Asking is always better than guessing.
- Remember what the user already told you earlier in this conversation. Do not ask again.
- Once you have both, write a draft: a clear one-line subject and a short
  plain-text body of 3 to 6 sentences. No placeholders like [Your Name].
- Show the draft to the user and ask if they approve or want changes.
- If they want changes, update the draft and ask for approval again.
- Only after the user clearly approves, call the send_email tool.
- After it is sent, reply with one line saying who it went to and the subject.
"""


def get_agent():
    "Get Agent that send email to any email address"
    return create_agent(
        model = ChatGroq(model= "openai/gpt-oss-20b"),
        tools = ALL_TOOLS,
        system_prompt = SYSTEM_PROMPT,
        checkpointer = InMemorySaver()
    )