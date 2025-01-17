from datetime import datetime
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'clinica'

mysql = MySQL(app)

# Rutas para el CRUD de Types


@app.route('/types', methods=['GET'])
def get_types():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM types')
    types = cursor.fetchall()
    return jsonify(types)


@app.route('/types', methods=['POST'])
def create_type():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO types (tip_name) VALUES (%s)',
                   (data['tip_name'],))
    mysql.connection.commit()
    return jsonify({'message': 'Type created successfully'}), 201


@app.route('/types/<int:tip_id>', methods=['PUT'])
def update_type(tip_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE types SET tip_name = %s WHERE tip_id = %s', (data['tip_name'], tip_id))
    mysql.connection.commit()
    return jsonify({'message': 'Type updated successfully'})


@app.route('/types/<int:tip_id>', methods=['DELETE'])
def delete_type(tip_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM types WHERE tip_id = %s', (tip_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Type deleted successfully'})

# Rutas para el CRUD de Users


@app.route('/users', methods=['GET'])
def get_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return jsonify(users)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    required_fields = ['usr_user', 'usr_password', 'usr_name',
                       'usr_lastname', 'usr_dni', 'usr_email', 'usr_phone', 'tip_id']

    # Verificar que todos los campos requeridos están presentes
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO users (usr_user, usr_password, usr_name, usr_lastname, usr_dni, usr_email, usr_phone, tip_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (data['usr_user'], data['usr_password'], data['usr_name'], data['usr_lastname'], data['usr_dni'], data['usr_email'], data['usr_phone'], data['tip_id']))
    mysql.connection.commit()
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/users/<int:usr_id>', methods=['PUT'])
def update_user(usr_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE users
        SET usr_user = %s, usr_password = %s, usr_name = %s, usr_lastname = %s, usr_dni = %s, usr_email = %s, usr_phone = %s, tip_id = %s
        WHERE usr_id = %s
    ''', (data['usr_user'], data['usr_password'], data['usr_name'], data['usr_lastname'], data['usr_dni'], data['usr_email'], data['usr_phone'], data['tip_id'], usr_id))
    mysql.connection.commit()
    return jsonify({'message': 'User updated successfully'})


@app.route('/users/<int:usr_id>', methods=['DELETE'])
def delete_user(usr_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM users WHERE usr_id = %s', (usr_id,))
    mysql.connection.commit()
    return jsonify({'message': 'User deleted successfully'})


# Rutas para el CRUD de STATES
@app.route('/states', methods=['GET'])
def get_state():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM states')
    states = cursor.fetchall()
    return jsonify(states)


@app.route('/states', methods=['POST'])
def create_state():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO states (est_nombre) VALUES (%s)',
                   (data['est_nombre'],))
    mysql.connection.commit()
    return jsonify({'message': 'Type created successfully'}), 201


@app.route('/states/<int:est_id>', methods=['PUT'])
def update_state(est_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE types SET est_nombre = %s WHERE est_id = %s',
                   (data['est_nombre'], est_id))
    mysql.connection.commit()
    return jsonify({'message': 'Type updated successfully'})


@app.route('/states/<int:est_id>', methods=['DELETE'])
def delete_state(est_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM types WHERE tip_id = %s', (est_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Type deleted successfully'})


@app.route('/patients', methods=['GET'])
def get_patients():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            p.pac_id, 
            u.usr_name, 
            u.usr_lastname, 
            d.dia_descripcion,
            t.tur_dia, 
            t.tur_hora, 
            os.os_name
        FROM patients p
        JOIN users u ON p.usr_id = u.usr_id
        JOIN diagnistics d ON p.dia_id = d.dia_id
        JOIN turns t ON p.tur_id = t.tur_id
        JOIN medicares os ON p.os_id = os.os_id
    ''')
    patients = cursor.fetchall()
    return jsonify(patients)


