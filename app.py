import streamlit as st
import pandas as pd
from datetime import datetime
import io
import base64
from streamlit_drawable_canvas import st_canvas
from fpdf import FPDF
from PIL import Image
import os

# Configuración de la App
st.set_page_config(page_title="Gravity Works Pro", page_icon="🏗️", layout="centered")

# --- CARGA DEL LOGO (logo.png en GitHub) ---
def cargar_logo():
    if os.path.exists("logo.png"):
        return "logo.png"
    return None

# --- BASE DE DATOS MAESTRA (38 PARTIDAS) ---
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

# --- TRADUCCIONES UI ---
ui = {
    "Español": {"t": "Albarán Digital", "op": "Operario", "ob": "Obra", "btn": "GENERAR DOCUMENTOS", "res_name": "Nombre Responsable", "c1": "CAP 1: REDES", "c2": "CAP 2: HORCAS", "c3": "CAP 3: PERÍMETROS", "c4": "CAP 4: OTROS", "c5": "CAP 5: HORAS"},
    "Marrouqui": {"t": "قائمة العمل", "op": "عامل", "ob": "ورشة", "btn": "إنشاء المستندات", "res_name": "اسم المسؤول", "c1": "1: شبكات", "c2": "2: مشانق", "c3": "3: محيط", "c4": "4: آحرون", "c5": "5: ساعات"},
    "English": {"t": "Digital Report", "op": "Worker", "ob": "Site", "btn": "GENERATE DOCUMENTS", "res_name": "Responsible Name", "c1": "CAP 1: NETS", "c2": "CAP 2: GALLOWS", "c3": "CAP 3: PERIMETERS", "c4": "CAP 4: OTHERS", "c5": "CAP 5: HOURS"}
}

lang = st.sidebar.selectbox("🌐 Idioma / Language", ["Español", "Marrouqui", "English"])
l_idx = {"Español": 1, "Marrouqui": 2, "English": 3}[lang]

# Cabecera con Logo
path_logo = cargar_logo()
col_l, col_t = st.columns([1, 4])
with col_l:
    if path_logo: st.image(path_logo, width=100)
with col_t: st.title(ui[lang]["t"])

# Datos de entrada
c_op, c_ob = st.columns(2)
worker = c_op.text_input(ui[lang]["op"])
site = c_ob.text_input(ui[lang]["ob"])
date = st.date_input("Fecha", datetime.now())

st.divider()
resp = {}

# --- CAPÍTULOS (TODOS CERRADOS POR DEFECTO) ---
def render_cap(titulo, indices):
    with st.expander(titulo, expanded=False):
        for i in indices:
            p = partidas_master[i]
            resp[p[0]] = st.number_input(f"{p[0]}. {p[l_idx]} ({p[4]})", min_value=0, step=1, key=f"p_{p[0]}")

render_cap(ui[lang]["c1"], range(0, 10))
render_cap(ui[lang]["c2"], range(10, 15))
render_cap(ui[lang]["c3"], [15, 16, 18, 25, 26, 27, 28, 29])
render_cap(ui[lang]["c4"], [17, 19, 20, 21, 22, 23, 24, 30, 31, 32])
render_cap(ui[lang]["c5"], range(33, 38))

obs = st.text_area("Observaciones")

# Firma y Aclaración
st.subheader("Firma y Conformidad")
canvas_result = st_canvas(stroke_width=3, stroke_color="#000", background_color="#eee", height=150, width=400, key="canvas")
resp_name = st.text_input(ui[lang]["res_name"])

