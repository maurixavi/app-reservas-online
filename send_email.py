from email import message
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def fecha_para_visualizacion(fecha):
    return fecha.strftime("%A, %B %d").title()
  
def send(tipo, codigo, email, nombre, apellido, fecha, hora, cancha, condiciones, costo):
	user = st.secrets["smtp_user"]
	password = st.secrets["smtp_password"]
 
	sender_email = "Padel Club"
 
	msg = MIMEMultipart()
 
	smtp_server = "smtp.gmail.com"
	smtp_port = 587
 
	msg['From'] = sender_email
	msg['To'] = email
	msg['Subject'] = tipo
	
	with open('assets/img/PadelClubBanner.jpg', 'rb') as f:
		image = MIMEImage(f.read())
		image.add_header('Content-ID', '<logo>')
		msg.attach(image)

	message = ""
	if tipo == "Reserva de cancha":
		message = f"""
		<html>
		<body>
			<p>Hola {nombre} {apellido},</p>
			<p>Su reserva ha sido realizada con éxito.</p>
   		<p>Detalles de la reserva:</p>
			<p>Codigo de Reserva: {codigo}</p>
			<p>Fecha: {fecha}</p>
			<p>Hora: {hora}</p>
			<p>Duracion: 90 minutos</p>
			<p>Cancha: {cancha} ({condiciones})</p>
			<p>Costo: {costo}</p>
			<p>Gracias por elegirnos.</p>
			<p>Padel Club.</p>
			<img src="cid:logo" style="display: block; margin: 0 auto;">
			<p>Politica de cancelación: Recuerda que al confirmar la reserva, estás comprometiéndote a asistir. Se permite la realización de cancelaciones exclusivamente con 24 horas de anticipación.</p>
		</body>
		</html>
		"""
	if tipo == "Cancelacion de reserva":
		message = f"""
		<html>
		<body>
			<p>Hola {nombre} {apellido},</p>
			<p>Su reserva con el codigo {codigo} ha sido cancelada con éxito.</p>
			<p>Detalles de la reserva cancelada:</p>
			<p>Codigo de Reserva: {codigo}</p>
			<p>Fecha: {fecha}</p>
			<p>Hora: {hora}</p>
			<p>Duracion: 90 minutos</p>
			<p>Cancha: {cancha}</p>
			<p>Costo: {costo}</p>
			<p>Gracias por elegirnos.</p>
			<p>Padel Club.</p>
			<img src="cid:logo" style="display: block; margin: 0 auto;">
			<p>Politica de cancelación: Recuerda que al confirmar la reserva, estás comprometiéndote a asistir. Se permite la realización de cancelaciones exclusivamente con 24 horas de anticipación.</p>
		</body>
		</html>
		"""

	msg.attach(MIMEText(message, 'html'))
	#msg.attach(MIMEText(message, 'plain'))
 
	#Conexion al servidor
	try:
		server = smtplib.SMTP(smtp_server, smtp_port)
		server.starttls()
		server.login(user, password)
		server.sendmail(sender_email, email, msg.as_string())
		server.quit()
		#st.success("Email enviado correctamente")
  
	except smtplib.SMTPException as e:
		st.exception("Error al enviar el mail")