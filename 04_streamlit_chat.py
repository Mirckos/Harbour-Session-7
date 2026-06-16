import streamlit as st

st.set_page_config(page_title="Streamlit Chat")
st.title("Streamlit Chat Demo")

if "runs" not in st.session_state:
    st.session_state.runs = 0
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Send a message and I will reverse it."}
    ]

st.session_state.runs += 1

with st.sidebar:
    st.metric("Script reruns", st.session_state.runs)
    if st.button("Clear chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared. Send a new message."}
        ]
        st.rerun()

for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

if prompt := st.chat_input("Say something"):
    response = prompt[::-1]
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append({"role": "assistant", "content": response})

    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write(response)
