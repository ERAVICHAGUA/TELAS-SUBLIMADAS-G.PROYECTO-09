import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Inspección de Rebaba", layout="wide")

st.title("🔍 Sistema de Inspección de Rebaba + Registro de Medidas")

tab1, tab2 = st.tabs(["📤 Inspeccionar Imagen", "📜 Ver Registros"])

# ============================================================
# TAB 1 — INSPECCIONAR IMAGEN
# ============================================================
with tab1:
    st.header("Subir imagen para inspección")

    uploaded_file = st.file_uploader("Selecciona una imagen", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        st.image(uploaded_file, caption="Imagen subida", width=350)

        if st.button("🔎 Procesar imagen"):
            with st.spinner("Analizando..."):

                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                response = requests.post(f"{API_URL}/api/inspeccionar", files=files)

                if response.status_code == 200:
                    data = response.json()

                    st.subheader("📌 Resultado")
                    st.write(f"**Estado:** {data['status']}")
                    st.write(data["mensaje"])

                    st.write("**Puntos defectuosos detectados:**")
                    st.json(data["puntos_defectuosos"])

                    st.write(f"**Distancia Máxima:** {data['max_distancia']} px")

                else:
                    st.error("❌ Error al comunicarse con el backend")

# ============================================================
# TAB 2 — VER REGISTROS
# ============================================================
with tab2:
    st.header("Historial de inspecciones")

    if st.button("📥 Cargar registros"):
        with st.spinner("Obteniendo datos..."):
            response = requests.get(f"{API_URL}/api/registros")

            if response.status_code == 200:
                data = response.json()
                registros = data.get("inspecciones", [])

                if len(registros) == 0:
                    st.info("No hay registros aún.")
                else:
                    df = pd.DataFrame(registros)
                    st.dataframe(df, use_container_width=True)
            else:
                st.error("❌ Error al obtener registros desde el backend")
