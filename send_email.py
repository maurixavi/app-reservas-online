from email import message
import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


def send(email, nombre, fecha, hora, cancha):
	user = st.secrets["smtp_user"]
	password = st.secrets["smtp_password"]
 
	sender_email = "Padel Club"
 
	msg = MIMEMultipart()
 
	smtp_server = "smtp.gmail.com"
	smtp_port = 587
 
	msg['From'] = sender_email
	msg['To'] = email
	msg['Subject'] = "Reserva de cancha"
	
	# Cargar la imagen y adjuntarla al mensaje
	with open('assets/img/PadelClubBanner.jpg', 'rb') as f:
		image = MIMEImage(f.read())
		image.add_header('Content-ID', '<logo>')
		msg.attach(image)

	message = f"""
	<html>
	<body>
		<p>Hola {nombre},</p>
		<p>Su reserva ha sido realizada con éxito.</p>
		<p>Fecha: {fecha}</p>
		<p>Hora: {hora}</p>
		<p>Cancha: {cancha}</p>
		<p>Gracias por elegirnos.</p>
		<p>Padel Club.</p>
		<img src="cid:logo" style="display: block; margin: 0 auto;">
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