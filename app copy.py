import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send
from reservas import guardar_reserva
from datetime import datetime, timedelta
import locale
import pymongo

# Conexión a la base de datos
@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client.padelclub
reservas_collection = db.reservas

# Obtener las reservas para una fecha específica
@st.cache_data(ttl=600)
def get_reservas_por_fecha(fecha):
    items = reservas_collection.find({"fechareserva": fecha})
    items = list(items)
    return items

# Filtrar horarios y canchas disponibles
def obtener_disponibilidad(fecha):
    reservas = get_reservas_por_fecha(fecha)
    todos_los_horarios = ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]
    todas_las_canchas = ["Cancha 1 (Techada)", "Cancha 2 (Techada)", "Cancha 3 (Abierta)"]
    horarios_ocupados = [reserva["horario"] for reserva in reservas]
    canchas_ocupadas = [reserva["cancha"] for reserva in reservas]
    horarios_disponibles = [hora for hora in todos_los_horarios if hora not in horarios_ocupados]
    canchas_disponibles = [cancha for cancha in todas_las_canchas if cancha not in canchas_ocupadas]
    return horarios_disponibles, canchas_disponibles

# Establecer la localización en español
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")
fecha_actual = datetime.now()
fechas_disponibles = [(fecha_actual + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(1, 11)]

# Configuración de la página
st.set_page_config(page_title="Padel Club - Reserva tu cancha online", page_icon="🗓️", layout="centered")

st.image("assets/img/PadelCourts0.jpg")
st.title("Padel Club")
st.text("Calle Nombre, 1234")

selected = option_menu(
  menu_title=None, 
  options=["Reservar", "Canchas", "Detalles"], 
  icons=["calendar-date", "building", "bi-info-square"], 
  orientation="horizontal")

if selected == "Detalles":
    google_maps_embed = """
    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3423.7452252388107!2d-55.52924146085205!3d-30.893787466110506!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a9ff3bdacc6fb3%3A0xcdda19f9f9b9e93c!2sOPEN%20PADEL!5e0!3m2!1ses-419!2suy!4v1715816232122!5m2!1ses-419!2suy" width="640" height="350" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
    """
    st.components.v1.html(google_maps_embed, width=640, height=350)
    st.subheader("Horarios")
    dia, hora = st.columns(2)
    dia.text("Lunes a Viernes")
    hora.text("14:00 - 22:00")
    dia.text("Sabado")
    hora.text("08:00 - 23:00")
    dia.text("Domingo")
    hora.text("16:00 - 23:00")
    st.subheader("Contacto")
    st.text("+55 11 97783-6489")
    st.text("canchaspadel@mail.com")

if selected == "Reservar":
    st.subheader("Reservar")
    
    with st.form("form_reserva"):
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre")
        email = col2.text_input("Email")
        fecha = col1.selectbox("Fecha", options=fechas_disponibles)
        
        if fecha:
            horarios_disponibles, canchas_disponibles = obtener_disponibilidad(fecha)
            hora = col2.selectbox("Hora", horarios_disponibles)
            cancha = col1.selectbox("Cancha", canchas_disponibles)
        
        notas = col2.text_area("Notas")
        enviar = st.form_submit_button("Confirmar reserva")
    
    if enviar:
        if nombre == "":
            st.warning("El nombre es obligatorio")
        elif email == "":
            st.warning("El email es obligatorio")
        else:
            guardar_reserva(nombre, email, fecha, hora, cancha)
            send(email, nombre, fecha, hora, cancha)
            st.success("La reserva se ha realizado con éxito. Revise su casilla de correo para ver los detalles.")
