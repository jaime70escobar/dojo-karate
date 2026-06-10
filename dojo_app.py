import streamlit as st
import pandas as pd
import json
import io
from datetime import datetime, date

# Configuración de la página
st.set_page_config(page_title="Dojo Karate - Shito-Ryu Kenwa Mabuni", page_icon="🥋", layout="wide")

# Inicializar estado de la sesión (simula una base de datos en memoria)
if 'alumnos' not in st.session_state:
    st.session_state.alumnos = []
if 'sucursales' not in st.session_state:
    st.session_state.sucursales = []
if 'pagos' not in st.session_state:
    st.session_state.pagos = []
if 'historiales' not in st.session_state:
    st.session_state.historiales = {}

# --- Funciones de utilidad ---
def calcular_edad(fecha_nacimiento):
    today = date.today()
    return today.year - fecha_nacimiento.year - ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

def exportar_a_excel():
    df_alumnos = pd.DataFrame(st.session_state.alumnos)
    df_sucursales = pd.DataFrame(st.session_state.sucursales)
    df_pagos = pd.DataFrame(st.session_state.pagos)
    
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        df_alumnos.to_excel(writer, sheet_name='Alumnos', index=False)
        df_sucursales.to_excel(writer, sheet_name='Sucursales', index=False)
        df_pagos.to_excel(writer, sheet_name='Pagos', index=False)
    return excel_buffer.getvalue()

def exportar_a_json():
    datos = {
        "alumnos": st.session_state.alumnos,
        "sucursales": st.session_state.sucursales,
        "pagos": st.session_state.pagos,
        "historiales": st.session_state.historiales
    }
    return json.dumps(datos, indent=4, default=str).encode('utf-8')

# --- Interfaz Principal ---
st.title("🥋 Dojo Karate")
st.subheader("Asociación de Karate SHITO-RYU KENWA MABUNI")
st.caption("Disciplina · Honor · Esfuerzo")

st.sidebar.title("Gestión interna del dojo")
if st.sidebar.button("Salir del Sistema"):
    st.info("Sesión cerrada correctamente.")

# Pestañas de navegación
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🥋 Alumnos", "📈 Progreso", "🏢 Sucursales", "💰 Pagos", "💾 Backup"])

# ==========================================
# PESTAÑA 1: INSCRIPCIÓN DE ALUMNOS
# ==========================================
with tab1:
    st.header("📝 Inscripción de Alumnos")
    with st.form("form_alumno"):
        col1, col2 = st.columns(2)
        with col1:
            nombre = st.text_input("Nombre Completo *")
            fecha_nac = st.date_input("Fecha de Nacimiento *", min_value=date(1950, 1, 1))
            representante = st.text_input("Nombre del Representante (Si es menor)")
            telefono = st.text_input("Teléfono (WhatsApp ej: 584120000000) *", help="⚠️ Solo números, mín. 7 dígitos")
        with col2:
            edad = calcular_edad(fecha_nac)
            st.metric("Edad", f"{edad} años")
            
            sucursales_opts = [s['nombre'] for s in st.session_state.sucursales] if st.session_state.sucursales else ["Sin sucursales registradas"]
            sucursal = st.selectbox("Sucursal *", sucursales_opts)
            
            cinturon = st.selectbox("Cinturón *", ["Blanco", "Amarillo", "Verde", "Azul", "Marrón", "Negro"])
            foto = st.file_uploader("Foto de Perfil (Opcional: JPG, PNG)", type=['jpg', 'png', 'jpeg'])
            
        observaciones = st.text_area("Observaciones")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_alumno = st.form_submit_button("✅ Inscribir Alumno", type="primary")
        with col_btn2:
            st.form_submit_button("❌ Cancelar edición")

        if submit_alumno:
            if nombre and telefono and sucursal != "Sin sucursales registradas":
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
                st.success(f"Alumno {nombre} inscrito correctamente.")
            else:
                st.error("Por favor completa los campos obligatorios (*).")