@app.route('/patients', methods=['POST'])
def create_patients():
    data = request.get_json()

    # Validar que todos los campos requeridos estén presentes
    required_fields = ['dia_id', 'tur_id', 'usr_id', 'os_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f'Faltan los siguientes campos: {", ".join(missing_fields)}'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO patients (dia_id, tur_id, usr_id, os_id)
        VALUES (%s, %s, %s, %s)
    ''', (data['dia_id'], data['tur_id'], data['usr_id'], data['os_id']))
    mysql.connection.commit()

    return jsonify({'message': 'Paciente registrado correctamente'}), 201



@app.route('/patients/<int:pac_id>', methods=['DELETE'])
def delete_patients(pac_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM patients WHERE pac_id = %s', (pac_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Type deleted successfully'})

##### Administradores pablo ############


@app.route('/administrators', methods=['GET'])
def get_administrators():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM administrators')
    users = cursor.fetchall()
    return jsonify(users)


@app.route('/administrators', methods=['POST'])
def create_administrators():
    data = request.get_json()
    usr_id = data['usr_id']
    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO administrators (usr_id) VALUES (%s)', (usr_id,))
    mysql.connection.commit()
    return jsonify({'message': 'User created successfully'}), 201


@app.route('/administrators/<int:adm_id>', methods=['PUT'])
def update_administrators(adm_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE administrators SET usr_id = %s
        WHERE adm_id = %s
        ''', (data['usr_id'], adm_id))
    mysql.connection.commit()
    return jsonify({'message': 'administrators updated successfully'})


@app.route('/administrators/<int:adm_id>', methods=['DELETE'])
def delete_administrators(adm_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM administrators WHERE adm_id = %s', (adm_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Administradro deleted successfully'})

# Rutas para el CRUD de specialities
# Realizado por Daniel


@app.route('/specialities', methods=['GET'])
def get_specialities():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM specialities')
    specialities = cursor.fetchall()
    return jsonify(specialities)


@app.route('/specialities/<int:esp_id>', methods=['GET'])
def get_speciality(esp_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM specialities WHERE esp_id = %s', (esp_id,))
    speciality = cursor.fetchone()
    return jsonify(speciality)


@app.route('/specialities/<int:esp_id>', methods=['DELETE'])
def delete_speciality(esp_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM specialities WHERE esp_id = %s', (esp_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Speciality deleted successfully'})


@app.route('/specialities', methods=['POST'])
def create_speciality():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO specialities (esp_name) VALUES (%s)', (data['esp_name'],))
    mysql.connection.commit()
    return jsonify({'message': 'Speciality created successfully'}), 201


@app.route('/specialities/<int:esp_id>', methods=['PUT'])
def update_speciality(esp_id):
    data = request.get_json()
    esp_name = data['esp_name']
    cursor = mysql.connection.cursor()
    cursor.execute(
        'UPDATE specialities SET esp_name = %s WHERE esp_id = %s', (esp_name, esp_id))
    mysql.connection.commit()
    return jsonify({'message': 'Speciality updated successfully'})


# Rutas para el CRUD de schedules
# Realizado por Daniel

@app.route('/schedules', methods=['GET'])
def get_schedules():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM schedules')
    column_names = [desc[0] for desc in cursor.description]
    schedules = []

    for row in cursor.fetchall():
        row_dict = dict(zip(column_names, row))

        # Convierte timedelta a string (HH:MM:SS)
        for key, value in row_dict.items():
            if isinstance(value, datetime.timedelta):
                row_dict[key] = str(value)  # Convertir timedelta a cadena

        schedules.append(row_dict)

    return jsonify(schedules)


@app.route('/schedules', methods=['POST'])
def create_schedule():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO schedules (hor_dia, hor_franja, hor_duracion) VALUES (%s, %s, %s)',
                   (data['hor_dia'], data['hor_franja'], data['hor_duracion']))
    mysql.connection.commit()
    return jsonify({'message': 'Schedule created successfully'}), 201


@app.route('/schedules/<int:hor_id>', methods=['PUT'])
def update_schedule(hor_id):
    data = request.get_json()
    hor_dia = data['hor_dia']
    hor_franja = data['hor_franja']
    hor_duracion = data['hor_duracion']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE schedules SET hor_dia = %s, hor_franja = %s, hor_duracion = %s WHERE hor_id = %s',
                   (hor_dia, hor_franja, hor_duracion, hor_id))
    mysql.connection.commit()
    return jsonify({'message': 'Schedule updated successfully'})


@app.route('/schedules/<int:hor_id>', methods=['DELETE'])
def delete_schedule(hor_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM schedules WHERE hor_id = %s', (hor_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Schedule deleted successfully'})

# Rutas para el CRUD de doctors
# Realizado por Daniel


@app.route('/doctors', methods=['GET'])
def get_doctors():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            d.doc_id, 
            d.doc_matricula, 
            u.usr_name, 
            u.usr_lastname, 
            s.esp_name, 
            sch.hor_dia, 
            TIME_FORMAT(sch.hor_franja, '%H:%i') AS hor_franja, 
            TIME_FORMAT(sch.hor_duracion, '%H:%i') AS hor_duracion
        FROM doctors d
        JOIN users u ON d.usr_id = u.usr_id
        JOIN specialities s ON d.esp_id = s.esp_id
        JOIN schedules sch ON d.hor_id = sch.hor_id
    ''')
    doctors = cursor.fetchall()
    return jsonify(doctors)


@app.route('/doctors', methods=['POST'])
def create_doctor():
    data = request.get_json()
    doc_matricula = data['doc_matricula']
    usr_id = data['usr_id']
    esp_id = data['esp_id']
    hor_id = data['hor_id']
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO doctors (doc_matricula, usr_id, esp_id, hor_id) VALUES (%s, %s,%s,%s)',
                   (doc_matricula, usr_id, esp_id, hor_id))
    mysql.connection.commit()
    return jsonify({'message': 'Doctor created successfully'}), 201


@app.route('/doctors/<int:doc_id>', methods=['PUT'])
def update_doctor(doc_id):
    data = request.get_json()
    doc_matricula = data['doc_matricula']
    usr_id = data['usr_id']
    esp_id = data['esp_id']
    hor_id = data['hor_id']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE doctors SET doc_matricula = %s, usr_id = %s, esp_id = %s, hor_id = %s WHERE doc_id = %s',
                   (doc_matricula, usr_id, esp_id, hor_id, doc_id))
    mysql.connection.commit()
    return jsonify({'message': 'Doctor updated successfully'})


@app.route('/doctors/<int:doc_id>', methods=['GET'])
def get_doctor(doc_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            d.doc_id, 
            d.doc_matricula, 
            d.usr_id, 
            d.esp_id, 
            d.hor_id
        FROM doctors d
        WHERE d.doc_id = %s
    ''', (doc_id,))
    doctor = cursor.fetchone()
    if not doctor:
        return jsonify({'error': 'Doctor no encontrado'}), 404
    return jsonify(doctor)


@app.route('/doctors/<int:doc_id>', methods=['DELETE'])
def delete_doctor(doc_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM doctors WHERE doc_id = %s', (doc_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Doctor deleted successfully'})

######## doctors _ Medicares tabla intermedia #################
# pablo


@app.route('/doctors_medicares', methods=['GET'])
def get_doctors_medicares():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM doctors_medicares')
    users = cursor.fetchall()
    return jsonify(users)


@app.route('/doctors_medicares', methods=['POST'])
def create_doctors_medicares():
    data = request.get_json()
    doc_id = data['doc_id']
    os_id = data['os_id']
    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO doctors_medicares (doc_id, os_id) VALUES (%s,%s)', (doc_id, os_id,))
    mysql.connection.commit()
    return jsonify({'message': 'doctors_medicares created successfully'}), 201


