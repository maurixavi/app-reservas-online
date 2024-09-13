import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send
import datetime
import locale
import pymongo
import re
import random

st.set_page_config(
  page_title="Padel Club - Reserva tu cancha online", 
  page_icon="🗓️",
  layout="centered")

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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

def generate_unique_reservation_code():
    while True:
        code = '{:08d}'.format(random.randint(0, 99999999))
        if not reservas_collection.find_one({"codigo_reserva": code}):
            return code


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_telefono(telefono):
    return telefono.isdigit() and len(telefono) in range(7, 13)

def fecha_para_visualizacion(fecha):
    return fecha.strftime("%A, %B %d").title()

def get_horarios_disponibles(fecha):
    horarios = [
        "08:30", "10:00", "11:30", "13:00",
        "14:30", "16:00", "17:30", "19:00",
        "20:30", "22:00"
    ]
    horarios_sabado = [
        "08:30", "10:00", "11:30", "13:00",
        "14:30", "16:00", "17:30", "19:00",
        "20:30", "22:00"
    ]
    horarios_domingo = [
        "14:30", "16:00", "17:30", "19:00",
        "20:30", "22:00"
    ]
    
    dia_semana = fecha.strftime("%A")
    fecha_str = fecha_to_string(fecha)
    horarios_disponibles = []
    if dia_semana == "sábado":
        for horario in horarios_sabado:
            canchas_disponibles = get_canchas_disponibles(fecha_str, horario)
            if canchas_disponibles:
                horarios_disponibles.append(horario)
    elif dia_semana == "domingo":
        for horario in horarios_domingo:
            canchas_disponibles = get_canchas_disponibles(fecha_str, horario)
            if canchas_disponibles:
                horarios_disponibles.append(horario)
    else:
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

def obtener_condiciones_y_costo(cancha, fecha):
    condiciones = ""
    costo = ""
    dia_semana = fecha.strftime("%A").title()
    dias_semana = ["Lunes", "Martes", "Miercoles", "Jueves"]
    
    if cancha == "Cancha 1":
        condiciones = "Cerrada, Cristal"
        if dia_semana in dias_semana:
            costo = "€12.50"
        else:
            costo = "€15.00"
    elif cancha == "Cancha 2":
        condiciones = "Abierta, Cristal"
        if dia_semana in dias_semana:
            costo = "€10.00"
        else:
            costo = "€12.50"
    elif cancha == "Cancha 3":
        condiciones = "Abierta, Muro"
        if dia_semana in dias_semana:
            costo = "€8.00"
        else:
            costo = "€10.00"
    
    return condiciones, costo

canchas_imagenes = {
    "Cancha 1": "assets/img/canchacerrada00.jpg",
    "Cancha 2": "assets/img/canchaabierta01.jpg",
    "Cancha 3": "assets/img/canchaabiertamuro01.jpg"
}

selected = option_menu(
  menu_title=None, 
  options=["Reservar", "Cancelar", "Canchas", "Detalles"], 
  icons=["calendar-date", "calendar-x", "building", "bi-info-square"], 
  orientation="horizontal")

# ---- MENU ----
if selected == "Detalles":
  google_maps_embed = """
  <div style="display: flex; justify-content: center;">
    <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d12131.716864602487!2d-3.6724954445800897!3d40.52105560000001!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0xd422c722671aed3%3A0x5bba412f7341860b!2sClub%20de%20P%C3%A1del%20Suizo!5e0!3m2!1ses-419!2suy!4v1716094821173!5m2!1ses-419!2suy" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
  </div>
  """
  st.components.v1.html(google_maps_embed, width=640, height=350)

  col_horarios, col_contacto = st.columns(2)

  with col_horarios:
    st.subheader("Horarios")
    sub_col1, sub_col2 = st.columns(2)
    with sub_col1:
        st.text("Lunes a Viernes:")
        st.text("Sábado:")
        st.text("Domingo:")
    with sub_col2:
        st.text("14:00 - 22:00")
        st.text("08:00 - 23:00")
        st.text("16:00 - 23:00")

  with col_contacto:
    st.subheader("Contacto")
    st.text("📞 +55 11 97783-6489")
    st.text("📧 canchaspadel@mail.com")

if selected == "Canchas":
  st.subheader("Canchas")
  
  st.write("##### Cancha 1")
  st.image("assets/img/canchacerrada00.jpg")
  st.text("Condiciones: Cerrada, Cristal.")
  st.text("Costo: €12.50 (Lunes a Jueves), €15.00 (Viernes a Domingo)")
  st.write("---")
  
  st.write("##### Cancha 2")
  st.image("assets/img/canchaabierta01.jpg")
  st.text("Condiciones: Abierta, Cristal.")
  st.text("Costo: €10.00 (Lunes a Jueves), €12.50 (Viernes a Domingo)")
  st.write("---")
  
  st.write("##### Cancha 3")
  st.image("assets/img/canchaabiertamuro01.jpg")
  st.text("Condiciones: Abierta, Muro.")
  st.text("Costo: €8.00 (Lunes a Jueves), €10.00 (Viernes a Domingo)")
  
