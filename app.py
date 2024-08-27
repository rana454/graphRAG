import os
import re
import streamlit as st


def query_llm(method, query):
    command = f"python -m graphrag.query --root ./ragtest --method {method} \"{query}\""
    result = os.popen(command).read()

    # Extract text after "SUCCESS: "
    success_pattern = r'SUCCESS:.*?\n(.*)'
    match = re.search(success_pattern, result, re.DOTALL)
    if match:
        filtered_result = match.group(1).strip()
    else:
        filtered_result = result

    return filtered_result
os.environ["GRAPHRAG_API_KEY"] = st.secrets["GRAPHRAG_API_KEY"]
# Initialize session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("BIPARD Query Interface")

method = st.sidebar.selectbox("Select Method", ["global", "local"])
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
if prompt := st.chat_input("Enter your query"):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = query_llm(method, prompt)
    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})


