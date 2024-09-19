import streamlit as st
import openai

st.title("ChatGPT-like clone")

# Configura la clave de API de OpenAI desde los secretos de Streamlit
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Establece un modelo por defecto
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Inicializa el historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Muestra los mensajes del historial en la aplicación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Acepta la entrada del usuario
if prompt := st.chat_input("¿En qué puedo ayudarte?"):
    # Agrega el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Muestra el mensaje del usuario
    with st.chat_message("user"):
        st.markdown(prompt)

    # Genera y muestra la respuesta del asistente
    with st.chat_message("assistant"):
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            stream=False,  # Cambia a True si deseas transmisión en tiempo real
        )
        assistant_message = response["choices"][0]["message"]["content"]
        st.markdown(assistant_message)
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
