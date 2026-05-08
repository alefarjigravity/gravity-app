import streamlit as st
import pandas as pd
from datetime import datetime
import io
import urllib.parse

st.set_page_config(page_title="Gravity Works - Pro", page_icon="🏗️")

# --- BASE DE DATOS TRILINGÜE (38 PARTIDAS) ---
# Hemos asegurado que cada comilla esté en su sitio para evitar el SyntaxError
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

# --- INTERFAZ ---
st.sidebar.image("https://www.gravityworks.eu/wp-content/uploads/2021/04/logo-gravity-works.png", width=180)
lang_choice = st.sidebar.selectbox("🌐 Seleccione Idioma", ["Español", "Marrouqui", "English"])
# Mapeo de columna según idioma
lang_idx = {"Español": 1, "Marrouqui": 2, "English": 3}[lang_choice]

ui = {
    "Español": {"t": "Albarán Digital", "op": "Operario", "ob": "Obra", "btn": "1. Generar Excel", "obs": "Observaciones", "c1": "CAP 1: REDES Y SEGURIDAD", "c2": "CAP 2: HORCAS Y VERTICALES", "c3": "CAP 3: PERÍMETROS", "c4": "CAP 4: ANCLAJES Y OTROS", "c5": "CAP 5: HORAS EXTRAS"},
    "Marrouqui": {"t": "قائمة العمل الرقمية", "op": "عامل", "ob": "ورشة", "btn": "1. إنشاء إكسل", "obs": "ملاحظات", "c1": "1: الحماية", "c2": "2: المشانق", "c3": "3: المحيط", "c4": "4: المراسي", "c5": "5: ساعات إضافية"},
    "English": {"t": "Digital Report", "op": "Worker", "ob": "Site", "btn": "1. Generate Excel", "obs": "Notes", "c1": "CAP 1: SAFETY NETS", "c2": "CAP 2: GALLOWS", "c3": "CAP 3: PERIMETERS", "c4": "CAP 4: ANCHORS", "c5": "CAP 5: OVERTIME"}
}

st.title(ui[lang_choice]["t"])

# Iniciamos el Formulario
with st.form("main_form"):
    c1, c2 = st.columns(2)
    worker = c1.text_input(ui[lang_choice]["op"])
    site = c2.text_input(ui[lang_choice]["ob"])
    date = st.date_input("Fecha", datetime.now())
    
    st.divider()
    respuestas = {}
    
    # CAPÍTULO 1 (Ítems 1-10)
    with st.expander(ui[lang_choice]["c1"], expanded=False):
        for i in range(0, 10):
            p = partidas_master[i]
            respuestas[p[0]] = st.number_input(f"{p[0]}. {p[lang_idx]} ({p[4]})", min_value=0.0, step=0.1, key=f"p_{p[0]}")

    # CAPÍTULO 2 (Ítems 11-15)
    with st.expander(ui[lang_choice]["c2"], expanded=False):
        for i in range(10, 15):
            p = partidas_master[i]
            respuestas[p[0]] = st.number_input(f"{p[0]}. {p[lang_idx]} ({p[4]})", min_value=0.0, step=0.1, key=f"p_{p[0]}")

    # CAPÍTULO 3 (Lógica de perímetros)
    with st.expander(ui[lang_choice]["c3"], expanded=False):
        idx_c3 = [15, 16, 18, 25, 26, 27, 28, 29]
        for idx in idx_c3:
            p = partidas_master[idx]
            respuestas[p[0]] = st.number_input(f"{p[0]}. {p[lang_idx]} ({p[4]})", min_value=0.0, step=0.1, key=f"p_{p[0]}")

    # CAPÍTULO 4 (Anclajes y Otros)
    with st.expander(ui[lang_choice]["c4"], expanded=False):
        idx_c4 = [17, 19, 20, 21, 22, 23, 24, 30, 31, 32]
        for idx in idx_c4:
            p = partidas_master[idx]
            respuestas[p[0]] = st.number_input(f"{p[0]}. {p[lang_idx]} ({p[4]})", min_value=0.0, step=0.1, key=f"p_{p[0]}")

    # CAPÍTULO 5 (Horas - ABIERTO POR DEFECTO)
    with st.expander(ui[lang_choice]["c5"], expanded=True):
        for i in range(33, 38):
            p = partidas_master[i]
            respuestas[p[0]] = st.number_input(f"{p[0]}. {p[lang_idx]} ({p[4]})", min_value=0.0, step=0.5, key=f"p_{p[0]}")

    obs = st.text_area(ui[lang_choice]["obs"])
    
    # EL BOTÓN DE ENVIAR DEBE ESTAR AQUÍ DENTRO (Última línea del with st.form)
    submitted = st.form_submit_button(ui[lang_choice]["btn"])

# --- LÓGICA TRAS PULSAR ENVIAR (FUERA DEL FORMULARIO) ---
if submitted:
    if not worker or not site:
        st.error("Por favor, rellena el nombre del operario y la obra.")
    else:
        # Generamos la lista de lo que se ha trabajado
        datos_informe = []
        for p in partidas_master:
            cantidad = respuestas[p[0]]
            if cantidad > 0:
                datos_informe.append({
                    "Cód": p[0], 
                    "Descripción": p[lang_idx], 
                    "Cant": cantidad, 
                    "Uni": p[4]
                })
        
        if not datos_informe and not obs:
            st.warning("No hay datos para generar el albarán.")
        else:
            df = pd.DataFrame(datos_informe)
            
            # Generación del Excel Profesional
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Albaran', startrow=5)
                workbook = writer.book
                worksheet = writer.sheets['Albaran']
                
                # Formatos
                bold = workbook.add_format({'bold': True})
                header_fmt = workbook.add_format({'bold': True, 'bg_color': '#003366', 'font_color': 'white'})
                
                # Encabezados de Obra
                worksheet.write(0, 0, f"OPERARIO: {worker.upper()}", bold)
                worksheet.write(1, 0, f"OBRA: {site.upper()}", bold)
                worksheet.write(2, 0, f"FECHA: {date.strftime('%d/%m/%Y')}", bold)
                
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(5, col_num, value, header_fmt)
                
                if obs:
                    row_obs = len(df) + 7
                    worksheet.write(row_obs, 0, "OBSERVACIONES / MATERIAL ROTO:", bold)
                    worksheet.write(row_obs + 1, 0, obs)
                
                worksheet.set_column('B:B', 50)

            st.success("✅ Excel preparado.")
            st.download_button(
                label="📥 DESCARGAR EXCEL",
                data=output.getvalue(),
                file_name=f"{site}_{date}_{worker}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Link de WhatsApp
            msg_wa = f"Hola, envío albarán de Gravity Works.\n🏗️ Obra: {site}\n👷 Operario: {worker}\n📅 Fecha: {date}"
            encoded_msg = urllib.parse.quote(msg_wa)
            ws_url = f"https://wa.me/?text={encoded_msg}"
            
            st.markdown(f"""
                <a href="{ws_url}" target="_blank">
                    <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer; margin-top:10px;">
                        📱 2. AVISAR POR WHATSAPP
                    </button>
                </a>
                """, unsafe_allow_html=True)
