import sqlite3

conn = sqlite3.connect("workout_app_db.db")
cur = conn.cursor()
cur.execute("PRAGMA foreign_keys = ON;")

#a catalog of all muscles to be tracked including information about each one.
cur.execute(
'''CREATE TABLE IF NOT EXISTS muscles(
muscle_id INTEGER PRIMARY KEY AUTOINCREMENT,
muscle_com_name TEXT NOT NULL,
muscle_sci_name TEXT,
muscle_desc TEXT,
muscle_group TEXT)''')

#the roles that a muscle can have during an exercise.
cur.execute(
'''CREATE TABLE IF NOT EXISTS emphs(
emph_id INTEGER PRIMARY KEY AUTOINCREMENT,
role TEXT NOT NULL)''')

#workout session tracker
cur.execute(
'''CREATE TABLE IF NOT EXISTS sessions(
session_id INTEGER PRIMARY KEY AUTOINCREMENT,
start_dt TEXT,
length REAL,
routine TEXT)''')

#a catalog of all exercises that could be done including information about each one.
cur.execute(
'''CREATE TABLE IF NOT EXISTS exe(
exe_id INTEGER PRIMARY KEY AUTOINCREMENT,
exe_name TEXT NOT NULL,
exe_disc TEXT,
exe_notes TEXT)''')

#different metrics which can be tracked
cur.execute(
'''CREATE TABLE IF NOT EXISTS metrics(
metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
metric TEXT NOT NULL)''')

#this ties metrics to specific exercises so you cant do bench press for distance. 
cur.execute(
'''CREATE TABLE IF NOT EXISTS exercise_metrics(
metric_id INTEGER,
exe_id INTEGER,
   PRIMARY KEY(metric_id, exe_id),
   FOREIGN KEY(metric_id) REFERENCES metrics(metric_id) ON DELETE CASCADE,
   FOREIGN KEY(exe_id) REFERENCES exe(exe_id) ON DELETE CASCADE
   )''')

#this ties specific muscles to excerces
cur.execute(
'''CREATE TABLE IF NOT EXISTS exercise_muscles(
exe_id INTEGER, 
muscle_id INTEGER,
emph_id INTEGER,
PRIMARY KEY(exe_id, muscle_id, emph_id),
FOREIGN KEY(exe_id) REFERENCES exe(exe_id) ON DELETE CASCADE,
FOREIGN KEY(muscle_id) REFERENCES muscles(muscle_id) ON DELETE CASCADE,
FOREIGN KEY(emph_id) REFERENCES emphs(emph_id) ON DELETE CASCADE)''')

#the different types of sets that you do (drop set, to failure, etc.)
cur.execute(
'''CREATE TABLE IF NOT EXISTS set_types(
set_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_type TEXT)''')


cur.execute(
'''CREATE TABLE IF NOT EXISTS exe_logs(
exe_log_id INTEGER PRIMARY KEY AUTOINCREMENT,
exe_id INTEGER,
session_id INTEGER,
FOREIGN KEY(session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
FOREIGN KEY(exe_id) REFERENCES exe(exe_id) ON DELETE CASCADE)''')

#a log of each set performed and record of the exercise log it belonged to.
cur.execute(
'''CREATE TABLE IF NOT EXISTS sets(
set_id INTEGER PRIMARY KEY AUTOINCREMENT,
set_type_id INTEGER,
set_number INTEGER,
exe_log_id INTEGER,
FOREIGN KEY(set_type_id) REFERENCES set_types(set_type_id) ON DELETE CASCADE)''')

#tracks the specefic values completed during exercise (set_id was ___ weight, or set_id was ___ reps)

cur.execute(
'''CREATE TABLE IF NOT EXISTS set_metric_values(
set_id INTEGER,
metric_id INTEGER,
value REAL,
PRIMARY KEY(set_id, metric_id),
FOREIGN KEY(set_id) REFERENCES sets(set_id) ON DELETE CASCADE,
FOREIGN KEY(metric_id) REFERENCES metrics(metric_id) ON DELETE CASCADE)'''
)

conn.commit()

conn.close()

