import streamlit as st
import pandas as pd
from datetime import datetime
import io
import base64
import urllib.parse
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from PIL import Image
import os

# Configuración de la página
st.set_page_config(page_title="Gravity Works Pro", page_icon="🏗️")

# --- BASE DE DATOS MAESTRA (38 PARTIDAS) ---
# [ID, Español, Marrouquí, Inglés, Unidad]
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

# --- UI TRANSLATIONS ---
ui = {
    "Español": {"t": "Albarán Digital", "op": "Operario", "ob": "Obra", "btn": "Generar Albaranes", "obs": "Observaciones", "sign": "Firma del Responsable", "c1": "CAP 1: REDES Y SEGURIDAD", "c2": "CAP 2: HORCAS Y VERTICALES", "c3": "CAP 3: PERÍMETROS", "c4": "CAP 4: ANCLAJES Y OTROS", "c5": "CAP 5: HORAS EXTRAS"},
    "Marrouqui": {"t": "قائمة العمل الرقمية", "op": "عامل", "ob": "ورشة", "btn": "إنشاء المستندات", "obs": "ملاحظات", "sign": "توقيع المسؤول", "c1": "1: الحماية", "c2": "2: المشانق", "c3": "3: المحيط", "c4": "4: المراسي", "c5": "5: ساعات إضافية"},
    "English": {"t": "Digital Report", "op": "Worker", "ob": "Site", "btn": "Generate Documents", "obs": "Notes", "sign": "Signature", "c1": "CAP 1: SAFETY NETS", "c2": "CAP 2: GALLOWS", "c3": "CAP 3: PERIMETERS", "c4": "CAP 4: ANCHORS", "c5": "CAP 5: OVERTIME"}
}

st.sidebar.image("https://www.gravityworks.eu/wp-content/uploads/2021/04/logo-gravity-works.png", width=180)
lang = st.sidebar.selectbox("🌐 Seleccione Idioma", ["Español", "Marrouqui", "English"])
l_idx = {"Español": 1, "Marrouqui": 2, "English": 3}[lang]

st.title(ui[lang]["t"])

# --- DATOS GENERALES ---
c1, c2 = st.columns(2)
worker = c1.text_input(ui[lang]["op"])
site = c2.text_input(ui[lang]["ob"])
date = st.date_input("Fecha", datetime.now())

st.divider()
res = {}

