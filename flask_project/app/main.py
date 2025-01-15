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


if __name__ == '__main__':
    app.run(debug=True)
