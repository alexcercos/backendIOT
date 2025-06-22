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
    weight FLOAT
);

CREATE TABLE IF NOT EXISTS pox_data (
    id SERIAL PRIMARY KEY,
    ts FLOAT NOT NULL,
    set_id INT REFERENCES sets(id) ON DELETE CASCADE,
    breath_rate FLOAT NOT NULL,
    heart_rate FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS kinect_data (
    id SERIAL PRIMARY KEY,
    ts FLOAT NOT NULL,
    set_id INT REFERENCES sets(id) ON DELETE CASCADE,
    completeness FLOAT NOT NULL,
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