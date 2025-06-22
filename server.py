from flask import Flask, jsonify, request
import database as db

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins (for development)

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
    user_id = str(request.args.get("user_id"))
    exercise = current_exercises.get(user_id, -1)
    return jsonify({"current_exercise" : exercise}), 200


@app.route('/setCurrentExercise', methods=['POST'])
def set_current_exercise():
    r = request.get_json()
    user_id = str(r.get("user_id"))
    exercise_id = r.get("exercise_id")
    set_id = r.get("set_id")
    if exercise_id < 0:
        current_exercises.pop(user_id,-1)
        return jsonify({"message": "Exercise removed"}), 200
    
    current_exercises[user_id] = {"exercise" : exercise_id, "set_id" : set_id}
    print("Set exercise: ",user_id,current_exercises[user_id])
    return jsonify({"message" : "Exercise set"}), 200


@app.route('/dbGet', methods=['GET'])
def db_get():
    table = request.args.get("table")
    data = db.query(table)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/getPatient', methods=['GET'])
def get_patient():
    user = request.args.get("user_id")
    data = db.get_patient_info(user)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/getSession', methods=['GET'])
def get_session():
    session = request.args.get("session_id")
    data = db.get_session_info(session)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/getExercise', methods=['GET'])
def get_exercise():
    exercise = request.args.get("exercise_id")
    data = db.get_exercise_info(exercise)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500


@app.route('/userSessions', methods=['GET'])
def get_user_sessions():
    user = request.args.get("user_id")
    data = db.get_user_sessions(user)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/sets', methods=['GET'])
def get_sets():
    session = request.args.get("session_id")
    data = db.get_sets(session)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/poxExercise', methods=['GET'])
def get_pox_from_exercise():
    set_id = request.args.get("set_id")
    data = db.get_pox(set_id)
    if data:
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Database query failed'}), 500
    

@app.route('/kinectExercise', methods=['GET'])
def get_kinect_from_exercise():
    set_id = request.args.get("set_id")
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
    

@app.route('/createSession', methods=['POST'])
def create_session():
    data = request.get_json()
    user_id = data.get("user_id")
    id = db.create_session(user_id)
    if id is not None:
        return jsonify({'id': id}), 201
    else:
        return jsonify({'error': 'Data insertion failed'}), 500

@app.route('/finishSession', methods=['POST'])
def finish_session_route():
    data = request.get_json()
    session_id = data.get("session_id")
    
    success = db.finish_session(session_id)
    if success:
        return jsonify({'message': 'Session finished successfully'}), 200
    else:
        return jsonify({'error': 'Failed to finish session'}), 500

@app.route('/addExercise', methods=["POST"])
def add_exercise():
    data = request.get_json()
    session_id = data.get("session_id")
    exercise_id = data.get("exercise_id")
    reps = data.get("reps")
    weight = data.get("weight")
    id = db.add_exercise(session_id, exercise_id, reps, weight)
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
        duration = max(d["ts"] for d in data) - min(d["ts"] for d in data)
        if db.set_metrics(set_id, mean_hr, mean_br, duration):
            return jsonify({'message': 'Metrics set successfully'}), 201
        else:
            return jsonify({'error': 'Data insertion failed'}), 500
    else:
        return jsonify({'error': 'Exercise not found'}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
