CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS therapist (
    id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS patient (
    id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    age INT NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL,
    therapist_id INT REFERENCES therapist(id) ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS exercise (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES patient(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sets (
    id SERIAL PRIMARY KEY,
    session_id INT REFERENCES sessions(id) ON DELETE CASCADE,
    exercise_id INT REFERENCES exercise(id) ON DELETE RESTRICT,
    mean_heart_rate FLOAT NOT NULL,
    mean_breath_rate FLOAT NOT NULL,
    duration FLOAT NOT NULL,
    reps INT NOT NULL,
    weight FLOAT,
    date DATE NOT NULL DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS pox_data (
    id SERIAL PRIMARY KEY,
    ts FLOAT NOT NULL,
    set_id INT REFERENCES sets(id) ON DELETE CASCADE,
    total_phase FLOAT NOT NULL,
    breath_phase FLOAT NOT NULL,
    heart_phase FLOAT NOT NULL,
    breath_rate FLOAT NOT NULL,
    heart_rate FLOAT NOT NULL,
    distance FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS kinect_data (
    id SERIAL PRIMARY KEY,
    ts FLOAT NOT NULL,
    set_id INT REFERENCES sets(id) ON DELETE CASCADE,
    spine_base VARCHAR(100) NOT NULL,
    spine_mid VARCHAR(100) NOT NULL,
    neck VARCHAR(100) NOT NULL,
    head VARCHAR(100) NOT NULL,
    shoulder_left VARCHAR(100) NOT NULL,
    elbow_left VARCHAR(100) NOT NULL,
    wrist_left VARCHAR(100) NOT NULL,
    hand_left VARCHAR(100) NOT NULL,
    shoulder_right VARCHAR(100) NOT NULL,
    elbow_right VARCHAR(100) NOT NULL,
    wrist_right VARCHAR(100) NOT NULL,
    hand_right VARCHAR(100) NOT NULL,
    hip_left VARCHAR(100) NOT NULL,
    knee_left VARCHAR(100) NOT NULL,
    ankle_left VARCHAR(100) NOT NULL,
    foot_left VARCHAR(100) NOT NULL,
    hip_right VARCHAR(100) NOT NULL,
    knee_right VARCHAR(100) NOT NULL,
    ankle_right VARCHAR(100) NOT NULL,
    foot_right VARCHAR(100) NOT NULL,
    spine_shoulder VARCHAR(100) NOT NULL,
    completness FLOAT NOT NULL,
    instability FLOAT NOT NULL
);

WITH
    new_therapist AS (
        INSERT INTO users(username, password)
        VALUES ('therapist', 'therapist')
        RETURNING id
    ),
    new_patient AS (
        INSERT INTO users(username, password)
        VALUES ('patient', 'patient')  -- ojo: corregí "patiemt"
        RETURNING id
    ),
    insert_therapist AS (
        INSERT INTO therapist(id)
        SELECT id FROM new_therapist
        RETURNING id
    )
INSERT INTO patient(id, age, height, weight, therapist_id)
SELECT new_patient.id, 25, 170, 70, new_therapist.id
FROM new_patient, new_therapist;

INSERT INTO exercise(name, description) VALUES('biceps_right', 'Biceps (right)');
INSERT INTO exercise(name, description) VALUES('biceps_left', 'Biceps (left)');
INSERT INTO exercise(name, description) VALUES('quad_right', 'Quad (right)');
INSERT INTO exercise(name, description) VALUES('quad_left', 'Quad (left)');
INSERT INTO exercise(name, description) VALUES('triceps_right', 'Triceps (right)');
INSERT INTO exercise(name, description) VALUES('triceps_left', 'Triceps (left)');