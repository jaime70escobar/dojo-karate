import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime, date

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Dojo Karate - Shito-Ryu", page_icon="🥋", layout="wide")

# ==========================================
# 2. DISEÑO PERSONALIZADO (CSS)
# ==========================================
st.markdown("""
<style>
    /* Fondo general con gradiente sutil oscuro */
    .stApp {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d1b1b 100%);
    }
    
    /* Títulos principales en color dorado */
    h1, h2, h3 {
        color: #FFD700 !important;
        font-family: 'Georgia', serif;
    }
    
    /* Texto general en blanco para contraste */
    .stMarkdown, .stTextInput label, .stSelectbox label, .stNumberInput label, .stDateInput label, .stTextArea label {
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    /* Botones principales en rojo karate con borde dorado */
    .stButton > button {
        background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
        color: white !important;
        border: 2px solid #FFD700;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #1a1a1a !important;
        transform: scale(1.02);
    }
    
    /* Pestañas personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #2d1b1b;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #1a1a1a;
        color: #FFD700;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background: #C41E3A !important;
        color: white !important;
    }
    
    /* Formularios con fondo oscuro y borde */
    .stForm {
        background: rgba(45, 27, 27, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #C41E3A;
    }
    
    /* Sidebar con estilo dojo */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #2d1b1b 100%);
    }
    
    /* Métricas destacadas */
    [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 1.8em;
    }
    [data-testid="stMetricLabel"] {
        color: #FFFFFF !important;
    }
    
    /* Mensajes de éxito/error con estilo */
    .stSuccess {
        background: rgba(34, 139, 34, 0.2) !important;
        border-left: 5px solid #228B22;
        color: #90EE90 !important;
    }
    .stError {
        background: rgba(196, 30, 58, 0.2) !important;
        border-left: 5px solid #C41E3A;
        color: #FFB6C1 !important;
    }
    
    /* Inputs y selectores */
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stTextArea > div > div > textarea {
        background-color: #3a2222 !important;
        color: white !important;
        border: 1px solid #C41E3A !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. INICIALIZAR ESTADO DE LA SESIÓN
# ==========================================
if 'alumnos' not in st.session_state:
    st.session_state.alumnos = []
if 'sucursales' not in st.session_state:
    st.session_state.sucursales = []
if 'pagos' not in st.session_state:
    st.session_state.pagos = []
if 'historiales' not in st.session_state:
    st.session_state.historiales = {}

# ==========================================
# 4. FUNCIONES DE UTILIDAD
# ==========================================
def calcular_edad(fecha_nacimiento):
    today = date.today()
    return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

def exportar_a_excel():
    df_alumnos = pd.DataFrame(st.session_state.alumnos)
    df_sucursales = pd.DataFrame(st.session_state.sucursales)
    df_pagos = pd.DataFrame(st.session_state.pagos)
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        if not df_alumnos.empty: df_alumnos.to_excel(writer, sheet_name='Alumnos', index=False)
        if not df_sucursales.empty: df_sucursales.to_excel(writer, sheet_name='Sucursales', index=False)
        if not df_pagos.empty: df_pagos.to_excel(writer, sheet_name='Pagos', index=False)
    return excel_buffer.getvalue()

def exportar_a_json():
    datos = {
        "alumnos": st.session_state.alumnos,
        "sucursales": st.session_state.sucursales,
        "pagos": st.session_state.pagos,
        "historiales": st.session_state.historiales
    }
    return json.dumps(datos, indent=4, default=str).encode('utf-8')

# ==========================================
# 5. ENCABEZADO PRINCIPAL
# ==========================================
st.markdown("""
<div style="text-align: center; padding: 25px; background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%); 
            border-radius: 15px; margin-bottom: 25px; border: 3px solid #FFD700; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
    <h1 style="color: #FFD700; margin: 0; font-size: 2.5em; text-shadow: 3px 3px 6px rgba(0,0,0,0.7);">
        🥋 DOJO KARATE
    </h1>
    <h2 style="color: white; margin: 10px 0; font-size: 1.3em; font-weight: normal;">
        Asociación de Karate SHITO-RYU KENWA MABUNI
    </h2>
    <p style="color: #FFD700; font-style: italic; font-size: 1.1em; margin: 15px 0 0 0; letter-spacing: 2px;">
        ⚔️ Disciplina · Honor · Esfuerzo ⚔️
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. SIDEBAR (MENÚ LATERAL)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: #C41E3A; 
                border-radius: 10px; margin-bottom: 20px; border: 2px solid #FFD700;">
        <h3 style="color: #FFD700; margin: 0;">⚙️ GESTIÓN</h3>
        <p style="color: white; margin: 5px 0; font-size: 0.9em;">Panel Interno del Dojo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Estadísticas Rápidas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🥋 Alumnos", len(st.session_state.alumnos))
        st.metric("🏢 Sucursales", len(st.session_state.sucursales))
    with col2:
        st.metric("💰 Pagos", len(st.session_state.pagos))
    
    st.divider()
    if st.button("🚪 Salir del Sistema", use_container_width=True):
        st.info("Sesión cerrada correctamente. (Recarga la página para volver a entrar)")

# ==========================================
# 7. PESTAÑAS DE NAVEGACIÓN
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🥋 ALUMNOS", "📈 PROGRESO", "🏢 SUCURSALES", "💰 PAGOS", "💾 BACKUP"])

# ==========================================
# PESTAÑA 1: INSCRIPCIÓN DE ALUMNOS
# ==========================================
with tab1:
    st.markdown("### 📝 Inscripción de Alumnos")
    with st.form("form_alumno"):
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            nombre = st.text_input("👤 Nombre Completo *")
            fecha_nac = st.date_input("🎂 Fecha de Nacimiento *", min_value=date(1950, 1, 1))
            representante = st.text_input("👨‍👩‍👧 Nombre del Representante (Si es menor)")
            telefono = st.text_input("📱 Teléfono WhatsApp *", help="⚠️ Solo números, mín. 7 dígitos (ej: 584120000000)")
            observaciones = st.text_area("📌 Observaciones")
            
        with col_right:
            st.markdown("""
            <div style="background: rgba(196, 30, 58, 0.2); padding: 15px; border-radius: 10px; border: 2px solid #C41E3A; margin-bottom: 15px;">
                <h4 style="color: #FFD700; margin-top: 0;">📋 Datos Rápidos</h4>
            </div>
            """, unsafe_allow_html=True)
            
            edad = calcular_edad(fecha_nac)
            st.metric("🎂 Edad Calculada", f"{edad} años")
            
            sucursales_opts = [s['nombre'] for s in st.session_state.sucursales] if st.session_state.sucursales else ["⚠️ Registra una sucursal primero"]
            sucursal = st.selectbox("🏢 Sucursal *", sucursales_opts)
            
            cinturon = st.selectbox("🥋 Cinturón *", ["Blanco", "Amarillo", "Verde", "Azul", "Marrón", "Negro"])
            foto = st.file_uploader("📸 Foto de Perfil", type=['jpg', 'png', 'jpeg'], help="Opcional. Formatos: JPG, PNG")
            
        st.markdown("<br>", unsafe_allow_html=True)
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_alumno = st.form_submit_button("✅ Inscribir Alumno", use_container_width=True)
        with col_btn2:
            st.form_submit_button("❌ Cancelar edición", use_container_width=True)

        if submit_alumno:
            if nombre and telefono and sucursal != "⚠️ Registra una sucursal primero":
                nuevo_alumno = {
                    "id": len(st.session_state.alumnos) + 1,
                    "nombre": nombre,
                    "fecha_nacimiento": str(fecha_nac),
                    "edad": edad,
                    "representante": representante,
                    "sucursal": sucursal,
                    "telefono": telefono,
                    "cinturon": cinturon,
                    "observaciones": observaciones,
                    "foto": foto.name if foto else "Sin foto"
                }
                st.session_state.alumnos.append(nuevo_alumno)
                st.session_state.historiales[nombre] = {"eventos": [], "medallas": [], "kumite": [], "kata": []}
                st.success(f"✅ Alumno **{nombre}** inscrito correctamente.")
                st.rerun()
            else:
                st.error("❌ Por favor completa los campos obligatorios (*).")

# ==========================================
# PESTAÑA 2: DIRECTORIO Y PROGRESO
# ==========================================
with tab2:
    st.markdown("### 📈 Historial y Progreso del Alumno")
    alumnos_opts = [a['nombre'] for a in st.session_state.alumnos] if st.session_state.alumnos else ["⚠️ No hay alumnos registrados"]
    alumno_sel = st.selectbox("🔍 Selecciona un alumno...", alumnos_opts)

    if alumno_sel != "⚠️ No hay alumnos registrados":
        st.info(f"Viendo historial de: **{alumno_sel}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏆 Logros y Eventos")
            evento = st.text_input("Evento / Historial", key="evt")
            if st.button("➕ Agregar evento", key="btn_evt"):
                if evento:
                    st.session_state.historiales[alumno_sel]["eventos"].append(evento)
                    st.success("Evento agregado")
                    st.rerun()

            medalla = st.text_input("Medalla", key="med")
            if st.button("➕ Agregar medalla", key="btn_med"):
                if medalla:
                    st.session_state.historiales[alumno_sel]["medallas"].append(medalla)
                    st.success("Medalla agregada")
                    st.rerun()

        with col2:
            st.markdown("#### 🥋 Progreso Técnico")
            kumite = st.text_input("Kumite", key="kum")
            if st.button("➕ Agregar kumite", key="btn_kum"):
                if kumite:
                    st.session_state.historiales[alumno_sel]["kumite"].append(kumite)
                    st.success("Kumite registrado")
                    st.rerun()

            kata = st.text_input("Avance en Kata", key="kat")
            if st.button("➕ Actualizar kata", key="btn_kat"):
                if kata:
                    st.session_state.historiales[alumno_sel]["kata"].append(kata)
                    st.success("Kata actualizado")
                    st.rerun()
                    
        # Mostrar resumen
        st.markdown("##### 📜 Resumen Actual")
        hist = st.session_state.historiales[alumno_sel]
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Eventos", len(hist["eventos"]))
        c2.metric("Medallas", len(hist["medallas"]))
        c3.metric("Kumite", len(hist["kumite"]))
        c4.metric("Katas", len(hist["kata"]))

# ==========================================
# PESTAÑA 3: REGISTRO DE SUCURSALES
# ==========================================
with tab3:
    st.markdown("### 🏢 Registro de Sucursales")
    with st.form("form_sucursal"):
        col1, col2 = st.columns([2, 1])
        with col1:
            nombre_suc = st.text_input("🏢 Nombre de la Sucursal *")
            direccion = st.text_area("📍 Dirección *")
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            submit_suc = st.form_submit_button("✅ Registrar Sucursal", use_container_width=True)

        if submit_suc:
            if nombre_suc and direccion:
                st.session_state.sucursales.append({"nombre": nombre_suc, "direccion": direccion})
                st.success(f"✅ Sucursal '**{nombre_suc}**' registrada correctamente.")
                st.rerun()
            else:
                st.error("❌ Completa todos los campos obligatorios.")

    st.markdown("### Sucursales Activas")
    if st.session_state.sucursales:
        cols = st.columns(2)
        for i, s in enumerate(st.session_state.sucursales):
            with cols[i % 2]:
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #2d1b1b 0%, #1a1a1a 100%); 
                            padding: 15px; border-radius: 10px; margin: 10px 0; 
                            border-left: 5px solid #C41E3A;">
                    <h4 style="color: #FFD700; margin: 0;">🏢 {s['nombre']}</h4>
                    <p style="color: white; margin: 5px 0;">📍 {s['direccion']}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ No hay sucursales registradas aún.")

# ==========================================
# PESTAÑA 4: REGISTRO DE PAGOS
# ==========================================
with tab4:
    st.markdown("### 💰 Registro de Pagos")
    with st.form("form_pago"):
        col1, col2 = st.columns([2, 1])
        with col1:
            alumnos_pago_opts = [a['nombre'] for a in st.session_state.alumnos] if st.session_state.alumnos else ["⚠️ No hay alumnos"]
            alumno_pago = st.selectbox("👤 Alumno *", alumnos_pago_opts)
            concepto = st.selectbox("📝 Concepto *", ["Mensualidad", "Inscripción", "Examen de Cinta", "Uniforme / Karategi"])
        with col2:
            monto = st.number_input("💵 Monto ($ USD) *", min_value=0.0, step=0.01)
            st.markdown("<br>", unsafe_allow_html=True)
            submit_pago = st.form_submit_button("✅ Registrar Pago", use_container_width=True)
        
        if submit_pago:
            if alumno_pago != "⚠️ No hay alumnos" and monto > 0:
                st.session_state.pagos.append({
                    "alumno": alumno_pago,
                    "monto": monto,
                    "concepto": concepto,
                    "fecha": str(date.today())
                })
                st.success("✅ Pago registrado exitosamente.")
                st.rerun()
            else:
                st.error("❌ Verifica los datos del pago.")

    st.markdown("### 📜 Historial de Pagos")
    if st.session_state.pagos:
        df_pagos_view = pd.DataFrame(st.session_state.pagos)
        st.dataframe(df_pagos_view, use_container_width=True, hide_index=True)
    else:
        st.info("No hay pagos registrados aún.")

# ==========================================
# PESTAÑA 5: BACKUP DE DATOS
# ==========================================
with tab5:
    st.markdown("### 💾 Backup y Restauración de Datos")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div style="background: rgba(45, 27, 27, 0.6); padding: 20px; border-radius: 15px; border: 1px solid #C41E3A;">
            <h4 style="color: #FFD700; margin-top: 0;">📊 Exportar a Excel</h4>
            <p style="color: white; font-size: 0.9em;">Descarga todos tus datos en un archivo Excel con hojas separadas para Alumnos, Sucursales y Pagos.</p>
        </div>
        """, unsafe_allow_html=True)
        excel_data = exportar_a_excel()
        st.download_button(
            label="⬇️ Descargar Excel",
            data=excel_data,
            file_name="dojo_backup.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(45, 27, 27, 0.6); padding: 20px; border-radius: 15px; border: 1px solid #C41E3A;">
            <h4 style="color: #FFD700; margin-top: 0;">🔒 Exportar Backup JSON</h4>
            <p style="color: white; font-size: 0.9em;">Descarga una copia de seguridad completa. Guárdala en un lugar seguro.</p>
        </div>
        """, unsafe_allow_html=True)
        json_data = exportar_a_json()
        st.download_button(
            label="⬇️ Descargar Backup JSON",
            data=json_data,
            file_name="dojo_backup_completo.json",
            mime="application/json",
            use_container_width=True
        )

    with col2:
        st.markdown("""
        <div style="background: rgba(196, 30, 58, 0.2); padding: 20px; border-radius: 15px; border: 2px solid #C41E3A;">
            <h4 style="color: #FFD700; margin-top: 0;">♻️ Restaurar Backup</h4>
            <p style="color: #FFB6C1; font-size: 0.9em;">⚠️ Atención: esto reemplazará todos los datos actuales.</p>
        </div>
        """, unsafe_allow_html=True)
        
        archivo_json = st.file_uploader("Selecciona un archivo JSON de backup", type=['json'])
        
        if archivo_json is not None:
            if st.button("♻️ Restaurar desde JSON", use_container_width=True):
                try:
                    datos = json.load(archivo_json)
                    st.session_state.alumnos = datos.get("alumnos", [])
                    st.session_state.sucursales = datos.get("sucursales", [])
                    st.session_state.pagos = datos.get("pagos", [])
                    st.session_state.historiales = datos.get("historiales", {})
                    st.success("✅ ¡Datos restaurados correctamente!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error al restaurar: {e}")