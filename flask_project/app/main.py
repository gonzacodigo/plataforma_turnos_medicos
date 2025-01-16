from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

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
    cursor.execute('INSERT INTO types (tip_name) VALUES (%s)', (data['tip_name'],))
    mysql.connection.commit()
    return jsonify({'message': 'Type created successfully'}), 201

@app.route('/types/<int:tip_id>', methods=['PUT'])
def update_type(tip_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE types SET tip_name = %s WHERE tip_id = %s', (data['tip_name'], tip_id))
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
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO users (usr_id, usr_user, usr_password, usr_name, usr_lastname, usr_dni, usr_email, usr_phone, tip_id)
        VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)
    ''', (data['usr_id'],data['usr_user'], data['usr_password'], data['usr_name'], data['usr_lastname'], data['usr_dni'], data['usr_email'], data['usr_phone'], data['tip_id']))
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
    cursor.execute('INSERT INTO states (est_nombre) VALUES (%s)', (data['est_nombre'],))
    mysql.connection.commit()
    return jsonify({'message': 'Type created successfully'}), 201

@app.route('/states/<int:est_id>', methods=['PUT'])
def update_state(est_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE types SET est_nombre = %s WHERE est_id = %s', (data['est_nombre'], est_id))
    mysql.connection.commit()
    return jsonify({'message': 'Type updated successfully'})

@app.route('/states/<int:est_id>', methods=['DELETE'])
def delete_state(est_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM types WHERE tip_id = %s', (est_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Type deleted successfully'})



# Rutas para el CRUD de PATIENTS
@app.route('/patients', methods=['GET'])
def get_patients():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patients')
    patients = cursor.fetchall()
    return jsonify(patients)

@app.route('/patients', methods=['POST'])
def create_patients():
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO patients (pac_id, dia_id, tur_id, usr_id, os_id) VALUES (%s, %s, %s, %s, %s)', (data['pac_id'],data['dia_id'],data['tur_id'],data['usr_id'],data['os_id'],))
    mysql.connection.commit()
    return jsonify({'message': 'Type created successfully'}), 201


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
    cursor.execute('INSERT INTO specialities (esp_name) VALUES (%s)', (data['esp_name'],))
    mysql.connection.commit()
    return jsonify({'message': 'Speciality created successfully'}),201

@app.route('/specialities/<int:esp_id>', methods=['PUT'])
def update_speciality(esp_id):
    data = request.get_json()
    esp_name = data['esp_name']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE specialities SET esp_name = %s WHERE esp_id = %s', (esp_name, esp_id))
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
    cursor.execute('INSERT INTO schedules (hor_dia, hor_franja, hor_duracion) VALUES (%s, %s, %s)', (data['hor_dia'], data['hor_franja'], data['hor_duracion']))
    mysql.connection.commit()
    return jsonify({'message': 'Schedule created successfully'}),201

@app.route('/schedules/<int:hor_id>', methods=['PUT'])
def update_schedule(hor_id):
    data = request.get_json()
    hor_dia = data['hor_dia']
    hor_franja = data['hor_franja']
    hor_duracion = data['hor_duracion']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE schedules SET hor_dia = %s, hor_franja = %s, hor_duracion = %s WHERE hor_id = %s', (hor_dia, hor_franja, hor_duracion, hor_id))
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
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM doctors')
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
    cursor.execute('INSERT INTO doctors (doc_matricula, usr_id, esp_id, hor_id) VALUES (%s, %s,%s,%s)', (doc_matricula, usr_id, esp_id, hor_id))
    mysql.connection.commit()
    return jsonify({'message': 'Doctor created successfully'}),201

@app.route('/doctors/<int:doc_id>', methods=['PUT'])
def update_doctor(doc_id):
    data = request.get_json()
    doc_matricula = data['doc_matricula']
    usr_id = data['usr_id']
    esp_id = data['esp_id']
    hor_id = data['hor_id']
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE doctors SET doc_matricula = %s, usr_id = %s, esp_id = %s, hor_id = %s WHERE doc_id = %s', (doc_matricula, usr_id, esp_id, hor_id, doc_id))
    mysql.connection.commit()
    return jsonify({'message': 'Doctor updated successfully'})

@app.route('/doctors/<int:doc_id>', methods=['DELETE'])
def delete_doctor(doc_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM doctors WHERE doc_id = %s', (doc_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Doctor deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
