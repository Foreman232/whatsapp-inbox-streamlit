import streamlit as st
import pandas as pd
import requests
import json

API_URL = "https://waba-v2.360dialog.io/messages"
API_TOKEN = "Bearer TU_TOKEN_DE_360DIALOG"

# Simulación de mensajes entrantes desde archivo local
def cargar_mensajes():
    with open("data.json", "r", encoding="utf-8") as f:
        return pd.DataFrame(json.load(f))

df = cargar_mensajes()

st.title("📬 Bandeja de Entrada WhatsApp")

usuarios = df["from"].unique()
seleccionado = st.selectbox("Selecciona un número", usuarios)

conversacion = df[df["from"] == seleccionado]

for _, row in conversacion.iterrows():
    if row["direction"] == "in":
        st.markdown(f"🟢 *{row['from']}*: {row['message']}")
    else:
        st.markdown(f"🔵 *Tú*: {row['message']}")

st.markdown("---")
respuesta = st.text_input("Escribe tu respuesta:")
if st.button("📤 Enviar"):
    payload = {
        "to": f"whatsapp:{seleccionado}",
        "type": "text",
        "text": {"body": respuesta}
    }
    headers = {
        "Authorization": API_TOKEN,
        "Content-Type": "application/json"
    }
    r = requests.post(API_URL, headers=headers, json=payload)
    if r.status_code == 200:
        st.success("Mensaje enviado")
    else:
        st.error(f"Error al enviar: {r.text}")