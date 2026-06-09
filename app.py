%%writefile app.py
import streamlit as st
import pandas as pd

# 1. Configuración de la interfaz
st.set_page_config(page_title="Reporte Clínico Delphi", layout="wide")
st.title("🏥 Centro Clínico Delphi: Reporte Kinesiológico Dinámico")

# 2. Cargar los datos DIRECTAMENTE desde Google Sheets en vivo
# El ttl=30 hace que la app busque nuevos datos cada 30 segundos
@st.cache_data(ttl=30)
def cargar_datos():
    try:
        # Usamos la URL de exportación directa de Google
        url_directa = "https://docs.google.com/spreadsheets/d/1hzSkpdgYFo6RYHDr5Prj47woo5xUT318tS_i_iGWjk8/export?format=csv&gid=1448110922"
        
        data = pd.read_csv(url_directa)
        
        # Limpiamos espacios y datos vacíos
        data.columns = data.columns.str.strip()
        data = data.fillna("No registrado")
        
        return data
    except Exception as e:
        st.error(f"Error al conectar con la base de datos: {e}")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    col_paciente = 'Nombre del paciente:'

    if col_paciente in df.columns:
        # 3. Buscador en la barra lateral
        st.sidebar.header("Control de Pacientes")
        
        # Filtramos para que no aparezca "No registrado" como si fuera un paciente
        lista_pacientes = [p for p in df[col_paciente].unique() if p != "No registrado"]
        paciente_seleccionado = st.sidebar.selectbox("Seleccione un paciente:", lista_pacientes)

        p_data = df[df[col_paciente] == paciente_seleccionado].iloc[-1]

        # 4. Cabecera del Reporte con Datos de Filiación
        st.subheader(f"Ficha Clínica: {paciente_seleccionado}")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.write(f"**RUT:** {p_data.get('RUT', 'No registrado')}")
            st.write(f"**Edad:** {p_data.get('Edad', 'No registrada')} años")
        with col_f2:
            st.write(f"**Médico Tratante:** {p_data.get('Medico tratante', 'No especificado')}")
            st.write(f"**Kinesiólogo:** {p_data.get('Kinesiólogo tratante:', 'No especificado')}")
        with col_f3:
            st.write(f"**Fase de Atención:** {p_data.get('Fase de atención', 'No registrada')}")
            st.write(f"**Fecha Registro:** {p_data.get('Fecha:', p_data.get('Marca temporal', 'N/A'))}")

        st.divider()

        # 5. Panel Métrico de Evolución Clínica (CORRECCIÓN 1: Evitamos st.metric por error de localtunnel)
        st.subheader("📊 Parámetros y Evolución Funcional")
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        # Usamos Markdown para simular el diseño del metric sin usar Javascript dinámico
        col_m1.markdown(f"**Dolor (EVA)**\n### {p_data.get('Dolor EVA', '—')}")
        col_m2.markdown(f"**Rango de Movimiento (ROM)**\n### {p_data.get('Rango de Movimiento (ROM)', '—')}")
        col_m3.markdown(f"**Fuerza CORE**\n### {p_data.get('Fuerza CORE', '—')}")
        
        groc_txt = f"In: {p_data.get('Groc inicial', '—')} | Post: {p_data.get('Groc posterior', '—')}"
        col_m4.markdown(f"**Evolución GROC**\n### {groc_txt}")

        st.divider()

        # 6. Módulo Interactivo: Pestañas de las Directrices de Salud
        st.subheader("🌱 DIRECTRIZ: 6 PILARES DE SALUD")
        
        pilares_activos = str(p_data.get('(Marcar los pilares abordados en la sesión):', 'Ninguno'))
        st.write(f"*Pilares abordados en esta sesión:* **{pilares_activos}**")
        
        recomendacion = str(p_data.get('Recomendación para el hogar (pilar seleccionado)', 'No registrado'))

        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "Sedentarismo", "Sueño", "Estrés", "Alimentación", "Tóxicos", "Relaciones"
        ])

        with tab1:
            if "Sedentarismo" in pilares_activos or (recomendacion != 'No registrado' and "Sedentarismo" in pilares_activos):
                st.info(f"**Plan de Acción Doméstico:**\n\n{recomendacion}")
            else:
                st.write("No se registraron cambios de conducta para este pilar en la sesión seleccionada.")
                
        with tab2:
            if "Sueño" in pilares_activos:
                st.info(f"**Plan de Acción Doméstico:**\n\n{recomendacion}")
            else:
                st.write("No se registraron cambios de conducta para este pilar en la sesión seleccionada.")

        with tab3:
            if "Estrés" in pilares_activos:
                st.info(f"**Plan de Acción Doméstico:**\n\n{recomendacion}")
            else:
                st.write("No se registraron cambios de conducta para este pilar en la sesión seleccionada.")

        with tab4:
            if "Alimentación" in pilares_activos:
                st.info(f"**Plan de Acción Doméstico:**\n\n{recomendacion}")
            else:
                st.write("No se registraron cambios de conducta para este pilar en la sesión seleccionada.")

        with tab5:
            if "Tóxicos" in pilares_activos:
                st.info(f"**Plan de Acción Doméstico:**\n\n{recomendacion}")
            else:
                st.write("No se registraron cambios de conducta para este pilar en la sesión seleccionada.")

        with tab6:
            if "Relaciones" in pilares_activos:
                st.info(f"**Plan de Acción Doméstico:**\n\n{recomendacion}")
            else:
                st.write("No se registraron cambios de conducta para este pilar en la sesión seleccionada.")

        st.divider()

        # 7. Gestión Administrativa y de Interconexión Médica
        st.subheader("📋 Estado de Licencias y Decisiones Clínicas")
        
        col_adm1, col_adm2 = st.columns(2)
        with col_adm1:
            st.write(f"**¿Posee Licencia Médica?:** {p_data.get('¿Existe licencia médica?', 'No registrado')}")
            st.write(f"**Registro Temporal y Días:** {p_data.get('Si existe licencia indicar fecha y N° de días:', 'No registrado')}")
            st.write(f"**Estado de la Licencia:** {p_data.get('Estado de la licencia', 'No registrado')}")
        
        with col_adm2:
            st.write(f"**Decisión Clínica Registrada:** {p_data.get('Decisión Clínica (Hito Intermedio):', 'No especificada')}")
        
        nota_medico = str(p_data.get('Notas para el Médico:', 'No registrado'))
        if nota_medico != "No registrado":
            st.warning(f"⚠️ **NOTAS COMPARTIDAS PARA EL MÉDICO TRATANTE:**\n\n{nota_medico}")

    else:
        st.error(f"Error Crítico: No se encontró la columna '{col_paciente}' en tu archivo.")
else:
    st.warning("La base de datos está vacía o no se cargó correctamente.")