@app.route('/doctors_medicares/<int:id>', methods=['PUT'])
def update_doctors_medicares(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE doctors_medicares SET doc_id = %s, os_id= %s
        WHERE id = %s
    ''', (data['doc_id'], data['os_id'], id))
    mysql.connection.commit()
    return jsonify({'message': 'doctors_medicares updated successfully'})


@app.route('/doctors_medicares/<int:id>', methods=['DELETE'])
def delete_doctors_medicares(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM doctors_medicares WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({'message': 'doctors_medicares deleted successfully'})

################# medicares  ###########
# pablo


@app.route('/medicares', methods=['GET'])
def get_medicares():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM medicares')
    users = cursor.fetchall()
    return jsonify(users)


@app.route('/medicares', methods=['POST'])
def post_medicares():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''INSERT INTO medicares(os_name) 
                   VALUES (%s)''', (data['os_name'],))
    mysql.connection.commit()
    return jsonify({'message': 'medicares created successfully'}), 201


@app.route('/medicares/<int:os_id>', methods=['PUT'])
def update_medicares(os_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE medicares SET os_name= %s
        WHERE os_id = %s
    ''', (data['os_name'], os_id,))
    mysql.connection.commit()
    return jsonify({'message': 'medicares updated successfully'})


@app.route('/medicares/<int:os_id>', methods=['DELETE'])
def delete_medicares(os_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM medicares WHERE os_id = %s', (os_id,))
    mysql.connection.commit()
    return jsonify({'message': 'medicares deleted successfully'})

# CRUD realizado por Jose
# Ruta para obtener los receptionists


@app.route('/receptionists', methods=['GET'])
def get_receptionists():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM receptionists')
    receptionists = cursor.fetchall()
    return jsonify(receptionists)

# Ruta para crear un nuevo receptionist


@app.route('/receptionists', methods=['POST'])
def create_receptionist():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO receptionists (rec_turn, usr_id) VALUES (%s, %s)',
                   (data['rec_turn'], data['usr_id']))
    mysql.connection.commit()
    return jsonify({'message': 'Receptionist created successfully'}), 201

# Ruta para actualizar un receptionist


@app.route('/receptionists/<int:rec_id>', methods=['PUT'])
def update_receptionist(rec_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE receptionists SET rec_turn = %s, usr_id = %s WHERE rec_id = %s',
                   (data['rec_turn'], data['usr_id'], rec_id))
    mysql.connection.commit()
    return jsonify({'message': 'Receptionist updated successfully'})

# Ruta para eliminar un receptionist


@app.route('/receptionists/<int:rec_id>', methods=['DELETE'])
def delete_receptionist(rec_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM receptionists WHERE rec_id = %s', (rec_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Receptionist deleted successfully'})


# CRUD realizado por Jose
# Ruta para obtener los diagnósticos (diagnistics)
@app.route('/diagnistics', methods=['GET'])
def get_diagnistics():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM diagnistics')
    diagnistics = cursor.fetchall()
    return jsonify(diagnistics)

# Ruta para crear un nuevo diagnóstico (diagnistic)


@app.route('/diagnistics', methods=['POST'])
def create_diagnistic():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO diagnistics (dia_descripcion, pac_id) 
        VALUES (%s, %s)
    ''', (data['dia_descripcion'], data['pac_id']))
    mysql.connection.commit()
    return jsonify({'message': 'Diagnistic created successfully'}), 201

# Ruta para actualizar un diagnóstico (diagnistic)


