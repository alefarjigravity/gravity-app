import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuración de página
st.set_page_config(page_title="Gravity Works App", page_icon="🏗️")

# Diccionario de Idiomas
texts = {
    "Español": {
        "title": "Parte de Trabajo",
        "worker": "Operario",
        "job": "Obra",
        "date": "Fecha",
        "submit": "Generar Albarán Excel",
        "items": ["Red Horizontal Bajo Encofrado", "Protección Perimetral Mordazas", "Horas Extras"]
    },
    "Marrouqui": {
        "title": "تقرير العمل",
        "worker": "العامل",
        "job": "ورشة العمل",
        "date": "تاريخ",
        "submit": "إنشاء ملف إكسل",
        "items": ["شبكة أمان أفقية", "حماية المحيط", "ساعات إضافية"]
    },
    "English": {
        "title": "Work Report",
        "worker": "Worker Name",
        "job": "Site Name",
        "date": "Date",
        "submit": "Generate Excel Report",
        "items": ["Horizontal Safety Net", "Perimeter Protection", "Extra Hours"]
    }
}

# Selección de Idioma
lang = st.sidebar.selectbox("🌐 Idioma / Language / لغة", ["Español", "Marrouqui", "English"])
t = texts[lang]

st.title(f"🏗️ {t['title']}")
st.write("Gravity Works Proteccions Col·lectives")

# Formulario Principal
with st.form("albaran_form"):
    col1, col2 = st.columns(2)
    with col1:
        worker = st.text_input(t['worker'])
        job = st.text_input(t['job'])
    with col2:
        date = st.date_input(t['date'], datetime.now())
        plant = st.text_input("Edificio / Planta")

    st.divider()
    st.subheader("Unidades de Obra")
    
    # Ejemplo de partidas (Aquí pondrías las 38)
    cantidades = {}
    for i, item in enumerate(t['items']):
        cantidades[item] = st.number_input(f"{item}", min_value=0.0, step=1.0)

    submitted = st.form_submit_button(t['submit'])

    if submitted:
        # CREAR EXCEL EN MEMORIA
        df = pd.DataFrame({
            "Concepto": cantidades.keys(),
            "Cantidad": cantidades.values()
        })
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Albaran')
        
        excel_data = output.getvalue()
        
        # Nombre del archivo PRO
        file_name = f"{job.replace(' ','_')}_{date}_{worker.replace(' ','_')}.xlsx"
        
        st.success(f"✅ Albarán generado: {file_name}")
        st.download_button(
            label="📥 Descargar Excel para Gerencia",
            data=excel_data,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
