import streamlit as st
import pandas as pd
from datetime import datetime
import io
import urllib.parse

st.set_page_config(page_title="Gravity Works - Pro", page_icon="🏗️")

# --- BASE DE DATOS TRILINGÜE ---
# Estructura: [ID, Español, Árabe, Inglés, Unidad]
partidas_master = [
    [1, "RED HORIZONTAL BAJO ENCOFRADO", "شبكة أفقية تحت القوالب", "UNDER-SLAB HORIZONTAL NET", "M2"],
    [2, "PROTECCIÓN PERIMETRAL CON BARANDILLAS + MORDAZAS", "حماية المحيط بالدرابزين + المشابك", "PERIMETER PROTECTION + CLAMPS", "ML"],
    [3, "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASES", "حماية المحيط بالدرابزين + القواعد", "PERIMETER PROTECTION + BASES", "ML"],
    [4, "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASES (HUECOS)", "حماية المحيط (الفجوات)", "PERIMETER PROTECTION (VOIDS)", "ML"],
    [5, "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASQUIS (HUECOS)", "حماية المحيط + باسكيس (الفجوات)", "PERIMETER PROTECTION + BASQUIS", "ML"],
    [6, "PROTECCIÓN PERIMETRAL CON BARANDILLAS + BASQUIS (MURO)", "حماية المحيط + باسكيس (الحائط)", "PERIMETER PROTECTION + BASQUIS (WALL)", "ML"],
    [7, "PROTECCIÓN PERIMETRAL CON GARRAS DE MURO", "حماية المحيط مع مخالب الحائط", "PERIMETER PROTECTION WITH WALL CLAWS", "ML"],
    [8, "PROTECCIÓN PERIMETRAL DE MURO PANTALLA", "حماية المحيط لحائط الحجاب", "DIAPHRAGM WALL PERIMETER", "ML"],
    [9, "PROTECCIÓN HORIZONTAL CON REDES (HUECOS)", "الحماية الأفقية بالشبكات", "HORIZONTAL NET PROTECTION", "M2"],
    [10, "PROTECCIÓN VERTICAL CON REDES (HUECOS)", "الحماية العمودية بالشبكات", "VERTICAL NET PROTECTION", "M2"],
    [11, "PRIMERA PUESTA DE HORCAS", "الوضع الأول للمشانق", "GALLOWS FIRST SETTING", "ML"],
    [12, "ELEVACIÓN HORCAS", "رفع المشانق", "GALLOWS ELEVATION", "ML"],
    [13, "RED DE DESENCOFRADO", "شبكة إزالة القوالب", "STRIPPING NET", "ML"],
    [14, "RED VERTICAL DE FACHADA", "شبكة الواجهة العمودية", "VERTICAL FAÇADE NET", "M2"],
    [15, "RED VERTICAL - ESCALERAS", "شبكة عمودية - سلالم", "VERTICAL NET - STAIRS", "M2"],
    [16, "PERÍMETRO CON BARANDILLAS EN ESCALERAS", "المحيط مع درابزين في السلالم", "STAIRS PERIMETER RAILINGS", "ML"],
    [17, "RED EN VENTANAS", "شبكة في النوافذ", "WINDOW NETTING", "UDS"],
    [18, "LINEA DE VIDA HORIZONTAL (MOCHILA)", "حبل الحياة الأفقي", "HORIZONTAL LIFE LINE", "UDS"],
    [19, "LINEA DE VIDA VERTICAL (CUERDA)", "حبل الحياة العمودي", "VERTICAL LIFE LINE", "ML"],
    [20, "PUNTOS DE ANCLAJE (TEXTILES)", "نقاط مرساة (نسيج)", "ANCHOR POINTS (TEXTILE)", "UDS"],
    [21, "PUNTOS DE ANCLAJE (METÁLICOS)", "نقاط مرساة (معدنية)", "ANCHOR POINTS (METALLIC)", "UDS"],
    [22, "PUNTOS DE ANCLAJE CON CABO", "نقاط مرساة مع كابل", "ANCHOR POINTS + LANYARD", "UDS"],
    [23, "RED HORIZONTAL EN ESTRUCTURA DE HORMIGÓN", "شبكة أفقية في الخرسانة", "HORIZONTAL NET CONCRETE", "M2"],
    [24, "RED VERTICAL EN ESTRUCTURA DE HORMIGÓN", "شبكة عمودية في الخرسانة", "VERTICAL NET CONCRETE", "M2"],
    [25, "RED HORIZONTAL EN ESTRUCTURA METÁLICA", "شبكة أفقية في الهيكل المعدني", "HORIZONTAL NET STEEL", "M2"],
    [26, "PERÍMETRO EN CUBIERTA EN ESTRUCTURA METÁLICA", "المحيط في سقف معدني", "ROOF PERIMETER STEEL", "ML"],
    [27, "PERÍMETRO CON 'T' DE MURO", "المحيط مع حرف T", "PERIMETER WITH WALL 'T'", "ML"],
    [28, "MARQUESINA", "مظلة واقية", "CANOPY", "ML"],
    [29, "PERÍMETRO CON RED A PILARES", "المحيط مع شبكة للأعمدة", "COLUMN NET PERIMETER", "ML"],
    [30, "RED TIPO PANTALLA", "شبكة نوع الشاشة", "SCREEN TYPE NET", "ML"],
    [31, "MOSQUITERA", "ناموسية", "MOSQUITO NET", "M2"],
    [32, "LONA TIPO PLÁSTICO / RAFIA", "قماش بلاستيك", "PLASTIC TARP", "M2"],
    [33, "PROTECCIÓN BARILLAS CON SETAS", "حماية القضبان بالفطر", "REBAR CAPS", "UDS"],
    [34, "HORAS DE MANTENIMIENTO", "ساعات الصيانة", "MAINTENANCE HOURS", "UDS"],
    [35, "HORAS EXTRAS (FUERA DE JORNADA)", "ساعات إضافية", "OVERTIME HOURS", "UDS"],
    [36, "HORAS EXTRAS FESTIVAS", "إضافي أعياد", "HOLIDAY OVERTIME", "UDS"],
    [37, "HORAS EXTRAS NOCTURNAS", "إضافي ليلي", "NIGHT OVERTIME", "UDS"],
    [38, "HORAS EXTRAS FESTIVAS NOCTURNAS", "إضافي ليلي أعياد", "NIGHT HOLIDAY OVERTIME", "UDS"]
]

