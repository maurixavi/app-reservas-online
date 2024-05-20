import pandas as pd
import streamlit as st

# Leer el archivo Excel
def leer_reservas():
    try:
        reservas = pd.read_excel('reservas.xlsx', sheet_name='reservas')
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        columnas = ['nombre', 'email', 'fecha', 'hora', 'cancha']
        reservas = pd.DataFrame(columns=columnas)
    return reservas

# Guardar reservas en el archivo Excel
def guardar_reserva(nombre, email, fecha, hora, cancha):
    reservas = leer_reservas()
    nueva_reserva = pd.DataFrame({
        'nombre': [nombre],
        'email': [email],
        'fecha': [fecha],
        'hora': [hora],
        'cancha': [cancha]
    })
    reservas_actualizadas = reservas.append(nueva_reserva, ignore_index=True)
    reservas_actualizadas.to_excel('reservas.xlsx', sheet_name='reservas', index=False)

# Verificar disponibilidad
def verificar_disponibilidad(fecha, hora, cancha):
    reservas = leer_reservas()
    reserva_existente = reservas[(reservas['fecha'] == fecha) & (reservas['hora'] == hora) & (reservas['cancha'] == cancha)]
    return reserva_existente.empty

# Obtener disponibilidad
def obtener_disponibilidad(fecha):
    reservas = leer_reservas()
    reservas_fecha = reservas[reservas['fecha'] == fecha]
    horarios_disponibles = ['08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']
    canchas = ['Cancha 1', 'Cancha 2', 'Cancha 3', 'Cancha 4']
    disponibilidad = [(hora, cancha) for hora in horarios_disponibles for cancha in canchas if ((reservas_fecha['hora'] == hora) & (reservas_fecha['cancha'] == cancha)).sum() == 0]
    return disponibilidad
