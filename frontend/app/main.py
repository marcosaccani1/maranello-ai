import streamlit as st

from app.api_client import BackendConnectionError, send_chat_message

st.set_page_config(
    page_title="Maranello AI",
    page_icon="🏎️",
    layout="centered",
)

st.title("🏎️ Maranello AI")
st.caption("Enterprise Knowledge Assistant")

with st.sidebar:
    st.header("Informazioni")

    st.write(
        "Assistente aziendale dimostrativo basato su FastAPI, "
        "LangGraph e Retrieval-Augmented Generation."
    )

    st.divider()

    st.subheader("Stato attuale")
    st.write("Frontend collegato al backend FastAPI.")
    st.write("RAG e agente AI saranno aggiunti nei prossimi incrementi.")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Ciao, sono Maranello AI. "
                "Come posso aiutarti con la knowledge base aziendale?"
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Scrivi una domanda...")

if prompt:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sto elaborando la richiesta..."):
            try:
                response = send_chat_message(prompt)
                answer = response["answer"]
            except BackendConnectionError:
                answer = (
                    "Non riesco a contattare il backend. "
                    "Verifica che FastAPI sia in esecuzione sulla porta 8000."
                )

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )