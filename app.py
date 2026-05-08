import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuración de la aplicación
st.set_page_config(page_title="Gravity Works - Albarán Digital", page_icon="🏗️")

# --- BASE DE DATOS DE PARTIDAS ---
partidas_info = [
    {"n": 1, "esp": "RED HORIZONTAL BAJO ENCOFRADO", "uni": "M2"},
    {"n": 2, "esp": "PROTECCIÓN PERIMETRAL CON BARANDILLAS + MORDAZAS", "uni": "ML"},
    {"n": 3, "esp": "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASES", "uni": "ML"},
    {"n": 4, "esp": "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASES (HUECOS)", "uni": "ML"},
    {"n": 5, "esp": "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASQUIS (HUECOS)", "uni": "ML"},
    {"n": 6, "esp": "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASQUIS (MURO)", "uni": "ML"},
    {"n": 7, "esp": "PROTECCIÓN PERIMETRAL CON GARRAS DE MURO", "uni": "ML"},
    {"n": 8, "esp": "PROTECCIÓN PERIMETRAL DE MURO PANTALLA", "uni": "ML"},
    {"n": 9, "esp": "PROTECCIÓN HORIZONTAL CON REDES (HUECOS)", "uni": "M2"},
    {"n": 10, "esp": "PROTECCIÓN VERTICAL CON REDES (HUECOS)", "uni": "M2"},
    {"n": 11, "esp": "PRIMERA PUESTA DE HORCAS", "uni": "ML"},
    {"n": 12, "esp": "ELEVACIÓN HORCAS", "uni": "ML"},
    {"n": 13, "esp": "RED DE DESENCOFRADO", "uni": "ML"},
    {"n": 14, "esp": "RED VERTICAL DE FACHADA", "uni": "M2"},
    {"n": 15, "esp": "RED VERTICAL - ESCALERAS", "uni": "M2"},
    {"n": 16, "esp": "PERÍMETRO CON BARANDILLAS EN ESCALERAS", "uni": "ML"},
    {"n": 17, "esp": "RED EN VENTANAS", "uni": "UDS"},
    {"n": 18, "esp": "LINEA DE VIDA HORIZONTAL (MOCHILA)", "uni": "UDS"},
    {"n": 19, "esp": "LINEA DE VIDA VERTICAL (CUERDA)", "uni": "ML"},
    {"n": 20, "esp": "PUNTOS DE ANCLAJE (TEXTILES)", "uni": "UDS"},
    {"n": 21, "esp": "PUNTOS DE ANCLAJE (METÁLICOS)", "uni": "UDS"},
    {"n": 22, "esp": "PUNTOS DE ANCLAJE CON CABO", "uni": "UDS"},
    {"n": 23, "esp": "RED HORIZONTAL EN ESTRUCTURA DE HORMIGÓN", "uni": "M2"},
    {"n": 24, "esp": "RED VERTICAL EN ESTRUCTURA DE HORMIGÓN", "uni": "M2"},
    {"n": 25, "esp": "RED HORIZONTAL EN ESTRUCTURA METÁLICA", "uni": "M2"},
    {"n": 26, "esp": "PERÍMETRO EN CUBIERTA EN ESTRUCTURA METÁLICA", "uni": "ML"},
    {"n": 27, "esp": "PERÍMETRO CON 'T' DE MURO", "uni": "ML"},
    {"n": 28, "esp": "MARQUESINA", "uni": "ML"},
    {"n": 29, "esp": "PERÍMETRO CON RED A PILARES", "uni": "ML"},
    {"n": 30, "RED TIPO PANTALLA": "RED TIPO PANTALLA", "uni": "ML"},
    {"n": 31, "esp": "MOSQUITERA", "uni": "M2"},
    {"n": 32, "esp": "LONA TIPO PLÁSTICO / RAFIA", "uni": "M2"},
    {"n": 33, "esp": "PROTECCIÓN BARILLAS CON SETAS", "uni": "UDS"},
    {"n": 34, "esp": "HORAS DE MANTENIMIENTO", "uni": "UDS"},
    {"n": 35, "esp": "HORAS EXTRAS (FUERA DE JORNADA)", "uni": "UDS"},
    {"n": 36, "esp": "HORAS EXTRAS FESTIVAS", "uni": "UDS"},
    {"n": 37, "esp": "HORAS EXTRAS NOCTURNAS", "uni": "UDS"},
    {"n": 38, "esp": "HORAS EXTRAS FESTIVAS NOCTURNAS", "uni": "UDS"}
]

# --- INTERFAZ ---
st.sidebar.image("https://www.gravityworks.eu/wp-content/uploads/2021/04/logo-gravity-works.png", width=180)
lang = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "Marrouqui", "English"])

