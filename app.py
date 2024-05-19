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
st.text("Carr. de Madrid a Burgos, Km. 14, 28108 Alcobendas, Madrid, España")

# Función para convertir fecha a string
def fecha_to_string(fecha):
    return fecha.strftime("%Y-%m-%d")

# Establecer la localización en español
locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client.padelclub
reservas_collection = db.reservas

def fecha_para_visualizacion(fecha):
    return fecha.strftime("%A, %B %d")

def get_horarios_disponibles(fecha):
    horarios = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
    fecha_str = fecha_to_string(fecha)
    horarios_disponibles = []
    for horario in horarios:
        canchas_disponibles = get_canchas_disponibles(fecha_str, horario)
        if canchas_disponibles:
            horarios_disponibles.append(horario)
    return horarios_disponibles

# Canchas disponibles basadas en la fecha y el horario seleccionado
def get_canchas_disponibles(fecha_str, horario):
    canchas = ["Cancha 1", "Cancha 2", "Cancha 3"]
    reservas = reservas_collection.find({"fecha": fecha_str, "horario": horario})
    canchas_ocupadas = [reserva["cancha"] for reserva in reservas]
    canchas_disponibles = [cancha for cancha in canchas if cancha not in canchas_ocupadas]
    return canchas_disponibles

canchas_imagenes = {
    "Cancha 1": "assets/img/canchacerrada00.jpg",
    "Cancha 2": "assets/img/canchaabierta01.jpg",
    "Cancha 3": "assets/img/canchaabiertamuro01.jpg"
}

selected = option_menu(
  menu_title=None, 
  options=["Reservar", "Canchas", "Detalles"], 
  icons=["calendar-date", "building", "bi-info-square"], 
  orientation="horizontal")

