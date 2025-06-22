import psycopg2
from psycopg2 import sql

DB_CONFIG = {
    "dbname" : "sjk007",
    "user" : "postgres",
    "password" : "admin",
    "host" : "localhost",
    "port" : "5432"
}


def connect():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        return conn, cursor
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None, None


def query(table):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM {table_name}").format(table_name=sql.Identifier(table))
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_patient_info(user):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM patient WHERE id = %s")
        cursor.execute(query, (user,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_session_info(session):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM sessions WHERE id = %s")
        cursor.execute(query, (session,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_exercise_info(exercise):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM exercise WHERE id = %s")
        cursor.execute(query, (exercise,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_user_sessions(user):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM sessions WHERE user_id = %s")
        cursor.execute(query, (user,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_sets(session):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("""
            SELECT 
                sets.*, 
                exercise.name AS exercise_name, 
                exercise.description AS exercise_desc
            FROM sets
            JOIN exercise ON sets.exercise_id = exercise.id
            WHERE sets.session_id = %s
        """)
        cursor.execute(query, (session,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_pox(set_id):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM pox_data WHERE set_id = %s")
        cursor.execute(query, (set_id,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def get_kinect(set_id):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT * FROM kinect_data WHERE set_id = %s")
        cursor.execute(query, (set_id,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def create_user(username, password, user_type, other_data):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("INSERT INTO users(username, password) VALUES (%s, %s) RETURNING id")
        cursor.execute(query, (username, password))
        user_id = cursor.fetchone()[0]
        if user_type == "Patient":
            query2 = sql.SQL("INSERT INTO patient(id, age, height, weight, therapist_id) VALUES (%s, %s, %s, %s, %s)")
            cursor.execute(query2, (user_id, other_data["age"], other_data["height"], other_data["weight"], other_data["therapist_id"]))
        else:
            query2 = sql.SQL("INSERT INTO therapist(id) VALUES (%s)")
            cursor.execute(query2, (user_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error executing query: {e}")
        return False 
    finally:
        cursor.close()
        conn.close()


def create_session(user_id):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("INSERT INTO sessions(user_id) VALUES (%s) RETURNING id")
        cursor.execute(query, (user_id))
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def finish_session(session_id):
    conn, cursor = connect()
    if not conn:
        return False
    try:
        query = sql.SQL("UPDATE sessions SET end_time = CURRENT_TIMESTAMP WHERE id = %s")
        cursor.execute(query, (session_id,))
        conn.commit()
        return cursor.rowcount > 0  # True if a row was updated
    except Exception as e:
        print(f"Error finishing session: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_exercise(session_id, exercise_id, reps, weight):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("""
            INSERT INTO sets(
                session_id, exercise_id, 
                mean_heart_rate, mean_breath_rate,
                duration, reps, weight)
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            RETURNING id""")
        cursor.execute(query, (session_id, exercise_id, 0, 0, 0, reps, weight))
        id = cursor.fetchone()[0]
        conn.commit()
        return id
    except Exception as e:
        print(f"Error executing query: {e}")
        return None 
    finally:
        cursor.close()
        conn.close()


def add_pox(data):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("""
            INSERT INTO pox_data(
                ts, set_id,
                breath_rate, heart_rate
            ) VALUES (
                %s, %s, %s, %s
            )
        """)
        
        values = (
            data.get("timestamp"),
            data.get("set_id"),
            data.get("breath_rate"),
            data.get("heart_rate")
        )

        cursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def add_kinect(data):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("""
            INSERT INTO kinect_data(
                ts, set_id,
                completeness, instability
            ) VALUES (
                %s, %s, %s, %s
            )
        """)
        
        values = (
            data.get("timestamp"),
            data.get("set_id"),
            data.get("completeness"),
            data.get("instability"),
        )

        cursor.execute(query, values)
        conn.commit()
        return True
    except Exception as e:
        print(f"Error executing query: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def get_set_graphs_pox(set_id):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT ts,heart_rate,breath_rate FROM pox_data WHERE set_id = %s")
        cursor.execute(query, (set_id,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def get_set_graphs_kinect(set_id):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT ts,completeness,instability FROM kinect_data WHERE set_id = %s")
        cursor.execute(query, (set_id,))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()
    
def get_set_kinect_rep(set_id, min_ts):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("SELECT ts,completeness FROM kinect_data WHERE set_id = %s AND ts > %s")
        cursor.execute(query, (set_id,min_ts))
        columns = [desc[0] for desc in cursor.description]
        result = [dict(zip(columns, row)) for row in cursor.fetchall()]
        return result
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

def set_metrics(set_id, mean_hr, mean_br, duration):
    conn, cursor = connect()
    if not conn:
        return None
    try:
        query = sql.SQL("UPDATE sets SET mean_heart_rate = %s, mean_breath_rate = %s, duration = %s WHERE id = %s")
        cursor.execute(query, (mean_hr, mean_br, duration, set_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error executing query: {e}")
        return False 
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    conn, cursor = connect()
    if conn:
        cursor.execute("SELECT version();")
        print("PostgreSQL version:", cursor.fetchone())
        conn.close()