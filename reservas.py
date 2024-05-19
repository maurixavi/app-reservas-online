# reservas.py
import pandas as pd
from datetime import datetime

def obtener_fecha_actual():
  return datetime.now().strftime('%Y-%m-%d')

def obtener_timestamp_actual():
  return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# Guardar reservas en el archivo Excel
def guardar_reserva(nombre, email, fecha, hora, cancha):
    try:
        reservas = pd.read_excel('data/reservas.xlsx', sheet_name='reservas')
        if 'id' in reservas.columns:
            last_id = reservas['id'].max()
        else:
            last_id = 0
    except FileNotFoundError:
        # Si el archivo no existe, crear un DataFrame vacío
        columnas = ['id', 'nombre', 'email', 'fecha', 'hora', 'cancha']
        reservas = pd.DataFrame(columns=columnas)
        last_id = 0
    
    new_id = last_id + 1
    timestamp_actual = obtener_timestamp_actual()
    
    nueva_reserva = pd.DataFrame({
      	'id': [new_id],
        'nombre': [nombre],
        'email': [email],
        'fecha': [fecha],
        'hora': [hora],
        'cancha': [cancha],
        'timestamp': [timestamp_actual]
    })
    
    reservas_actualizadas = pd.concat([reservas, nueva_reserva], ignore_index=True)
    #reservas_actualizadas = reservas.append(nueva_reserva, ignore_index=True)
    reservas_actualizadas.to_excel('data/reservas.xlsx', sheet_name='reservas', index=False)
