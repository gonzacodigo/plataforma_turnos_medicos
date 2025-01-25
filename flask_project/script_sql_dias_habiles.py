from datetime import datetime, timedelta

# Configuraciones
DOC_ID = 2  # ID del doctor
START_TIME = "08:00:00"  # Hora de inicio
END_TIME = "20:00:00"  # Hora de fin
STATUS = "available"  # Estado de la disponibilidad
YEAR = 2025  # Año para generar la disponibilidad

# Función para verificar si un día es lunes a viernes
def is_weekday(date):
    return date.weekday() < 5  # 0: lunes, 4: viernes

# Generar todas las fechas del año
start_date = datetime(YEAR, 1, 1)  # Primer día del año
end_date = datetime(YEAR, 12, 31)  # Último día del año
current_date = start_date

# Almacenar las consultas generadas
queries = []

while current_date <= end_date:
    if is_weekday(current_date):  # Solo lunes a viernes
        query = f"INSERT INTO `doctor_availability` (`id`, `doc_id`, `date`, `start_time`, `end_time`, `status`) VALUES (NULL, '{DOC_ID}', '{current_date.strftime('%Y-%m-%d')}', '{START_TIME}', '{END_TIME}', '{STATUS}');"
        queries.append(query)  # Agregar la consulta a la lista
    current_date += timedelta(days=1)  # Pasar al siguiente día

# Guardar las consultas en un archivo SQL
with open("doctor_availability_2025.sql", "w") as file:
    file.write("\n".join(queries))

print("Script generado y guardado como 'doctor_availability_2025.sql'.")