# --- CAPÍTULOS (EXPANDERS) ---
with st.expander(ui[lang]["c1"], expanded=False):
    for i in range(0, 10):
        p = partidas_master[i]
        res[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c2"], expanded=False):
    for i in range(10, 15):
        p = partidas_master[i]
        res[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c3"], expanded=False):
    indices_c3 = [15, 16, 18, 25, 26, 27, 28, 29]
    for idx in indices_c3:
        p = partidas_master[idx]
        res[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c4"], expanded=False):
    indices_c4 = [17, 19, 20, 21, 22, 23, 24, 30, 31, 32]
    for idx in indices_c4:
        p = partidas_master[idx]
        res[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

with st.expander(ui[lang]["c5"], expanded=False):
    for i in range(33, 38):
        p = partidas_master[i]
        res[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

obs = st.text_area(ui[lang]["obs"])

# --- FIRMA ---
st.subheader(ui[lang]["sign"])
canvas_result = st_canvas(
    stroke_width=3, stroke_color="#000000", background_color="#eeeeee",
    height=150, width=400, drawing_mode="freedraw", key="canvas"
)

# --- PROCESO ---
if st.button(ui[lang]["btn"]):
    if not worker or not site:
        st.error("Rellene Operario y Obra")
    elif canvas_result.image_data is None:
        st.warning("Firme antes de generar")
    else:
        # Filtrar datos (Siempre en ESPAÑOL para documentos)
        data_rows = []
        for p in partidas_master:
            cant = res[p[0]]
            if cant > 0:
                data_rows.append({"Cód": p[0], "Descripción": p[1], "Cant": cant, "Uni": p[4]})
        
        df = pd.DataFrame(data_rows)
        
        # Procesar firma
        img_firma = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        img_buffer = io.BytesIO()
        img_firma.save(img_buffer, format="PNG")
        
        # --- EXCEL ---
        xlsx_io = io.BytesIO()
        with pd.ExcelWriter(xlsx_io, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Albaran', startrow=5)
            wb, ws = writer.book, writer.sheets['Albaran']
            b_fmt = wb.add_format({'bold': True})
            h_fmt = wb.add_format({'bold': True, 'bg_color': '#003366', 'font_color': 'white'})
            
            ws.write(0, 0, f"OPERARIO: {worker.upper()}", b_fmt)
            ws.write(1, 0, f"OBRA: {site.upper()}", b_fmt)
            ws.write(2, 0, f"FECHA: {date.strftime('%d/%m/%Y')}", b_fmt)
            
            for col_num, val in enumerate(df.columns.values):
                ws.write(5, col_num, val, h_fmt)
            
            if obs:
                ws.write(len(df)+7, 0, "OBSERVACIONES:", b_fmt)
                ws.write(len(df)+8, 0, obs)
            
            ws.insert_image(len(df)+10, 0, 'f.png', {'image_data': img_buffer, 'x_scale': 0.4, 'y_scale': 0.4})
            ws.set_column('B:B', 50)

        # --- PDF (FPDF) ---
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "GRAVITY WORKS - ALBARAN DE TRABAJO", 0, 1, 'C')
        pdf.ln(5)
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 7, f"Operario: {worker}", 0, 1)
        pdf.cell(0, 7, f"Obra: {site}", 0, 1)
        pdf.cell(0, 7, f"Fecha: {date}", 0, 1)
        pdf.ln(5)
        
        # Tabla PDF
        pdf.set_fill_color(0, 51, 102)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(10, 8, "Id", 1, 0, 'C', True)
        pdf.cell(130, 8, "Partida", 1, 0, 'L', True)
        pdf.cell(20, 8, "Cant", 1, 0, 'C', True)
        pdf.cell(20, 8, "Uni", 1, 1, 'C', True)
        
        pdf.set_text_color(0)
        for _, row in df.iterrows():
            pdf.cell(10, 7, str(row['Cód']), 1)
            pdf.cell(130, 7, str(row['Descripción']), 1)
            pdf.cell(20, 7, str(row['Cant']), 1)
            pdf.cell(20, 7, str(row['Uni']), 1, 1)
        
        pdf.ln(5)
        pdf.multi_cell(0, 5, f"Observaciones: {obs if obs else '-'}")
        
        # Firma PDF
        with open("f.png", "wb") as f: f.write(img_buffer.getvalue())
        pdf.ln(5)
        pdf.cell(0, 7, "Firma del Responsable:", 0, 1)
        pdf.image("f.png", w=50)
        pdf_bytes = pdf.output(dest='S').encode('latin1')

        # --- COMPARTIR ---
        st.success("✅ Generados correctamente")
        f_base = f"{worker.replace(' ','_')}_{site.replace(' ','_')}_{date.strftime('%d-%m-%Y')}"
        
        def btn_share(data, fname, label, color):
            b64 = base64.b64encode(data).decode()
            uid = label.replace(" ","")
            return f"""
                <script>
                async function s_{uid}(){{
                    const b = "{b64}";
                    const r = await fetch(`data:application/octet-stream;base64,${{b}}`);
                    const bl = await r.blob();
                    const f = new File([bl], "{fname}", {{type: bl.type}});
                    if(navigator.share){{ await navigator.share({{files:[f]}}); }}
                    else {{ alert("Navegador no compatible"); }}
                }}
                </script>
                <button onclick="s_{uid}()" style="width:100%;background:{color};color:white;border:none;padding:12px;border-radius:8px;font-weight:bold;cursor:pointer;margin-bottom:8px;">{label}</button>
            """
        
        st.components.v1.html(btn_share(xlsx_io.getvalue(), f"{f_base}.xlsx", "📊 COMPARTIR EXCEL (Administración)", "#003366"), height=70)
        st.components.v1.html(btn_share(pdf_bytes, f"{f_base}.pdf", "📄 COMPARTIR PDF (Cliente)", "#c0392b"), height=70)
