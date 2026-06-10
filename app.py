import streamlit as st
import pandas as pd

# 1. Configuración Estética Global
st.set_page_config(page_title="Reporte Clínico Delphi", layout="wide")

# CSS personalizado para emular el estilo de la imagen (Colores Delphi)
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .report-header { text-align: center; padding: 10px; background-color: white; border-radius: 10px; margin-bottom: 20px; }
    .info-box { background-color: #ffffff; padding: 15px; border: 1px solid #e0e0e0; border-radius: 8px; height: 100%; }
    .date-box { background-color: #f1f3f4; padding: 10px; border-radius: 5px; text-align: center; border: 1px solid #dcdcdc; }
    .metric-title { font-size: 14px; color: #666; margin-bottom: 2px; text-transform: uppercase; }
    .metric-value { font-size: 22px; font-weight: bold; color: #1a73e8; }
    .pilar-card { background-color: #e6f4ea; padding: 20px; border-radius: 10px; border-left: 5px solid #34a853; }
    </style>
    """, unsafe_allow_html=True)

# 2. Conexión Automatizada (TTL=30 segundos)
@st.cache_data(ttl=30)
def cargar_datos():
    url = "https://docs.google.com/spreadsheets/d/1hzSkpdgYFo6RYHDr5Prj47woo5xUT318tS_i_iGWjk8/export?format=csv&gid=1448110922"
    data = pd.read_csv(url)
    data.columns = data.columns.str.strip()
    return data.fillna("Pendiente")

df = cargar_datos()

# 3. Lógica de Selección de Paciente
st.sidebar.image("https://img.icons8.com/color/96/medical-history.png", width=80)
st.sidebar.title("Gestión Delphi")
lista_p = [p for p in df['Nombre del paciente:'].unique() if p != "Pendiente"]
paciente = st.sidebar.selectbox("Seleccionar Paciente:", lista_p)
p_data = df[df['Nombre del paciente:'] == paciente].iloc[-1]

# --- ESTRUCTURA VISUAL DEL REPORTE ---

# TITULO (Igual a la Web)
st.markdown(f"""
    <div class="report-header">
        <h1 style="color: #202124; margin-bottom: 0;">CENTRO CLÍNICO DELPHI</h1>
        <p style="color: #5f6368; font-size: 1.1em;">Reporte Kinesiológico Estandarizado</p>
        <h3 style="color: #d93025; margin-top: 0;">{p_data.get('Fase de atención', 'FASE ACTUAL')}</h3>
    </div>
    """, unsafe_allow_html=True)

# BLOQUE 1: Información Personal (Grid de 3 columnas)
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown(f"""<div class="info-box">
        <b>Paciente:</b> {paciente}<br>
        <b>RUT:</b> {p_data.get('RUT', '—')}<br>
        <b>Edad:</b> {p_data.get('Edad', '—')} años
    </div>""", unsafe_allow_html=True)
with col_b:
    st.markdown(f"""<div class="info-box">
        <b>Diagnóstico Médico:</b><br>
        {p_data.get('Diagnóstico', 'Lumbago mecánico agudo')}<br>
        <b>Derivado:</b> {p_data.get('Marca temporal', '—')[:10]}
    </div>""", unsafe_allow_html=True)
with col_c:
    st.markdown(f"""<div class="info-box">
        <b>Médico:</b> {p_data.get('Medico tratante', 'Dr. Mario Condal')}<br>
        <b>Kinesiólogo:</b> {p_data.get('Kinesiólogo tratante:', 'Gabriel R.')}<br>
        <b>Contacto:</b> {p_data.get('Kinesiologo tratante:', 'mcondal@delphi.cl')}
    </div>""", unsafe_allow_html=True)

st.write("") # Espaciador

# BLOQUE 2: Recuadros de Fechas (Timeline)
st.write("**CRONOLOGÍA DEL TRATAMIENTO**")
d1, d2, d3, d4, d5, d6 = st.columns(6)
fechas = [
    ("Visita Médico", p_data.get('Fecha:', '—')),
    ("Inicio Licencia", p_data.get('Si existe licencia indicar fecha y N° de días:', '—')),
    ("Eval. Inicial", "12-05-2026"),
    ("1º Sesión Kine", "Pendiente"),
    ("Hito (Sesión 6)", "Pendiente"),
    ("Eval. Final", "Pendiente")
]
for col, (label, date) in zip([d1, d2, d3, d4, d5, d6], fechas):
    col.markdown(f"""<div class="date-box"><small>{label}</small><br><b>{date}</b></div>""", unsafe_allow_html=True)

st.divider()

# BLOQUE 3: Evaluación y Parámetros (Estilo MAR)
col_eval, col_groc = st.columns([2, 1])
with col_eval:
    st.subheader("1. Evaluación Clínica")
    m1, m2, m3 = st.columns(3)
    m1.markdown(f'<p class="metric-title">DOLOR (EVA)</p><p class="metric-value">{p_data.get("Dolor EVA", "—")}</p>', unsafe_allow_html=True)
    m2.markdown(f'<p class="metric-title">RANGO MOV.</p><p class="metric-value">{p_data.get("Rango de Movimiento (ROM)", "—")}</p>', unsafe_allow_html=True)
    m3.markdown(f'<p class="metric-title">FUERZA CORE</p><p class="metric-value">{p_data.get("Fuerza CORE", "—")}</p>', unsafe_allow_html=True)
    
    st.info(f"**Matriz M-A-R (Decisión):** {p_data.get('Decisión Clínica (Hito Intermedio):', 'Mantener plan actual.')}")

with col_groc:
    st.subheader("GROC")
    st.markdown(f"""<div style="text-align: center; padding: 20px; border: 2px solid #1a73e8; border-radius: 10px;">
        <span style="font-size: 40px; font-weight: bold;">{p_data.get('Groc posterior', '0')}</span><br>
        <small>Puntaje de Cambio Percibido</small>
    </div>""", unsafe_allow_html=True)

# BLOQUE 4: Pilares y Recomendaciones
st.write("")
st.subheader("DIRECTRIZ: 6 PILARES DE SALUD")
pilares_session = str(p_data.get('(Marcar los pilares abordados en la sesión):', 'General'))
tabs = st.tabs(["Sedentarismo", "Sueño", "Estrés", "Alimentación", "Tóxicos", "Relaciones"])

recomendacion_hogar = p_data.get('Recomendación para el hogar (pilar seleccionado)', 'Seguir indicaciones generales de higiene postural.')

for i, tab in enumerate(tabs):
    with tab:
        st.markdown(f"""
            <div class="pilar-card">
                <h4>Recomendación Activa</h4>
                <p style="font-size: 1.1em;">{recomendacion_hogar}</p>
            </div>
            """, unsafe_allow_html=True)

# Footer: Notas Médicas
st.warning(f"**NOTAS PARA EL MÉDICO TRATANTE:** {p_data.get('Notas para el Médico:', 'Sin observaciones adicionales.')}")
