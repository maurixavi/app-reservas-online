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


# Función para obtener horarios disponibles basados en la fecha seleccionada
def get_horarios_disponibles(fecha):
    horarios = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    fecha_str = fecha_to_string(fecha)
    reservas = reservas_collection.find({"fecha": fecha_str})
    horarios_ocupados = [reserva["horario"] for reserva in reservas]
    horarios_disponibles = [horario for horario in horarios if horario not in horarios_ocupados]
    return horarios_disponibles

def get_canchas_disponibles(fecha, horario):
    canchas = ["Cancha 1", "Cancha 2", "Cancha 3"]
    fecha_str = fecha_to_string(fecha)
    reservas = reservas_collection.find({"fecha": fecha_str, "horario": horario})
    canchas_ocupadas = [reserva["cancha"] for reserva in reservas]
    canchas_disponibles = [cancha for cancha in canchas if cancha not in canchas_ocupadas]
    return canchas_disponibles

# Crear el formulario
st.title("Reserva de Canchas de Padel")

# Formulario para nombre, email y fecha
with st.form(key='form1'):
    nombre = st.text_input("Nombre")
    email = st.text_input("Email")
    fecha = st.date_input("Fecha", min_value=datetime.date.today())
    submit_button = st.form_submit_button(label='Siguiente')

if submit_button:
    # Mostrar campos de horario y cancha solo después de seleccionar la fecha
    st.write(f"Nombre: {nombre}")
    st.write(f"Email: {email}")
    st.write(f"Fecha seleccionada: {fecha}")

    # Obtener horarios disponibles para la fecha seleccionada
    horarios_disponibles = get_horarios_disponibles(fecha)
    if horarios_disponibles:
        horario = st.selectbox("Seleccione un horario disponible", horarios_disponibles)
        # Obtener canchas disponibles para el horario seleccionado
        canchas_disponibles = get_canchas_disponibles(fecha, horario)
        if canchas_disponibles:
            cancha = st.selectbox("Seleccione una cancha disponible", canchas_disponibles)
            # Botón para confirmar la reserva
            if st.button("Confirmar Reserva"):
                # Lógica para guardar la reserva en la base de datos
                nueva_reserva = {
                    "nombre": nombre,
                    "email": email,
                    "fecha": fecha_to_string(fecha),
                    "horario": horario,
                    "cancha": cancha
                }
                reservas_collection.insert_one(nueva_reserva)
                st.success("¡Reserva confirmada!")
        else:
            st.warning("No hay canchas disponibles para el horario seleccionado.")
    else:
        st.warning("No hay horarios disponibles para la fecha seleccionada.")