# --- FUNCIÓN HÍBRIDA COMPARTIR (iPhone) / DESCARGAR (Android) ---
def get_share_js(file_bytes, file_name, label, color):
    b64 = base64.b64encode(file_bytes).decode()
    b_id = "".join(filter(str.isalnum, label))
    return f"""
        <script>
        async function runShare_{b_id}() {{
            const b64Data = "{b64}";
            const fileName = "{file_name}";
            const res = await fetch(`data:application/octet-stream;base64,${{b64Data}}`);
            const blob = await res.blob();
            const file = new File([blob], fileName, {{ type: blob.type }});

            // Si es iPhone o soporta compartir, intenta el menú nativo
            if (navigator.share && navigator.canShare && navigator.canShare({{ files: [file] }})) {{
                try {{
                    await navigator.share({{ files: [file], title: 'Gravity Works', text: 'Adjunto albarán de obra.' }});
                }} catch (e) {{
                    downloadFallback();
                }}
            }} else {{
                downloadFallback();
            }}

            function downloadFallback() {{
                const link = document.createElement('a');
                link.href = URL.createObjectURL(blob);
                link.download = fileName;
                link.click();
            }}
        }}
        </script>
        <button onclick="runShare_{b_id}()" style="width:100%; background-color:{color}; color:white; border:none; padding:15px; border-radius:10px; font-weight:bold; cursor:pointer; font-size:16px; margin-bottom:10px;">
            {label}
        </button>
    """

if st.button(ui[lang]["btn"]):
    if not worker or not site or not resp_name:
        st.error("Rellene Operario, Obra y Nombre del Responsable.")
    elif canvas_result.image_data is None:
        st.warning("Debe firmar el albarán.")
    else:
        # 1. Datos siempre en ESPAÑOL para documentos
        df = pd.DataFrame([{"Cód": p[0], "Descripción": p[1], "Cant": resp[p[0]], "Uni": p[4]} for p in partidas_master if resp[p[0]] > 0])
        
        # 2. Firma
        img_f = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        img_io = io.BytesIO()
        img_f.save(img_io, format="PNG")
        
        # --- EXCEL ---
        xlsx_io = io.BytesIO()
        with pd.ExcelWriter(xlsx_io, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Albaran', startrow=5)
            wb, ws = writer.book, writer.sheets['Albaran']
            bold = wb.add_format({'bold': True})
            if path_logo: ws.insert_image('D1', path_logo, {'x_scale': 0.15, 'y_scale': 0.15})
            ws.write(0, 0, f"OPERARIO: {worker.upper()}", bold)
            ws.write(1, 0, f"OBRA: {site.upper()}", bold)
            ws.write(2, 0, f"FECHA: {date}", bold)
            ws.write(len(df)+8, 0, f"RESPONSABLE: {resp_name.upper()}", bold)
            ws.insert_image(len(df)+9, 0, 'f.png', {'image_data': img_io, 'x_scale': 0.4, 'y_scale': 0.4})
            ws.set_column('B:B', 45)
        
        # --- PDF ---
        pdf = FPDF()
        pdf.add_page()
        if path_logo: pdf.image(path_logo, x=10, y=8, w=30)
        pdf.set_font("Arial", 'B', 14); pdf.set_x(45)
        pdf.cell(0, 10, "GRAVITY WORKS - ALBARAN DE TRABAJO", 0, 1)
        pdf.set_font("Arial", '', 10); pdf.ln(10)
        pdf.cell(0, 7, f"Obra: {site} | Operario: {worker}", 0, 1)
        pdf.ln(5)
        for _, r in df.iterrows():
            pdf.cell(0, 7, f"{r['Cód']} - {r['Descripción']}: {r['Cant']} {r['Uni']}", 0, 1)
        pdf.ln(5); pdf.multi_cell(0, 5, f"Observaciones: {obs}")
        with open("temp_f.png", "wb") as f: f.write(img_io.getvalue())
        pdf.image("temp_f.png", w=45)
        pdf.set_font("Arial", 'B', 10); pdf.cell(0, 10, f"Responsable: {resp_name.upper()}", 0, 1)
        pdf_bytes = pdf.output(dest='S').encode('latin1')

        st.success("✅ Documentos listos. Pulsa para compartir o descargar:")
        f_name = f"{worker.replace(' ','_')}_{site.replace(' ','_')}_{date.strftime('%d-%m')}"
        
        # MOSTRAR BOTONES HÍBRIDOS
        st.components.v1.html(get_share_js(xlsx_io.getvalue(), f"{f_name}.xlsx", "📊 COMPARTIR EXCEL (Administración)", "#003366"), height=75)
        st.components.v1.html(get_share_js(pdf_bytes, f"{f_name}.pdf", "📄 COMPARTIR PDF (Cliente)", "#c0392b"), height=75)