@app.route('/diagnistics/<int:dia_id>', methods=['PUT'])
def update_diagnistic(dia_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE diagnistics 
        SET dia_descripcion = %s, pac_id = %s 
        WHERE dia_id = %s
    ''', (data['dia_descripcion'], data['pac_id'], dia_id))
    mysql.connection.commit()
    return jsonify({'message': 'Diagnistic updated successfully'})

# Ruta para eliminar un diagnóstico (diagnistic)


@app.route('/diagnistics/<int:dia_id>', methods=['DELETE'])
def delete_diagnistic(dia_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM diagnistics WHERE dia_id = %s', (dia_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Diagnistic deleted successfully'})


@app.route('/turns', methods=['GET'])
def get_turns():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT 
            tur_dia, 
            TIME_FORMAT(tur_hora, '%H:%i:%s') AS tur_hora, 
            doc_id, 
            pac_id, 
            est_id 
        FROM turns
    """)
    turns = cursor.fetchall()

    # Formatear los datos para FullCalendar
    events = [
        {
            "title": f"Turno de paciente {turn['pac_id']}",
            "start": f"{turn['tur_dia']}T{turn['tur_hora']}",
            "end": f"{turn['tur_dia']}T{turn['tur_hora']}",
        }
        for turn in turns
    ]
    return jsonify(events)


# Obtener los eventos en formato compatible con FullCalendar

# Crear un nuevo turno
@app.route('/turns', methods=['POST'])
def create_turns():
    data = request.get_json()

    try:
        # Validar formato de fecha y hora
        datetime.strptime(data['tur_dia'], '%Y-%m-%d')
        datetime.strptime(data['tur_hora'], '%H:%M:%S')

        # Verificar campos obligatorios
        if not all([data.get('doc_id'), data.get('pac_id'), data.get('est_id')]):
            return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Datos inválidos o faltantes', 'details': str(e)}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO turns (tur_dia, tur_hora, doc_id, pac_id, est_id) VALUES (%s, %s, %s, %s, %s)',
        (data['tur_dia'], data['tur_hora'],
         data['doc_id'], data['pac_id'], data['est_id'])
    )
    mysql.connection.commit()
    return jsonify({'message': 'Turno creado exitosamente'}), 201

# Obtener días bloqueados (vacaciones/festivos) de los doctores


@app.route('/doctor_availability', methods=['GET'])
def get_blocked_days():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT 
            id,
            doc_id, 
            DATE_FORMAT(start_time, '%Y-%m-%d') AS start_time, 
            DATE_FORMAT(end_time, '%Y-%m-%d') AS end_time, 
            status
        FROM doctor_availability
    """)
    doctor_availability = cursor.fetchall()

    events = [
        {
            "title": f"VACACIONES DEL DOCTOR {doc_avai['doc_id']}",
            "start": doc_avai["start_time"],
            "end": doc_avai["end_time"],
            "status": doc_avai["status"],
            "allDay": True
        }
        for doc_avai in doctor_availability
    ]
    return jsonify(events)


# Crear un nuevo registro de disponibilidad del doctor
@app.route('/doctor_availability', methods=['POST'])
def create_doctor_availability():
    data = request.get_json()

    if not all(key in data for key in ('doc_id', 'start_time', 'end_time', 'status')):
        return jsonify({'error': 'Faltan campos obligatorios'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        'INSERT INTO doctor_availability (doc_id, start_time, end_time, status) VALUES (%s, %s, %s, %s)',
        (data['doc_id'], data['start_time'], data['end_time'], data['status'])
    )
    mysql.connection.commit()
    return jsonify({'message': 'Disponibilidad creada exitosamente'}), 201


# Eliminar disponibilidad del doctor
@app.route('/doctor_availability/<int:id>', methods=['DELETE'])
def delete_doctor_availability(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM doctor_availability WHERE id = %s', (id,))
    mysql.connection.commit()
    return jsonify({'message': 'Disponibilidad eliminada exitosamente'}), 200


@app.route('/types/options', methods=['GET'])
def get_types_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT tip_id, tip_name FROM types')
    types = cursor.fetchall()
    return jsonify(types)


@app.route('/specialities/options', methods=['GET'])
def get_specialities_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT esp_id, esp_name FROM specialities')
    specialities = cursor.fetchall()
    return jsonify(specialities)


@app.route('/schedules/options', methods=['GET'])
def get_schedules_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT hor_id, 
               hor_dia, 
               TIME_FORMAT(hor_franja, '%H:%i') AS hor_franja,
               TIME_FORMAT(hor_duracion, '%H:%i') AS hor_duracion
        FROM schedules
    ''')
    schedules = cursor.fetchall()
    # Combinar campos para un formato legible
    for schedule in schedules:
        schedule['horario'] = f"{schedule['hor_dia']} ({schedule['hor_franja']} - {schedule['hor_duracion']})"
    return jsonify(schedules)

