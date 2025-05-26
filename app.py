import streamlit as st
import pandas as pd
import requests
import json

st.set_page_config(page_title="Bandeja WhatsApp", layout="centered")

API_URL = "https://waba-v2.360dialog.io/messages"
API_TOKEN = "Bearer yxKGn4IO24k4MRONILaJxG7xAK"

st.markdown("""
<style>
.chat-bubble {
    padding: 0.8em;
    margin: 0.3em 0;
    border-radius: 10px;
    max-width: 80%;
    display: inline-block;
}
.incoming {
    background-color: #e1ffc7;
    align-self: flex-start;
}
.outgoing {
    background-color: #dcf8c6;
    align-self: flex-end;
    text-align: right;
    margin-left: auto;
}
</style>
""", unsafe_allow_html=True)

def cargar_mensajes():
    with open("data.json", "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

df = cargar_mensajes()
st.title("📱 Bandeja de Entrada WhatsApp")

usuarios = df["from"].unique()
seleccionado = st.selectbox("Selecciona un número", usuarios)

conversacion = df[df["from"] == seleccionado]

for _, row in conversacion.iterrows():
    clase = "incoming" if row["direction"] == "in" else "outgoing"
    st.markdown(f'<div class="chat-bubble {clase}">{row["message"]}</div>', unsafe_allow_html=True)

st.markdown("---")
respuesta = st.text_input("Escribe tu respuesta:")

if st.button("📤 Enviar"):
    payload = {
        "to": f"whatsapp:{seleccionado}",
        "type": "text",
        "text": {"body": respuesta}
    }
    headers = {
        "D360-API-KEY": API_TOKEN.replace("Bearer ", ""),
        "Content-Type": "application/json"
    }
    r = requests.post(API_URL, headers=headers, json=payload)
    if r.status_code == 200:
        st.success("Mensaje enviado correctamente")
    else:
        st.error(f"Error al enviar: {r.text}")