ui = {
    "Español": {"title": "Albarán de Obra", "worker": "Operario", "site": "Obra", "gen": "Generar Excel"},
    "Marrouqui": {"title": "قائمة العمل", "worker": "عامل", "site": "ورشة", "gen": "إرسال"},
    "English": {"title": "Work Report", "worker": "Worker", "site": "Site", "gen": "Generate Excel"}
}

st.title(f"🏗️ {ui[lang]['title']}")

with st.form("albaran_form"):
    c1, c2 = st.columns(2)
    worker = c1.text_input(ui[lang]['worker'], placeholder="Ej: Juan Pérez")
    site = c2.text_input(ui[lang]['site'], placeholder="Ej: Obra Sabadell")
    date = st.date_input("Fecha", datetime.now())
    
    st.divider()
    respuestas = {}

    # --- CAPÍTULO 1: REDES Y SEGURIDAD ---
    with st.expander("🛡️ CAP 1: REDES Y SEGURIDAD (1-10)", expanded=False):
        for i in range(0, 10):
            p = partidas_info[i]
            respuestas[p['n']] = st.number_input(f"{p['n']}. {p['esp']} ({p['uni']})", min_value=0.0, step=0.1, key=f"it_{p['n']}")

    # --- CAPÍTULO 2: HORCAS Y VERTICALES ---
    with st.expander("🏗️ CAP 2: HORCAS Y VERTICALES (11-15)", expanded=False):
        for i in range(10, 15):
            p = partidas_info[i]
            respuestas[p['n']] = st.number_input(f"{p['n']}. {p['esp']} ({p['uni']})", min_value=0.0, step=0.1, key=f"it_{p['n']}")

    # --- CAPÍTULO 3: PERÍMETROS Y ESCALERAS ---
    with st.expander("🚧 CAP 3: PERÍMETROS Y ESCALERAS", expanded=False):
        indices_cap3 = [15, 16, 18, 25, 26, 27, 28, 29] # Partidas 16, 17, 19, 26, 27, 28, 29, 30
        for idx in indices_cap3:
            p = partidas_info[idx]
            respuestas[p['n']] = st.number_input(f"{p['n']}. {p['esp']} ({p['uni']})", min_value=0.0, step=0.1, key=f"it_{p['n']}")

    # --- CAPÍTULO 4: ANCLAJE Y OTROS ---
    with st.expander("🔩 CAP 4: ANCLAJE Y OTROS", expanded=False):
        indices_cap4 = [17, 19, 20, 21, 22, 23, 24, 30, 31, 32] # Partidas 18, 20, 21, 22, 23, 24, 25, 31, 32, 33
        for idx in indices_cap4:
            p = partidas_info[idx]
            respuestas[p['n']] = st.number_input(f"{p['n']}. {p['esp']} ({p['uni']})", min_value=0.0, step=0.1, key=f"it_{p['n']}")

    # --- CAPÍTULO 5: MANTENIMIENTO Y HORAS (Abierto por defecto) ---
    with st.expander("🕒 CAP 5: MANTENIMIENTO Y HORAS EXTRAS", expanded=True):
        for i in range(33, 38): # Partidas 34 a 38
            p = partidas_info[i]
            respuestas[p['n']] = st.number_input(f"{p['n']}. {p['esp']} ({p['uni']})", min_value=0.0, step=0.5, key=f"it_{p['n']}")

    submitted = st.form_submit_button(ui[lang]['gen'])

# --- PROCESO FUERA DEL FORMULARIO ---
if submitted:
    if not worker or not site:
        st.error("Rellena Operario y Obra")
    else:
        final_data = []
        for p in partidas_info:
            val = respuestas[p['n']]
            if val > 0:
                final_data.append({"Ítem": p['n'], "Descripción": p['esp'], "Cantidad": val, "Unidad": p['uni']})
        
        if not final_data:
            st.warning("No hay datos introducidos")
        else:
            df = pd.DataFrame(final_data)
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='GravityWorks')
                wb = writer.book
                ws = writer.sheets['GravityWorks']
                fmt = wb.add_format({'bold': True, 'bg_color': '#003366', 'font_color': 'white'})
                for col, val in enumerate(df.columns):
                    ws.write(0, col, val, fmt)
                ws.set_column('B:B', 50) # Ancho para descripción
            
            fname = f"{site.replace(' ','_')}_{date}_{worker.replace(' ','_')}.xlsx"
            st.success("¡Albarán generado!")
            st.download_button("📥 Descargar Excel para Gerencia", output.getvalue(), file_name=fname)