# ==========================================
# PESTAÑA 2: DIRECTORIO Y PROGRESO
# ==========================================
with tab2:
    st.header("📈 Historial y Progreso del Alumno")
    alumnos_opts = [a['nombre'] for a in st.session_state.alumnos] if st.session_state.alumnos else ["No hay alumnos registrados"]
    alumno_sel = st.selectbox("Selecciona un alumno...", alumnos_opts)

    if alumno_sel != "No hay alumnos registrados":
        st.info(f"Viendo historial, medallas, kumite y avances en kata de: **{alumno_sel}**")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Actualizar historial")
            evento = st.text_input("Evento / Historial")
            if st.button("Agregar evento"):
                if evento:
                    st.session_state.historiales[alumno_sel]["eventos"].append(evento)
                    st.success("Evento agregado")

            medalla = st.text_input("Medalla")
            if st.button("Agregar medalla"):
                if medalla:
                    st.session_state.historiales[alumno_sel]["medallas"].append(medalla)
                    st.success("Medalla agregada")

        with col2:
            st.subheader("Progreso Técnico")
            kumite = st.text_input("Kumite")
            if st.button("Agregar kumite"):
                if kumite:
                    st.session_state.historiales[alumno_sel]["kumite"].append(kumite)
                    st.success("Kumite registrado")

            kata = st.text_input("Avance en Kata")
            if st.button("Actualizar kata"):
                if kata:
                    st.session_state.historiales[alumno_sel]["kata"].append(kata)
                    st.success("Kata actualizado")

# ==========================================
# PESTAÑA 3: REGISTRO DE SUCURSALES
# ==========================================
with tab3:
    st.header("🏢 Registro de Sucursales")
    with st.form("form_sucursal"):
        nombre_suc = st.text_input("Nombre de la Sucursal *")
        direccion = st.text_area("Dirección *")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            submit_suc = st.form_submit_button("✅ Registrar Sucursal", type="primary")
        with col_btn2:
            st.form_submit_button("❌ Cancelar edición")

        if submit_suc:
            if nombre_suc and direccion:
                st.session_state.sucursales.append({"nombre": nombre_suc, "direccion": direccion})
                st.success(f"Sucursal '{nombre_suc}' registrada correctamente.")
            else:
                st.error("Completa todos los campos obligatorios.")

    st.subheader("Sucursales Activas")
    if st.session_state.sucursales:
        for s in st.session_state.sucursales:
            st.markdown(f"- **{s['nombre']}**: {s['direccion']}")
    else:
        st.warning("No hay sucursales registradas aún.")

# ==========================================
# PESTAÑA 4: REGISTRO DE PAGOS
# ==========================================
with tab4:
    st.header("💰 Registro de Pagos")
    with st.form("form_pago"):
        alumnos_pago_opts = [a['nombre'] for a in st.session_state.alumnos] if st.session_state.alumnos else ["No hay alumnos"]
        alumno_pago = st.selectbox("Alumno *", alumnos_pago_opts)
        monto = st.number_input("Monto ($ USD) *", min_value=0.0, step=0.01)
        concepto = st.selectbox("Concepto *", ["Mensualidad", "Inscripción", "Examen de Cinta", "Uniforme / Karategi"])
        
        submit_pago = st.form_submit_button("✅ Registrar Pago", type="primary")
        
        if submit_pago:
            if alumno_pago != "No hay alumnos" and monto > 0:
                st.session_state.pagos.append({
                    "alumno": alumno_pago,
                    "monto": monto,
                    "concepto": concepto,
                    "fecha": str(date.today())
                })
                st.success("Pago registrado exitosamente.")
            else:
                st.error("Verifica los datos del pago.")

    st.subheader("Historial de Pagos")
    if st.session_state.pagos:
        st.dataframe(pd.DataFrame(st.session_state.pagos), use_container_width=True)

# ==========================================
# PESTAÑA 5: BACKUP DE DATOS
# ==========================================
with tab5:
    st.header("💾 Backup de Datos")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Exportar a Excel")
        st.write("Descarga todos tus datos en un archivo Excel con hojas separadas para Alumnos, Sucursales y Pagos.")
        excel_data = exportar_a_excel()
        st.download_button(
            label="⬇️ Descargar Excel",
            data=excel_data,
            file_name="dojo_backup.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.subheader("🔒 Exportar Backup JSON")
        st.write("Descarga una copia de seguridad completa. Guárdala en un lugar seguro.")
        json_data = exportar_a_json()
        st.download_button(
            label="⬇️ Descargar Backup JSON",
            data=json_data,
            file_name="dojo_backup_completo.json",
            mime="application/json"
        )

    with col2:
        st.subheader("♻️ Restaurar Backup")
        st.warning("Atención: esto reemplazará todos los datos actuales.")
        archivo_json = st.file_uploader("Selecciona un archivo JSON de backup", type=['json'])
        
        if archivo_json is not None:
            if st.button("♻️ Restaurar desde JSON", type="primary"):
                try:
                    datos = json.load(archivo_json)
                    st.session_state.alumnos = datos.get("alumnos", [])
                    st.session_state.sucursales = datos.get("sucursales", [])
                    st.session_state.pagos = datos.get("pagos", [])
                    st.session_state.historiales = datos.get("historiales", {})
                    st.success("¡Datos restaurados correctamente!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al restaurar: {e}")