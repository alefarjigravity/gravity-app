import streamlit as st
import pandas as pd
from datetime import datetime
import io
import urllib.parse
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from PIL import Image
import os

# Configuración
st.set_page_config(page_title="Gravity Works Pro", page_icon="🏗️")

# --- BASE DE DATOS MAESTRA ---
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
    [22, "PUNTOS DE ANCLAJE CON CABO", "نقاط مرساة con كابل", "ANCHOR POINTS + LANYARD", "UDS"],
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

# --- TRADUCCIONES ---
ui = {
    "Español": {"t": "Albarán Digital", "op": "Operario", "ob": "Obra", "btn": "GENERAR DOCUMENTOS", "obs": "Observaciones", "sign": "Firma del Responsable", "c1": "CAP 1: REDES Y SEGURIDAD", "c2": "CAP 2: HORCAS Y VERTICALES", "c3": "CAP 3: PERÍMETROS", "c4": "CAP 4: ANCLAJES Y OTROS", "c5": "CAP 5: HORAS EXTRAS"},
    "Marrouqui": {"t": "قائمة العمل الرقمية", "op": "عامل", "ob": "ورشة", "btn": "إنشاء المستندات", "obs": "ملاحظات", "sign": "توقيع المسؤول", "c1": "1: الحماية", "c2": "2: المشانق", "c3": "3: المحيط", "c4": "4: المراسي", "c5": "5: ساعات إضافية"},
    "English": {"t": "Digital Report", "op": "Worker", "ob": "Site", "btn": "GENERATE DOCUMENTS", "obs": "Notes", "sign": "Signature", "c1": "CAP 1: SAFETY NETS", "c2": "CAP 2: GALLOWS", "c3": "CAP 3: PERIMETERS", "c4": "CAP 4: ANCHORS", "c5": "CAP 5: OVERTIME"}
}

lang = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "Marrouqui", "English"])
l_idx = {"Español": 1, "Marrouqui": 2, "English": 3}[lang]

st.title(ui[lang]["t"])

# --- DATOS GENERALES ---
c1, c2 = st.columns(2)
worker = c1.text_input(ui[lang]["op"])
site = c2.text_input(ui[lang]["ob"])
date = st.date_input("Fecha", datetime.now())

st.divider()
resp = {}

# CAPÍTULOS
with st.expander(ui[lang]["c1"], expanded=False):
    for i in range(0, 10):
        p = partidas_master[i]
        resp[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c2"], expanded=False):
    for i in range(10, 15):
        p = partidas_master[i]
        resp[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c3"], expanded=False):
    idx_c3 = [15, 16, 18, 25, 26, 27, 28, 29]
    for idx in idx_c3:
        p = partidas_master[idx]
        resp[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c4"], expanded=False):
    idx_c4 = [17, 19, 20, 21, 22, 23, 24, 30, 31, 32]
    for idx in idx_c4:
        p = partidas_master[idx]
        resp[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c5"], expanded=False):
    for i in range(33, 38):
        p = partidas_master[i]
        resp[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

obs = st.text_area(ui[lang]["obs"])

# FIRMA
st.subheader(ui[lang]["sign"])
canvas_result = st_canvas(
    stroke_width=3, stroke_color="#000000", background_color="#eeeeee",
    height=150, width=400, drawing_mode="freedraw", key="canvas"
)

if st.button(ui[lang]["btn"]):
    if not worker or not site:
        st.error("Faltan datos")
    else:
        # Generar datos en ESPAÑOL
        rows = [{"Cód": p[0], "Descripción": p[1], "Cant": resp[p[0]], "Uni": p[4]} for p in partidas_master if resp[p[0]] > 0]
        df = pd.DataFrame(rows)
        
        # Procesar Firma
        img_firma = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        img_byte = io.BytesIO()
        img_firma.save(img_byte, format="PNG")
        
        # --- EXCEL ---
        xlsx_io = io.BytesIO()
        with pd.ExcelWriter(xlsx_io, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Albaran', startrow=5)
            wb, ws = writer.book, writer.sheets['Albaran']
            b_f = wb.add_format({'bold': True})
            ws.write(0, 0, f"OPERARIO: {worker.upper()}", b_f)
            ws.write(1, 0, f"OBRA: {site.upper()}", b_f)
            ws.write(2, 0, f"FECHA: {date}", b_f)
            ws.insert_image(len(df)+10, 0, 'f.png', {'image_data': img_byte, 'x_scale': 0.4, 'y_scale': 0.4})
            ws.set_column('B:B', 50)
        
        # --- PDF ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "GRAVITY WORKS - ALBARAN", 0, 1, 'C')
        pdf.set_font("Arial", '', 10)
        pdf.ln(5)
        pdf.cell(0, 7, f"Operario: {worker}", 0, 1)
        pdf.cell(0, 7, f"Obra: {site}", 0, 1)
        pdf.ln(5)
        for _, r in df.iterrows():
            pdf.cell(0, 7, f"{r['Cód']} - {r['Descripción']}: {r['Cant']} {r['Uni']}", 0, 1)
        pdf.ln(5)
        pdf.multi_cell(0, 5, f"Obs: {obs}")
        with open("f_temp.png", "wb") as f: f.write(img_byte.getvalue())
        pdf.image("f_temp.png", w=50)
        pdf_bytes = pdf.output(dest='S').encode('latin1')

        # --- MOSTRAR BOTONES DE DESCARGA ---
        st.success("✅ ¡Hecho! Descarga y comparte:")
        f_name = f"{worker}_{site}_{date.strftime('%d-%m')}"
        
        col_ex, col_pdf = st.columns(2)
        with col_ex:
            st.download_button("📊 EXCEL (Interno)", xlsx_io.getvalue(), f"{f_name}.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with col_pdf:
            st.download_button("📄 PDF (Cliente)", pdf_bytes, f"{f_name}.pdf", "application/pdf")
        
        # Link WhatsApp Rápido
        msg = f"Hola, envío albarán de {worker} en obra {site}."
        st.markdown(f'<a href="https://wa.me/?text={urllib.parse.quote(msg)}" target="_blank"><button style="width:100%;background:#25D366;color:white;border:none;padding:10px;border-radius:5px;cursor:pointer;">📱 AVISAR POR WHATSAPP</button></a>', unsafe_allow_html=True)
