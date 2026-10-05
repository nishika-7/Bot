import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

import os
from dotenv import load_dotenv
load_dotenv()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]="QnABot"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful massistant . Please  repsonse to the user queries"),
        ("user", "{question}")
    ]
)

def generate_response(question,api_key, engine, temperature, max_tokens):
     groq_api_key = api_key
     llm = ChatGroq(model =engine, groq_api_key=api_key)
     output_Parser=StrOutputParser()
     chain = prompt | llm | output_Parser
     answer = chain.invoke({question})
     return answer

## Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Open AI API Key:",type="password")

## Select the OpenAI model
engine=st.sidebar.selectbox("Select Groq model",["openai/gpt-oss-120b"])

## Adjust response parameter
temperature=st.sidebar.slider("Temperature",min_value=0.0,max_value=1.0,value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

st.write("Goe ahead and ask any question")
user_input=st.text_input("You:")

if user_input and api_key:
     response = generate_response(user_input, api_key, engine, temperature, max_tokens)
     st.write(response)
elif user_input:
     st.warning("Please enter valid api_key")
else:
     st.warning("Provide user_input")