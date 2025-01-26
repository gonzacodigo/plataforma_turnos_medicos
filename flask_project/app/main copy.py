from datetime import datetime, timedelta
from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_cors import CORS
import MySQLdb.cursors

# Crear una instancia de la aplicación Flask
app = Flask(__name__)

# Habilitar CORS para permitir solicitudes desde diferentes dominios
CORS(app)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Dirección del servidor MySQL
app.config['MYSQL_USER'] = 'root'      # Nombre de usuario para la base de datos
app.config['MYSQL_PASSWORD'] = ''      # Contraseña para la base de datos
app.config['MYSQL_DB'] = 'clinica'     # Nombre de la base de datos
app.config['SECRET_KEY'] = '1234'

# Inicializar la conexión con MySQL
mysql = MySQL(app)

# ================================
# Simulacro de autenticación
# ================================
@app.route('/login', methods=['POST'])
def login():
    """
    Iniciar sesión con un usuario existente en la base de datos.
    """
    data = request.get_json()
    usr_user = data.get('usr_user')
    usr_password = data.get('usr_password')

    if not usr_user or not usr_password:
        return jsonify({'error': 'Usuario y contraseña requeridos'}), 400

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE usr_user = %s AND usr_password = %s',
                   (usr_user, usr_password))
    user = cursor.fetchone()

    if user:
        session['user_id'] = user['usr_id']
        session['user_role'] = user['tip_id']  # Asignar rol
        return jsonify({'message': 'Inicio de sesión exitoso', 'user': user})
    else:
        return jsonify({'error': 'Credenciales inválidas'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    """
    Cerrar sesión del usuario actual.
    """
    session.pop('user_id', None)
    session.pop('user_role', None)
    return jsonify({'message': 'Cierre de sesión exitoso'})

# ================================
# Funciones del Administrador
# ================================
@app.route('/turns/<int:turn_id>', methods=['GET'])
def get_turn_details(turn_id):
    """
    Obtener detalles de un turno específico.
    """
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT 
            t.tur_id, t.tur_dia, t.tur_hora, t.doc_id, t.pac_id, t.est_id,
            u.usr_name AS doctor_name, u.usr_email AS doctor_email,
            p.usr_name AS patient_name, p.usr_email AS patient_email
        FROM turns t
        JOIN users u ON t.doc_id = u.usr_id
        JOIN users p ON t.pac_id = p.usr_id
        WHERE t.tur_id = %s
    ''', (turn_id,))
    turn = cursor.fetchone()

    if not turn:
        return jsonify({'error': 'Turno no encontrado'}), 404

    return jsonify(turn)

@app.route('/turns/<int:turn_id>', methods=['PUT'])
def update_turn(turn_id):
    """
    Modificar los detalles de un turno existente.
    """
    data = request.get_json()
    tur_dia = data.get('tur_dia')
    tur_hora = data.get('tur_hora')
    doc_id = data.get('doc_id')
    est_id = data.get('est_id')

    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE turns 
        SET tur_dia = %s, tur_hora = %s, doc_id = %s, est_id = %s
        WHERE tur_id = %s
    ''', (tur_dia, tur_hora, doc_id, est_id, turn_id))
    mysql.connection.commit()

    return jsonify({'message': 'Turno actualizado correctamente'})

@app.route('/turns/<int:turn_id>', methods=['DELETE'])
def delete_turn(turn_id):
    """
    Cancelar un turno existente.
    """
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM turns WHERE tur_id = %s', (turn_id,))
    mysql.connection.commit()

    return jsonify({'message': 'Turno cancelado correctamente'})

# ================================
# Bloqueo de días por el administrador
# ================================
@app.route('/block_days', methods=['POST'])
def block_days():
    """
    Bloquear días específicos (feriados o vacaciones).
    """
    data = request.get_json()
    doc_id = data.get('doc_id')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if not doc_id or not start_date or not end_date:
        return jsonify({'error': 'Datos insuficientes para bloquear días'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO doctor_availability (doc_id, start_time, end_time, status)
        VALUES (%s, %s, %s, 'blocked')
    ''', (doc_id, start_date, end_date))
    mysql.connection.commit()

    return jsonify({'message': 'Días bloqueados correctamente'})

# ================================
# Restricciones de turnos por paciente
# ================================
@app.route('/validate_patient_turn', methods=['POST'])
def validate_patient_turn():
    """
    Validar si un paciente puede sacar un turno en la misma fecha.
    """
    data = request.get_json()
    pac_id = data.get('pac_id')
    tur_dia = data.get('tur_dia')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT * FROM turns WHERE pac_id = %s AND tur_dia = %s
    ''', (pac_id, tur_dia))
    turn = cursor.fetchone()

    if turn:
        return jsonify({'error': 'El paciente ya tiene un turno reservado en esta fecha'}), 400

    return jsonify({'message': 'Validación exitosa, el paciente puede reservar'})

if __name__ == '__main__':
    app.run(debug=True)
