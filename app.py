import streamlit as st
import pandas as pd
from datetime import datetime
import io

# Configuración de la aplicación
st.set_page_config(page_title="Gravity Works - Digital Albaran", page_icon="🏗️", layout="centered")

# CSS personalizado para que se vea más profesional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; background-color: #004a99; color: white; height: 3em; font-weight: bold; }
    .stDownloadButton>button { width: 100%; background-color: #28a745; color: white; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# DICCIONARIO MULTILINGÜE DE LAS 38 PARTIDAS
data_partidas = {
    "Español": [
        "1 - RED HORIZONTAL BAJO ENCOFRADO", "2 - PROTECCIÓN PERIMETRAL CON BARANDILLAS + MORDAZAS",
        "3 - PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASES", "4 - PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASES (HUECOS)",
        "5 - PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASQUIS (HUECOS)", "6 - PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASQUIS (MURO)",
        "7 - PROTECCIÓN PERIMETRAL CON GARRAS DE MURO", "8 - PROTECCIÓN PERIMETRAL DE MURO PANTALLA",
        "9 - PROTECCIÓN HORIZONTAL CON REDES (HUECOS)", "10 - PROTECCIÓN VERTICAL CON REDES (HUECOS)",
        "11 - PRIMERA PUESTA DE HORCAS", "12 - ELEVACIÓN HORCAS", "13 - RED DE DESENCOFRADO",
        "14 - RED VERTICAL DE FACHADA", "15 - RED VERTICAL - ESCALERAS", "16 - PERÍMETRO CON BARANDILLAS EN ESCALERAS",
        "17 - RED EN VENTANAS", "18 - LINEA DE VIDA HORIZONTAL (MOCHILA)", "19 - LINEA DE VIDA VERTICAL (CUERDA)",
        "20 - PUNTOS DE ANCLAJE (TEXTILES)", "21 - PUNTOS DE ANCLAJE (METÁLICOS)", "22 - PUNTOS DE ANCLAJE CON CABO",
        "23 - RED HORIZONTAL EN ESTRUCTURA DE HORMIGÓN", "24 - RED VERTICAL EN ESTRUCTURA DE HORMIGÓN",
        "25 - RED HORIZONTAL EN ESTRUCTURA METÁLICA", "26 - PERÍMETRO EN CUBIERTA EN ESTRUCTURA METÁLICA",
        "27 - PERÍMETRO CON 'T' DE MURO", "28 - MARQUESINA", "29 - PERÍMETRO CON RED A PILARES",
        "30 - RED TIPO PANTALLA", "31 - MOSQUITERA", "32 - LONA TIPO PLÁSTICO / RAFIA",
        "33 - PROTECCIÓN BARILLAS CON SETAS", "34 - HORAS DE MANTENIMIENTO", "35 - HORAS EXTRAS (FUERA DE JORNADA)",
        "36 - HORAS EXTRAS FESTIVAS", "37 - HORAS EXTRAS NOCTURNAS", "38 - HORAS EXTRAS FESTIVAS NOCTURNAS"
    ],
    "Marrouqui": [
        "1 - شبكة أفقية تحت القوالب", "2 - حماية المحيط بالدرابزين + المشابك",
        "3 - حماية المحيط بالدرابزين + القواعد", "4 - حماية المحيط بالدرابزين + القواعد (الفجوات)",
        "5 - حماية المحيط بالدرابزين + باسكيس (الفجوات)", "6 - حماية المحيط بالدرابزين + باسكيس (الحائط)",
        "7 - حماية المحيط مع مخالب الحائط", "8 - حماية المحيط لحائط الحجاب",
        "9 - الحماية الأفقية بالشبكات (الفجوات)", "10 - الحماية العمودية بالشبكات (الفجوات)",
        "11 - الوضع الأول للمشانق", "12 - رفع المشانق", "13 - شبكة إزالة القوالب",
        "14 - شبكة الواجهة العمودية", "15 - شبكة عمودية - سلالم", "16 - المحيط مع درابزين في السلالم",
        "17 - شبكة في النوافذ", "18 - حبل الحياة الأفقي (حقيبة)", "19 - حبل الحياة العمودي (حبل)",
        "20 - نقاط مرساة (نسيج)", "21 - نقاط مرساة (معدنية)", "22 - نقاط مرساة مع كابل",
        "23 - شبكة أفقية في الهيكل الخرساني", "24 - شبكة عمودية في الهيكل الخرساني",
        "25 - شبكة أفقية في الهيكل المعدني", "26 - المحيط في سقف الهيكل المعدني",
        "27 - المحيط مع حرف T للحائط", "28 - مظلة واقية", "29 - المحيط مع شبكة للأعمدة",
        "30 - شبكة نوع الشاشة", "31 - ناموسية", "32 - قماش بلاستيك / رافيا",
        "33 - حماية القضبان بالفطر", "34 - ساعات الصيانة", "35 - ساعات إضافية (خارج الدوام)",
        "36 - ساعات إضافية في الأعياد", "37 - ساعات إضافية ليلية", "38 - ساعات إضافية ليلية في الأعياد"
    ],
    "English": [
        "1 - UNDER-SLAB HORIZONTAL NET", "2 - PERIMETER PROTECTION WITH RAILINGS + CLAMPS",
        "3 - PERIMETER PROTECTION WITH RAILINGS + BASES", "4 - PERIMETER PROTECTION WITH RAILINGS + BASES (VOIDS)",
        "5 - PERIMETER PROTECTION WITH RAILINGS + BASQUIS (VOIDS)", "6 - PERIMETER PROTECTION WITH RAILINGS + BASQUIS (WALL)",
        "7 - PERIMETER PROTECTION WITH WALL CLAWS", "8 - DIAPHRAGM WALL PERIMETER PROTECTION",
        "9 - HORIZONTAL PROTECTION WITH NETS (VOIDS)", "10 - VERTICAL PROTECTION WITH NETS (VOIDS)",
        "11 - FIRST SETTING OF GALLOWS", "12 - GALLOWS ELEVATION", "13 - STRIPPING NET",
        "14 - VERTICAL FAÇADE NET", "15 - VERTICAL NET - STAIRS", "16 - PERIMETER WITH RAILINGS ON STAIRS",
        "17 - WINDOW NETTING", "18 - HORIZONTAL LIFE LINE (BACKPACK)", "19 - VERTICAL LIFE LINE (ROPE)",
        "20 - ANCHOR POINTS (TEXTILE)", "21 - ANCHOR POINTS (METALLIC)", "22 - ANCHOR POINTS WITH LANYARD",
        "23 - HORIZONTAL NET IN CONCRETE STRUCTURE", "24 - VERTICAL NET IN CONCRETE STRUCTURE",
        "25 - HORIZONTAL NET IN STEEL STRUCTURE", "26 - ROOF PERIMETER IN STEEL STRUCTURE",
        "27 - PERIMETER WITH WALL 'T'", "28 - CANOPY", "29 - PERIMETER WITH NET TO PILLARS",
        "30 - SCREEN TYPE NET", "31 - MOSQUITO NET", "32 - PLASTIC TARP / RAFFIA",
        "33 - REBAR PROTECTION CAPS", "34 - MAINTENANCE HOURS", "35 - OVERTIME HOURS",
        "36 - HOLIDAY OVERTIME", "37 - NIGHT OVERTIME", "38 - NIGHT HOLIDAY OVERTIME"
    ]
}

# Interfaz de Selección de Idioma
st.sidebar.image("https://www.gravityworks.eu/wp-content/uploads/2021/04/logo-gravity-works.png", width=200)
lang = st.sidebar.selectbox("🌐 Seleccione Idioma / Choose Language", ["Español", "Marrouqui", "English"])

# Textos de la Interfaz
ui_texts = {
    "Español": {"title": "Parte de Trabajo Digital", "header": "Datos Generales", "worker": "Nombre del Operario", "site": "Nombre de la Obra", "submit": "Generar Excel", "success": "¡Generado con éxito!"},
    "Marrouqui": {"title": "تقرير العمل الرقمي", "header": "بيانات عامة", "worker": "اسم العامل", "site": "اسم المشروع", "submit": "إنشاء إكسل", "success": "تم بنجاح!"},
    "English": {"title": "Digital Work Report", "header": "General Data", "worker": "Worker Name", "site": "Site Name", "submit": "Generate Excel", "success": "Success!"}
}

st.title(ui_texts[lang]["title"])

# Formulario de Datos
with st.form("main_form"):
    st.subheader(ui_texts[lang]["header"])
    col1, col2 = st.columns(2)
    with col1:
        worker_name = st.text_input(ui_texts[lang]["worker"], placeholder="Ej: Juan Pérez")
        obra_name = st.text_input(ui_texts[lang]["site"], placeholder="Ej: Obra Sabadell Centra")
    with col2:
        fecha = st.date_input("Fecha / التاريخ", datetime.now())
        planta = st.text_input("Edificio / Planta / المبنى")

    st.divider()
    st.subheader("Items / Partidas / بنود")
    
    # Recogemos las cantidades de las 38 partidas
    respuestas = {}
    items_list = data_partidas[lang]
    
    # Dividimos en 2 columnas para que sea más corto el scroll
    c_part1, c_part2 = st.columns(2)
    for i, item in enumerate(items_list):
        with c_part1 if i < 19 else c_part2:
            respuestas[data_partidas["Español"][i]] = st.number_input(item, min_value=0.0, step=0.5, key=f"item_{i}")

    st.divider()
    comentarios = st.text_area("Otros Conceptos / Material Roto")

    # --- ESTO VA DENTRO DEL FORMULARIO ---
    submitted = st.form_submit_button(ui_texts[lang]["submit"])

# --- ESTO VA FUERA DEL FORMULARIO (Saca la sangría/identación) ---
if submitted:
    if not worker_name or not obra_name:
        st.error("Por favor, rellena el nombre del operario y la obra.")
    else:
        # 1. Crear DataFrame filtrando solo lo que tenga cantidad > 0
        df = pd.DataFrame([
            {"Partida": k, "Cantidad": v} for k, v in respuestas.items() if v > 0
        ])
        
        if df.empty:
            st.warning("No has introducido ninguna cantidad.")
        else:
            # 2. Generar Excel en memoria
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Albaran')
                
                # Formatos estéticos
                workbook = writer.book
                worksheet = writer.sheets['Albaran']
                header_format = workbook.add_format({'bold': True, 'bg_color': '#003366', 'font_color': 'white'})
                
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                worksheet.set_column('A:A', 60) # Ajustar ancho de columna
            
            # 3. Nombre del archivo
            file_name = f"{obra_name.replace(' ','_')}_{fecha}_{worker_name.replace(' ','_')}.xlsx"
            
            # 4. Mostrar éxito y Botón de Descarga (FUERA del form)
            st.success(ui_texts[lang]["success"])
            st.download_button(
                label=f"📥 {ui_texts[lang]['submit']} (Excel)",
                data=output.getvalue(),
                file_name=file_name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