if selected == "Cancelar":
    st.subheader("Cancelar reserva")
    
    with st.form(key='form_cancelar_reserva'):
        codigo_reserva = st.text_input("Codigo de Reserva")
        cancelar_button = st.form_submit_button(label='Cancelar Reserva')

    if cancelar_button:
        reserva = reservas_collection.find_one({"codigo": codigo_reserva})
        reservas_collection.delete_one({"codigo": codigo_reserva})
        
        if reserva:
            send(
                  "Cancelacion de reserva",
                   reserva['codigo'],
                   reserva['email'],
                   reserva['nombre'],
                   reserva['apellido'],
                   reserva['fecha'],
                   reserva['horario'],
                   reserva['cancha'],
                   "",
                   reserva['costo'])
            st.success("Su reserva ha sido correctamente cancelada.")
            st.write("##### Detalles de la reserva")
            st.write(f"Nombre: {reserva['nombre']} {reserva['apellido']}")
            st.write(f"Email: {reserva['email']}")
            st.write(f"Fecha: {reserva['fecha']}")
            st.write(f"Hora: {reserva['horario']}")
            st.write(f"Cancha: {reserva['cancha']}")
            st.write(f"Costo: {reserva['costo']}")
            st.write(f"Realizada: {reserva['timestamp']}")    
        else:
            st.error("Código de reserva no encontrado.")
                    
                    