# Opciones para obras sociales


@app.route('/medicares/options', methods=['GET'])
def get_medicares_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT os_id, os_name FROM medicares')
    medicares = cursor.fetchall()
    return jsonify(medicares)

# Opciones para diagnósticos


@app.route('/diagnistics/options', methods=['GET'])
def get_diagnistics_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT dia_id, dia_descripcion FROM diagnistics')
    diagnistics = cursor.fetchall()
    return jsonify(diagnistics)


@app.route('/turns/options', methods=['GET'])
def get_turns_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            tur_id, 
            tur_dia, 
            TIME_FORMAT(tur_hora, '%H:%i:%s') AS tur_hora
        FROM turns
    ''')
    turns = cursor.fetchall()
    # Crear una descripción legible combinando fecha y hora
    for turn in turns:
        turn['descripcion'] = f"{turn['tur_dia']} a las {turn['tur_hora']}"
    return jsonify(turns)

@app.route('/doctors/options', methods=['GET'])
def get_doctors_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            d.doc_id,
            d.doc_matricula,
            d.doc_type,
            u.usr_name AS doctor_name,
            e.esp_name AS speciality,
            GROUP_CONCAT(DISTINCT m.os_name) AS medicares,
            CONCAT(da.date, ' (', TIME_FORMAT(da.start_time, '%H:%i'), ' - ', TIME_FORMAT(da.end_time, '%H:%i'), ')') AS availability
        FROM doctors d
        LEFT JOIN users u ON d.usr_id = u.usr_id
        LEFT JOIN specialities e ON d.esp_id = e.esp_id
        LEFT JOIN doctors_medicares dm ON d.doc_id = dm.doc_id
        LEFT JOIN medicares m ON dm.os_id = m.os_id
        LEFT JOIN doctor_availability da ON d.doc_id = da.doc_id
        GROUP BY d.doc_id, d.doc_matricula, d.doc_type, u.usr_name, e.esp_name
    ''')
    doctors = cursor.fetchall()
    
    # Formatear datos si es necesario
    for doctor in doctors:
        doctor['medicares'] = doctor['medicares'].split(',') if doctor['medicares'] else []

    return jsonify(doctors)

@app.route('/patients/options', methods=['GET'])
def get_patients_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            p.pac_id, 
            u.usr_name AS patient_name,
            d.dia_descripcion AS diagnosis,
            CONCAT(t.tur_dia, ' a las ', TIME_FORMAT(t.tur_hora, '%H:%i:%s')) AS turn,
            m.os_name AS medicare
        FROM patients p
        LEFT JOIN users u ON p.usr_id = u.usr_id
        LEFT JOIN diagnistics d ON p.dia_id = d.dia_id
        LEFT JOIN turns t ON p.tur_id = t.tur_id
        LEFT JOIN medicares m ON p.os_id = m.os_id
    ''')
    patients = cursor.fetchall()

    # Formatear datos para una representación más clara si es necesario
    for patient in patients:
        patient['description'] = f"{patient['patient_name']} - {patient['diagnosis']} - {patient['turn']} ({patient['medicare']})"

    return jsonify(patients)


@app.route('/states/options', methods=['GET'])
def get_states_options():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            est_id, 
            est_nombre 
        FROM states
    ''')
    states = cursor.fetchall()

    # Formatear los datos para una representación más clara si es necesario
    for state in states:
        state['description'] = state['est_nombre']

    return jsonify(states)


if __name__ == '__main__':
    app.run(debug=True)
