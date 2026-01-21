import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

load_dotenv()

session_store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


groq_api_key = os.getenv("GROQ_API_KEY")


def ask_groq(message, session_id="default_session", language="English"):
    try:
        llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)
        try:
            with open("system_prompt.txt", "r", encoding="utf-8") as file:
                system_prompt = file.read().strip()
        except FileNotFoundError:
            system_prompt = "You are a helpful AI assistant."

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        chain = prompt | llm
        with_message_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="messages",
        )
        config = {"configurable": {"session_id": session_id}}

        response = with_message_history.invoke(
            {"messages": [HumanMessage(content=message)]}, config=config
        )
        return response.content

    except Exception as e:
        return f"Error: {str(e)}"
