import streamlit as st
import os
import openai
import json
from llama_index import GPTSimpleVectorIndex

key = "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"
api_key = os.environ["OPENAI_API_KEY"] = key
index = GPTSimpleVectorIndex.load_from_disk("TomalinLE_HorvathS_SinclairDA.JSON")

class Chatbot:
    def __init__(self, api_key, index):
        self.index = index
        openai.api_key = api_key
        self.chat_history = []

    def generate_response(self, user_input):
        prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
        prompt += f"\nUser: {user_input}"
        response = index.query(user_input)

        message = {"role": "assistant", "content": response.response}
        self.chat_history.append({"role": "user", "content": user_input})
        self.chat_history.append(message)
        return message
    
    def load_chat_history(self, filename):
        try:
            with open(filename, 'r') as f:
                self.chat_history = json.load(f)
        except FileNotFoundError:
            pass

    def save_chat_history(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.chat_history, f)

def main():
    # Set up the chatbot
    chatbot = Chatbot(api_key, index)

    # Load chat history from file (if it exists)
    chat_history_file = "chat_history.json"
    chatbot.load_chat_history(chat_history_file)

    # Set up the Streamlit UI
    st.set_page_config(page_title="GeneBot", page_icon=":robot_face:")
    st.title("GeneBot")

    # Define the chat UI
    chat_history = st.empty()
    chat_input = st.text_input("User:")
    if st.button("Send"):
        message = chatbot.generate_response(chat_input)
        chat_history.write(f"{message['role']}: {message['content']}")
        chat_input.text_input = ""

    # Display chat history
    for message in chatbot.chat_history:
        chat_history.write(f"{message['role']}: {message['content']}")

    # Save chat history to file
    chatbot.save_chat_history(chat_history_file)

if __name__ == "__main__":
    main()