if selected == "Reservar":
  # Inicializacion variables de estado en st.session_state
  if 'step' not in st.session_state:
      st.session_state.step = 1
  if 'nombre' not in st.session_state:
      st.session_state.nombre = ''
  if 'apellido' not in st.session_state:
      st.session_state.apellido = ''
  if 'telefono' not in st.session_state:
      st.session_state.telefono = ''
  if 'email' not in st.session_state:
      st.session_state.email = ''
  if 'fecha' not in st.session_state:
      st.session_state.fecha = None
  if 'horario' not in st.session_state:
      st.session_state.horario = ''
  if 'cancha' not in st.session_state:
      st.session_state.cancha = ''
  if 'codigo_reserva' not in st.session_state:
      st.session_state.codigo_reserva = ''
  if 'reserva_confirmada' not in st.session_state:
      st.session_state.reserva_confirmada = False

  st.subheader("Reservar")

  # Paso 1: Formulario para nombre, email y fecha
  if st.session_state.step == 1:
      with st.form(key='form1'):
          col1, col2 = st.columns(2)
          with col1:
              st.session_state.nombre = st.text_input("Nombre", value=st.session_state.nombre)
          with col2:
              st.session_state.apellido = st.text_input("Apellido",value=st.session_state.apellido)
          st.session_state.email = st.text_input("Email", value=st.session_state.email)
          st.session_state.telefono = st.text_input("Telefono", value=st.session_state.telefono)
          st.session_state.fecha = st.date_input("Fecha", min_value=datetime.date.today(), max_value=datetime.date.today() + datetime.timedelta(days=9), value=st.session_state.fecha)
          st.text("*Se permiten reservas solamente dentro de un plazo de 10 días.")
          submit_button = st.form_submit_button(label='Siguiente')
      
      if submit_button:
          if st.session_state.nombre == "":
              st.warning("El nombre es un campo obligatorio. Por favor, ingrese su nombre.")
          elif st.session_state.email == "":
              st.warning("El email es un campo obligatorio. Por favor, ingrese su email.")
          elif not is_valid_email(st.session_state.email):
              st.warning("El email ingresado no es válido. Por favor, ingrese un email válido.")
          elif st.session_state.telefono == "":
              st.warning("El telefono es un campo obligatorio. Por favor, ingrese su telefono.")
          elif not is_valid_telefono(st.session_state.telefono):
              st.warning("El telefono ingresado contiene caracteres no válidos o largo no aceptado. Por favor, ingrese un telefono válido.")
          else:
              st.session_state.step = 2
              st.rerun()

  # Paso 2: Selección de horario
  if st.session_state.step == 2:
      st.write(f"Nombre: {st.session_state.nombre} {st.session_state.apellido}")
      st.write(f"Email: {st.session_state.email}")
      st.write(f"Telefono: {st.session_state.telefono}")
      st.write(f"Fecha seleccionada: {fecha_para_visualizacion(st.session_state.fecha)}")
      # current_time = datetime.datetime.now().strftime("%H:%M:%S")
      # st.text(f"Tiempo actual: {current_time}")

      horarios_disponibles = get_horarios_disponibles(st.session_state.fecha)
      if horarios_disponibles:
          st.session_state.horario = st.selectbox("Seleccione un horario disponible", horarios_disponibles, index=horarios_disponibles.index(st.session_state.horario) if st.session_state.horario in horarios_disponibles else 0)
          siguiente_button = st.button("Siguiente")
          volver_button = st.button("Volver")
          if siguiente_button:
              st.session_state.step = 3
              st.rerun()
          if volver_button:
              st.session_state.step = 1
              st.rerun()
          
      else:
          st.warning("No hay horarios disponibles para la fecha seleccionada.")
          siguiente_button = st.button("Volver a seleccionar fecha")
          volver_button = st.button("Volver a inicio")
          if siguiente_button:
              st.session_state.step = 1
              st.rerun()
          if volver_button:
              st.session_state.step = 1
              st.rerun()

  # Paso 3: Selección de cancha
  if st.session_state.step == 3:
      st.write(f"Nombre: {st.session_state.nombre} {st.session_state.apellido}")
      st.write(f"Email: {st.session_state.email}")
      st.write(f"Telefono: {st.session_state.telefono}")
      st.write(f"Fecha seleccionada: {fecha_para_visualizacion(st.session_state.fecha)}")
      st.write(f"Horario seleccionado: {st.session_state.horario}")

      canchas_disponibles = get_canchas_disponibles(fecha_to_string(st.session_state.fecha), st.session_state.horario)
      if canchas_disponibles:
          st.session_state.cancha = st.selectbox("Seleccione una cancha disponible.", canchas_disponibles, index=canchas_disponibles.index(st.session_state.cancha) if st.session_state.cancha in canchas_disponibles else 0)
          
          if st.session_state.cancha in canchas_imagenes:
            st.image(canchas_imagenes[st.session_state.cancha])

            condiciones, costo = obtener_condiciones_y_costo(st.session_state.cancha, st.session_state.fecha)
            st.write(f"Condiciones: {condiciones}")
            st.write(f"Costo: {costo}")
                    
          confirmar_button = st.button("Confirmar Reserva")
          volver_button = st.button("Volver")
          if confirmar_button:
              codigo_reserva = generate_unique_reservation_code()
              st.session_state.codigo_reserva = codigo_reserva   
              nueva_reserva = {
                  "codigo": codigo_reserva,
                  "nombre": st.session_state.nombre,
                  "apellido": st.session_state.apellido,
                  "email": st.session_state.email,
                  "telefono": st.session_state.telefono,
                  "fecha": fecha_to_string(st.session_state.fecha),
                  "horario": st.session_state.horario,
                  "cancha": st.session_state.cancha,
                  "costo": costo,
                  "timestamp": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
              }
              reservas_collection.insert_one(nueva_reserva)
              condiciones, costo = obtener_condiciones_y_costo(st.session_state.cancha, st.session_state.fecha)
              send(
                  "Reserva de cancha",
                   st.session_state.codigo_reserva,
                   st.session_state.email, 
                   st.session_state.nombre, 
                   st.session_state.apellido, 
                   fecha_to_string(st.session_state.fecha), 
                   st.session_state.horario, 
                   st.session_state.cancha, condiciones, costo)
              st.session_state.reserva_confirmada = True
              st.session_state.step = 4  
              st.rerun()
          if volver_button:
              st.session_state.step = 2
              st.rerun()
      else:
          st.warning("No hay canchas disponibles para el horario seleccionado.")
          volver_button = st.button("Volver a seleccionar horario")
          if volver_button:
              st.session_state.step = 2
              st.rerun()

  # Paso 4: Confirmacion de reserva
  if st.session_state.step == 4:
      st.success("Reserva confirmada exitosamente! Revisa tu casilla de mail.")
      
      st.write("##### Detalles de la reserva")

      
      col_attr, col_data = st.columns(2)
    
      with col_attr:
        st.write("**Codigo de Reserva**")
        st.write("**Nombre**")
        st.write("**Email**")
        st.write("**Telefono**")
        st.write("**Inicio**") 
        st.write("**Duración**")
        st.write("**Cancha**")
        st.write("**Costo**")
      with col_data:
        codigo_reserva = st.session_state.codigo_reserva
        st.write(codigo_reserva)
        st.write(f"{st.session_state.nombre} {st.session_state.apellido}")
        st.write(st.session_state.email)
        st.write(st.session_state.telefono)
        st.write(fecha_para_visualizacion(st.session_state.fecha) + f". Hora: {st.session_state.horario}")
        cancha_seleccionada = st.session_state.cancha
        condiciones, costo = obtener_condiciones_y_costo(cancha_seleccionada, st.session_state.fecha)
        st.write("90 minutos")
        st.write(f"{cancha_seleccionada} ({condiciones})")
        st.write(costo)
        
      st.write("---")
      
      st.warning("Politica de cancelación: Recuerda que al confirmar la reserva, estás comprometiéndote a asistir. Se permite la realización de cancelaciones exclusivamente con 24 horas de anticipación.")

      nueva_reserva_button = st.button("Hacer otra reserva")
      if nueva_reserva_button:
          st.session_state.step = 1
          st.session_state.nombre = ''
          st.session_state.email = ''
          st.session_state.fecha = None
          st.session_state.horario = ''
          st.session_state.cancha = ''
          st.session_state.reserva_confirmada = False
          st.rerun()