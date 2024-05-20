import streamlit as st
from streamlit_option_menu import option_menu
from send_email import send
from reservas import leer_reservas, guardar_reserva, verificar_disponibilidad, obtener_disponibilidad

#VARIABLES
horas = ["17:00", "18:00", "19:00", "20:00", "21:00", "22:00"]

canchas = ["Cancha 1 (Techada)", "Cancha 2 (Techada)", "Cancha 3 (Abierta)"]


st.set_page_config(
  page_title="Padel Club - Reserva tu cancha online", 
  page_icon="🗓️",
  layout="centered")

st.image("assets/img/PadelCourts0.jpg")
st.title("Padel Club")
st.text("Calle Nombre, 1234")

selected = option_menu(
  menu_title=None, 
  options=["Reservar", "Canchas", "Detalles"], 
  icons=["calendar-date", "building", "bi-info-square"], 
  orientation="horizontal")

if selected == "Detalles":
  # HTML del iframe de Google Maps
	google_maps_embed = """
	<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3423.7452252388107!2d-55.52924146085205!3d-30.893787466110506!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a9ff3bdacc6fb3%3A0xcdda19f9f9b9e93c!2sOPEN%20PADEL!5e0!3m2!1ses-419!2suy!4v1715816232122!5m2!1ses-419!2suy" width="640" height="350" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
	"""

	# Insertar el iframe en la aplicación
	st.components.v1.html(google_maps_embed, width=640, height=350)
	
	#st.markdown("""<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3423.7452252388107!2d-55.52924146085205!3d-30.893787466110506!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x95a9ff3bdacc6fb3%3A0xcdda19f9f9b9e93c!2sOPEN%20PADEL!5e0!3m2!1ses-419!2suy!4v1715816232122!5m2!1ses-419!2suy" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>""", unsafe_allow_html=True)
 
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
	
	col1, col2 = st.columns(2)
 
	nombre = col1.text_input("Nombre")
	email = col2.text_input("Email")
	fecha = col1.date_input("Fecha")
	#hora = col2.selectbox("Hora", horas)
	#cancha = col1.selectbox("Cancha", canchas)
	notas = col2.text_area("Notas")
	
	disponibilidad = obtener_disponibilidad(fecha)
	if disponibilidad:
			horas_disponibles = list(set([hora for hora, _ in disponibilidad]))
			canchas_disponibles = list(set([cancha for _, cancha in disponibilidad]))
			hora = st.selectbox('Hora', horas_disponibles)
			cancha = st.selectbox('Cancha', canchas_disponibles)
	else:
			st.warning("No hay horarios disponibles para la fecha seleccionada.")
			hora = None
			cancha = None

 
	enviar = st.button("Confirmar reserva")
	
	if enviar:
		if nombre == "":
			st.warning("El nombre es obligatorio")
		elif email == "":
			st.warning("El email es obligatorio")
		else:
			if verificar_disponibilidad(fecha, hora, cancha):
				guardar_reserva(nombre, email, fecha, hora, cancha)
				send(email, nombre, fecha, hora, cancha)
				st.success("La reserva se ha realizado con éxito. Revise su casilla de correo para ver los detalles.")
			else:
				st.warning("La cancha no está disponible en el horario seleccionado.")