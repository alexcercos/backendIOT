from flask import Flask, jsonify, request
import database as db


app = Flask(__name__)

current_exercises = {}

@app.route('/sendPox', methods=['POST'])
def send_pox():
    r = request.get_json()
    if db.add_pox(r):
        return jsonify({'message': 'Pox data added successfully'}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500


@app.route('/sendKinect', methods=['POST'])
def send_kinect():
    r = request.get_json()
    if db.add_kinect(r):
        return jsonify({'message': 'Kinect data added successfully'}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500
    

@app.route('/getCurrentExercise', methods=['GET'])
def get_current_exercise():
    r = request.get_json()
    user_id = r.get("user_id")
    exercise = current_exercises.get(user_id, -1)
    return jsonify({"current_exercise" : exercise}), 200


@app.route('/setCurrentExercise', methods=['POST'])
def set_current_exercise():
    r = request.get_json()
    user_id = r.get("user_id")
    exercise_id = r.get("exercise_id")
    set_id = r.get("set_id")
    current_exercises[user_id] = {"exercise" : exercise_id, "set_id" : set_id}
    return jsonify({"message" : "Exercise set"}), 200


@app.route('/dbGet', methods=['GET'])
def db_get():
    r = request.get_json()
    table = r.get("table")
    data = db.query(table)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/getPatient', methods=['GET'])
def get_patient():
    r = request.get_json()
    user = r.get("user_id")
    data = db.get_patient_info(user)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/getSession', methods=['GET'])
def get_session():
    r = request.get_json()
    session = r.get("session_id")
    data = db.get_session_info(session)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/getExercise', methods=['GET'])
def get_exercise():
    r = request.get_json()
    exercise = r.get("exercise_id")
    data = db.get_exercise_info(exercise)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500


@app.route('/userSessions', methods=['GET'])
def get_user_sessions():
    r = request.get_json()
    user = r.get("user_id")
    data = db.get_user_sessions(user)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/sets', methods=['GET'])
def get_sets():
    r = request.get_json()
    session = r.get("session_id")
    data = db.get_sets(session)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/poxExercise', methods=['GET'])
def get_pox_from_exercise():
    r = request.get_json()
    set_id = r.get("set_id")
    data = db.get_pox(set_id)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/kinectExercise', methods=['GET'])
def get_kinect_from_exercise():
    r = request.get_json()
    set_id = r.get("set_id")
    data = db.get_kinect(set_id)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/createUser', methods=['POST'])
def create_user():
    data = request.get_json()
    usr = data.get('username')
    psw = data.get('password')
    user_type = data.get("user_type")
    other_data = {}
    if user_type == "Patient":
        other_data["age"] = data.get("age")
        other_data["height"] = data.get("height")
        other_data["weight"] = data.get("weight")
        other_data["therapist_id"] = data.get("therapist_id")
    if db.create_user(usr, psw, user_type, other_data):
        return jsonify({'message': 'User created successfully'}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500
    

@app.route('/createExercise', methods=['POST'])
def create_exercise():
    data = request.get_json()
    if db.create_exercise(data):
        return jsonify({'message': 'Exercise created successfully'}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500
    

@app.route('/createSession', methods=['POST'])
def create_session():
    data = request.get_json()
    user_id = data.get("user_id")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    id = db.create_session(user_id, start_time, end_time)
    if id is not None:
        return jsonify({'id': id}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500
    

@app.route('/addExercise', methods=["POST"])
def add_exercise():
    data = request.get_json()
    session_id = data.get("session_id")
    exercise_id = data.get("exercise_id")
    date = data.get("date")
    id = db.add_exercise(session_id, exercise_id, date)
    if id is not None:
        return jsonify({'id': id}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500
    

@app.route('/setMetrics', methods=['POST'])
def set_metrics():
    r = request.get_json()
    set_id = r.get("set_id")
    data = db.get_pox(set_id)
    if len(data) > 0:
        mean_hr = sum(d["heart_rate"] for d in data) / len(data)
        mean_br = sum(d["breath_rate"] for d in data) / len(data)
        if db.set_metrics(set_id, mean_hr, mean_br):
            return jsonify({'message': 'Metrics set successfully'}), 201
        else:
            return jsonify({'error': 'Data insertion failed'}), 500
    else:
        return jsonify({'error': 'Exercise not found'}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
