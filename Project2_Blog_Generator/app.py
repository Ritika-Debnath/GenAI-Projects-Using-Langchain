import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate           # we can create a prompt template for the LLM to generate responses based on the user's input and the conversation history.
from langchain_core.output_parsers import StrOutputParser       # "StrOutputParser" is used to parse the output of the LLM into a string format that can be displayed in the chat interface.
from dotenv import load_dotenv
load_dotenv()  

llm = ChatGroq(model = "openai/gpt-oss-20b")        # Create the LLM instance with the specified model. 


# Create Prompts for the LLM to generate responses:
HUMAN_STYLE = """Write like a person, not like an AI:
- Vary your sentence length. Some short. Others longer, with a clause that earns its place.
- Use contractions (it's, don't, you'll) and talk straight to the reader as "you".
- Replace vague claims with a concrete example, a number, or a small story.
- Having an opinion is fine. Saying "I" is fine.
- Never use these words and phrases: "in today's fast-paced world", "delve", "moreover",
  "furthermore", "unlock", "leverage", "robust", "seamless", "game-changer",
  "it's worth noting", "navigate the landscape", "at the end of the day".
- Do not start every section the same way.
- Only use a bullet list when the content really is a list. Prefer paragraphs.
- Do not end with a summary of what you just said. End with one useful thought."""

OUTLINE_PROMPT = ChatPromptTemplate.from_template(      # We use "from_template" method to create a prompt template for the LLM to generate an outline for a blog post based on the user's input.
    "Write a short outline for a blog post.\n\n"
    "Topic: {topic}\n"
    "Tone: {tone}\n\n"
    "Give me:\n"
    "- one opening line that makes the reader curious\n"
    "- 4 section headings\n"
    "- 5 key points the post must cover\n\n"
    "Just the outline. Do not write the post."
)

DRAFT_PROMPT = ChatPromptTemplate.from_template(
    "Write a blog post from this outline.\n\n"
    "{outline}\n\n"
    + HUMAN_STYLE
    + "\n\n"
    "Tone: {tone}\n"
    "Output markdown, with the section headings as ###.\n"
    "Make it as long or as short as the topic actually needs."
)

POLISH_PROMPT = ChatPromptTemplate.from_template(
    "Improve this blog post without changing what it says.\n\n"
    + HUMAN_STYLE
    + "\n\n"
    "Also:\n"
    "- add a good # title at the top\n"
    "- keep the markdown\n\n"
    "Reply with the improved post only, no commentary.\n\n"
    "{draft}"
)


# Create Chains:
outline_chain = OUTLINE_PROMPT | llm | StrOutputParser()
draft_chain = DRAFT_PROMPT | llm | StrOutputParser()
final_chain = POLISH_PROMPT | llm | StrOutputParser()


# Create UI design:
st.subheader("✍️ AI Blog Generator")        # This will create a subheader in the Streamlit app (frontend)
st.caption("Outline → Draft → Polish. Three prompts, three chains.")     # This will create a caption beneath the subheader.

topic = st.text_input("Blog Title", "Why we have to learn the Gen-AI in 2026")      # This will create a text input field for the user to enter the blog title. 
tone = st.selectbox("Tone", ["direct", "normal", "friendly"])       # This will create a dropdown select box for the user to select the tone of the blog post.


# Handle the user's input and generate the blog post:
if st.button("Generate", type= "primary"):          # This will create a button that the user can click to generate the blog post.
    with st.spinner("Generating the outline"):
        outline = outline_chain.invoke({"topic":topic, "tone":tone})       # This will invoke the outline_chain with the user's input (topic and tone) to generate an outline for the blog post.
        
    with st.spinner("Generating the Draft"):
        draft = draft_chain.invoke({"outline": outline, "tone":tone})       # This will invoke the draft_chain with the generated outline and the user's selected tone to generate a draft for the blog post.
        
    with st.spinner("Polishing the draft blog"):
        final = final_chain.invoke({"draft": draft})        # This will invoke the final_chain with the generated draft to polish the blog post and produce the final version.
        
    st.markdown(final)          # This will display the final polished blog post in the (frontend) using markdown formatting.


    with st.expander("Raw Blog", expanded = False):   # This will create an expandable section that allows the user to view the raw blog post to copy for further use.
        st.code(final)          # This will display the final polished blog post in the expandable section using code formatting.