# --- LÓGICA DE INTERFAZ ---
st.sidebar.image("https://www.gravityworks.eu/wp-content/uploads/2021/04/logo-gravity-works.png", width=180)
lang_choice = st.sidebar.selectbox("🌐 Seleccione Idioma", ["Español", "Marrouqui", "English"])

lang_idx = {"Español": 1, "Marrouqui": 2, "English": 3}[lang_choice]

ui = {
    "Español": {"t": "Albarán Digital", "op": "Operario", "ob": "Obra", "btn": "1. Generar Excel", "ws": "2. Avisar por WhatsApp", "obs": "Observaciones"},
    "Marrouqui": {"t": "قائمة العمل الرقمية", "op": "عامل", "ob": "ورشة", "btn": "1. إنشاء إكسل", "ws": "2. واتساب", "obs": "ملاحظات"},
    "English": {"t": "Digital Report", "op": "Worker", "ob": "Site", "btn": "1. Generate Excel", "ws": "2. Send WhatsApp", "obs": "Notes"}
}

st.title(ui[lang_choice]["t"])

with st.form("main_form"):
    c1, c2 = st.columns(2)
    worker = c1.text_input(ui[lang_choice]["op"])
    site = c2.text_input(ui[lang_choice]["ob"])
    date = st.date_input("Fecha", datetime.now())
    
    st.divider()
    respuestas = {}
    
    # Capítulos agrupados
    with st.expander("📂 Partidas / Items", expanded=True):
        for p in partidas_master:
            respuestas[p[0]] = st.number_input(f"{p[0]}. {p[lang_idx]} ({p[4]})", min_value=0.0, step=0.1, key=f"p_{p[0]}")

    obs = st.text_area(ui[lang_choice]["obs"])
    submitted = st.form_submit_button(ui[lang_choice]["btn"])

if submitted:
    if not worker or not site:
        st.error("Rellene los datos básicos")
    else:
        # Filtrar datos con valor > 0
        final_list = []
        for p in partidas_master:
            cant = respuestas[p[0]]
            if cant > 0:
                final_list.append({"Cód": p[0], "Descripción": p[lang_idx], "Cant": cant, "Uni": p[4]})
        
        df = pd.DataFrame(final_list)
        
        # EXCEL CON ENCABEZADOS DE PERSONA Y OBRA
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Crear una hoja vacía para escribir manualmente los encabezados
            df.to_excel(writer, index=False, sheet_name='Albaran', startrow=5)
            
            workbook = writer.book
            worksheet = writer.sheets['Albaran']
            
            # Formatos
            bold = workbook.add_format({'bold': True, 'font_size': 12})
            header_fmt = workbook.add_format({'bold': True, 'bg_color': '#003366', 'font_color': 'white'})
            
            # Escribir los datos del punto 3
            worksheet.write(0, 0, f"OPERARIO: {worker.upper()}", bold)
            worksheet.write(1, 0, f"OBRA: {site.upper()}", bold)
            worksheet.write(2, 0, f"FECHA: {date.strftime('%d/%m/%Y')}", bold)
            
            # Formatear tabla de partidas
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(5, col_num, value, header_fmt)
            
            if obs:
                worksheet.write(len(df)+7, 0, "OBSERVACIONES:", bold)
                worksheet.write(len(df)+8, 0, obs)
            
            worksheet.set_column('B:B', 45)

        st.success("✅ Excel generado con encabezados.")
        st.download_button("📥 DESCARGAR EXCEL", output.getvalue(), file_name=f"{site}_{date}.xlsx")
        
        # BOTÓN DE WHATSAPP (Punto 2)
        msg = f"Hola, envío albarán de Gravity Works.\n🏗️ Obra: {site}\n👷 Operario: {worker}\n📅 Fecha: {date}"
        encoded_msg = urllib.parse.quote(msg)
        # Puedes poner un número fijo aquí, ej: phone=34600000000
        ws_url = f"https://wa.me/?text={encoded_msg}"
        
        st.markdown(f"""
            <a href="{ws_url}" target="_blank">
                <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer;">
                    📱 2. AVISAR POR WHATSAPP (A Gerencia)
                </button>
            </a>
            """, unsafe_allow_html=True)