# ---- MENU ----
if selected == "Detalles":
  google_maps_embed = """
  <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12131.716864602487!2d-3.6724954445800897!3d40.52105560000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd422c722671aed3%3A0x5bba412f7341860b!2sClub%20de%20P%C3%A1del%20Suizo!5e0!3m2!1ses-419!2suy!4v1716094821173!5m2!1ses-419!2suy" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
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

if selected == "Canchas":
  st.subheader("Cancha 1")
  st.image("assets/img/canchacerrada00.jpg")
  st.text("Condiciones: Cerrada, Cristal.")
  st.text("Costo: $1250 (Lunes a Jueves), $1500 (Viernes a Domingo)")
  st.write("##")
  
  st.subheader("Cancha 2")
  st.image("assets/img/canchaabierta01.jpg")
  st.text("Condiciones: Abierta, Cristal.")
  st.text("Costo: $1000 (Lunes a Jueves), $1250 (Viernes a Domingo)")
  st.write("##")
  
  st.subheader("Cancha 3")
  st.image("assets/img/canchaabiertamuro01.jpg")
  st.text("Condiciones: Abierta, Muro.")
  st.text("Costo: $800 (Lunes a Jueves), $1000 (Viernes a Domingo)")
  st.write("##")
  

if selected == "Reservar":
  # Inicializacion variables de estado en st.session_state
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


  st.subheader("Reservar")

  # Paso 1: Formulario para nombre, email y fecha
  if st.session_state.step == 1:
      with st.form(key='form1'):
          st.session_state.nombre = st.text_input("Nombre")
          st.session_state.email = st.text_input("Email")
          st.session_state.fecha = st.date_input("Fecha", min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=9))
          st.text("*Se permiten realizar reservas solamente dentro de un plazo de 10 días.")
          submit_button = st.form_submit_button(label='Siguiente')
      
      if submit_button:
          if st.session_state.nombre == "":
              st.warning("El nombre es obligatorio")
          elif st.session_state.email == "":
              st.warning("El email es obligatorio")
          else:
              st.session_state.step = 2
              st.experimental_rerun()

  # Paso 2: Selección de horario
  if st.session_state.step == 2:
      st.write(f"Nombre: {st.session_state.nombre}")
      st.write(f"Email: {st.session_state.email}")
      st.write(f"Fecha seleccionada: {fecha_para_visualizacion(st.session_state.fecha)}")

      horarios_disponibles = get_horarios_disponibles(st.session_state.fecha)
      if horarios_disponibles:
          st.session_state.horario = st.selectbox("Seleccione un horario disponible", horarios_disponibles, index=horarios_disponibles.index(st.session_state.horario) if st.session_state.horario in horarios_disponibles else 0)
          siguiente_button = st.button("Siguiente")
          volver_button = st.button("Volver")
          if siguiente_button:
              st.session_state.step = 3
              st.experimental_rerun()
          if volver_button:
              st.session_state.step = 1
              st.experimental_rerun()
          
      else:
          st.warning("No hay horarios disponibles para la fecha seleccionada.")
          siguiente_button = st.button("Volver a seleccionar fecha")
          volver_button = st.button("Volver a inicio")
          if siguiente_button:
              st.session_state.step = 1
              st.experimental_rerun()
          if volver_button:
              st.session_state.step = 1
              st.experimental_rerun()

  # Paso 3: Selección de cancha
  if st.session_state.step == 3:
      st.write(f"Nombre: {st.session_state.nombre}")
      st.write(f"Email: {st.session_state.email}")
      st.write(f"Fecha seleccionada: {fecha_para_visualizacion(st.session_state.fecha)}")
      st.write(f"Horario seleccionado: {st.session_state.horario}")

      canchas_disponibles = get_canchas_disponibles(fecha_to_string(st.session_state.fecha), st.session_state.horario)
      if canchas_disponibles:
          st.session_state.cancha = st.selectbox("Seleccione una cancha disponible.", canchas_disponibles, index=canchas_disponibles.index(st.session_state.cancha) if st.session_state.cancha in canchas_disponibles else 0)
          
          # Mostrar la imagen de la cancha seleccionada
          if st.session_state.cancha in canchas_imagenes:
            st.image(canchas_imagenes[st.session_state.cancha])

            # Mostrar información de la cancha
            if st.session_state.cancha == "Cancha 1":
                st.write("Condiciones: Cerrada, Cristal.")
                st.write("Costo: 1250 UYU (Lunes a Jueves), 1500 (Viernes a Domingo)")
            elif st.session_state.cancha == "Cancha 2":
                st.write("Condiciones: Abierta, Cristal.")
                st.write("Costo: 1000 (Lunes a Jueves), 1250 (Viernes a Domingo)")
            elif st.session_state.cancha == "Cancha 3":
                st.write("Condiciones: Abierta, Muro.")
                st.write("Costo: 800 UYU (Lunes a Jueves), 1000 UYU (Viernes a Domingo)")
          
          
          confirmar_button = st.button("Confirmar Reserva")
          volver_button = st.button("Volver")
          if confirmar_button:
              nueva_reserva = {
                  "nombre": st.session_state.nombre,
                  "email": st.session_state.email,
                  "fecha": fecha_to_string(st.session_state.fecha),
                  "horario": st.session_state.horario,
                  "cancha": st.session_state.cancha
              }
              reservas_collection.insert_one(nueva_reserva)
              send(
                   st.session_state.email, 
                  st.session_state.nombre, 
                   fecha_to_string(st.session_state.fecha), 
                   st.session_state.horario, 
                  st.session_state.cancha)
              st.session_state.reserva_confirmada = True
              st.session_state.step = 4  
              st.experimental_rerun()
          if volver_button:
              st.session_state.step = 2
              st.experimental_rerun()
      else:
          st.warning("No hay canchas disponibles para el horario seleccionado.")
          volver_button = st.button("Volver a seleccionar horario")
          if volver_button:
              st.session_state.step = 2
              st.experimental_rerun()

  # Paso 4: Confirmacion de reserva
  if st.session_state.step == 4:
      st.success("Reserva confirmada exitosamente! Revisa tu casilla de mail.")
      st.write(f"Nombre: {st.session_state.nombre}")
      st.write(f"Email: {st.session_state.email}")
      st.write(f"Fecha: {fecha_para_visualizacion(st.session_state.fecha)}")
      st.write(f"Horario: {st.session_state.horario}")
      st.write(f"Cancha: {st.session_state.cancha}")
      
      st.warning("IMPORTANTE: Recuerda que al confirmar la reserva, estás comprometiéndote a asistir. Se aceptaran cancelaciones exclusivamente con un día de anticipación vía comunicación al número +55 97783-6489. En caso de no asistir ni realizar cancelación no se aceptaran nuevas reservas para dichos datos de usuario (email y telefono).")

      nueva_reserva_button = st.button("Hacer otra reserva")
      if nueva_reserva_button:
          st.session_state.step = 1
          st.session_state.nombre = ''
          st.session_state.email = ''
          st.session_state.fecha = None
          st.session_state.horario = ''
          st.session_state.cancha = ''
          st.session_state.reserva_confirmada = False
          st.experimental_rerun()