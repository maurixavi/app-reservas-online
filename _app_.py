import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send
from reservas import guardar_reserva
import datetime
import locale
import pymongo

st.set_page_config(
  page_title="Padel Club - Reserva tu cancha online", 
  page_icon="🗓️",
  layout="centered")

st.image("assets/img/PadelCourts0.jpg")
st.title("Padel Club")
st.text("Calle Nombre, 1234")

# Función para convertir fecha a string
def fecha_to_string(fecha):
    return fecha.strftime("%Y-%m-%d")

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client.padelclub
reservas_collection = db.reservas

def get_horarios_disponibles(fecha):
    horarios = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    fecha_str = fecha_to_string(fecha)
    horarios_disponibles = []
    for horario in horarios:
        canchas_disponibles = get_canchas_disponibles(fecha_str, horario)
        if canchas_disponibles:
            horarios_disponibles.append(horario)
    return horarios_disponibles

# Función para obtener canchas disponibles basadas en la fecha y el horario seleccionado
def get_canchas_disponibles(fecha_str, horario):
    canchas = ["Cancha 1", "Cancha 2", "Cancha 3"]
    reservas = reservas_collection.find({"fecha": fecha_str, "horario": horario})
    canchas_ocupadas = [reserva["cancha"] for reserva in reservas]
    canchas_disponibles = [cancha for cancha in canchas if cancha not in canchas_ocupadas]
    return canchas_disponibles

# Inicializar variables de estado en st.session_state
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'nombre' not in st.session_state:
    st.session_state.nombre = ''
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'fecha' not in st.session_state:
    st.session_state.fecha = None
if 'horario' not in st.session_state:
    st.session_state.horario = ''
if 'cancha' not in st.session_state:
    st.session_state.cancha = ''

# Paso 1: Formulario para nombre, email y fecha
if st.session_state.step == 1:
    st.title("Reserva de Canchas de Padel")
    with st.form(key='form1'):
        st.session_state.nombre = st.text_input("Nombre")
        st.session_state.email = st.text_input("Email")
        st.session_state.fecha = st.date_input("Fecha", min_value=datetime.date.today())
        submit_button = st.form_submit_button(label='Siguiente')
    
    if submit_button:
        st.session_state.step = 2
        st.experimental_rerun()

# Paso 2: Selección de horario
if st.session_state.step == 2:
    st.write(f"Nombre: {st.session_state.nombre}")
    st.write(f"Email: {st.session_state.email}")
    st.write(f"Fecha seleccionada: {st.session_state.fecha}")

    horarios_disponibles = get_horarios_disponibles(st.session_state.fecha)
    if horarios_disponibles:
        st.session_state.horario = st.selectbox("Seleccione un horario disponible", horarios_disponibles)
        siguiente_button = st.button("Siguiente")
        if siguiente_button:
            st.session_state.step = 3
            st.experimental_rerun()
    else:
        st.warning("No hay horarios disponibles para la fecha seleccionada.")
        st.button("Volver", on_click=lambda: st.session_state.update(step=1))

# Paso 3: Selección de cancha
if st.session_state.step == 3:
    st.write(f"Nombre: {st.session_state.nombre}")
    st.write(f"Email: {st.session_state.email}")
    st.write(f"Fecha seleccionada: {st.session_state.fecha}")
    st.write(f"Horario seleccionado: {st.session_state.horario}")

    canchas_disponibles = get_canchas_disponibles(fecha_to_string(st.session_state.fecha), st.session_state.horario)
    if canchas_disponibles:
        st.session_state.cancha = st.selectbox("Seleccione una cancha disponible", canchas_disponibles)
        confirmar_button = st.button("Confirmar Reserva")
        if confirmar_button:
            nueva_reserva = {
                "nombre": st.session_state.nombre,
                "email": st.session_state.email,
                "fecha": fecha_to_string(st.session_state.fecha),
                "horario": st.session_state.horario,
                "cancha": st.session_state.cancha
            }
            reservas_collection.insert_one(nueva_reserva)
            st.success("¡Reserva confirmada!")
            st.session_state.step = 1  # Reiniciar formulario
            st.experimental_rerun()
    else:
        st.warning("No hay canchas disponibles para el horario seleccionado.")
        st.button("Volver", on_click=lambda: st.session_state.update(step=2))