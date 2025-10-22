import sqlite3
from contextlib import contextmanager

db_path = "C:/dev/NerdGains/workout_app_db.db"

def dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}

#establishes a db connection in accordance with the db_path variable.
@contextmanager
def est_db_conn(row_type='dict'):
	conn = sqlite3.connect(db_path)
	if row_type == 'dict':
		conn.row_factory = dict_factory
	elif row_type == 'row':
		conn.row_factory = sqlite3.Row
	
	try:
		yield conn
	finally:
		conn.close()
	
class DbManager():
	
	#returns the column data for a given table name
	def get_col_names(self, table_name):
		with est_db_conn() as conn:
			cur = conn.cursor()
			sql = f"PRAGMA table_info({table_name})"
			cur.execute(sql)
			return [dic['name'] for dic in cur.fetchall()]
			
	def table_names(self):
		with est_db_conn() as conn:
			cur = conn.cursor()
			sql = "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
			cur.execute(sql)
			result = cur.fetchall()
			table_names = [dict['name'] for dict in result]
			return table_names
	
	def query(self, 
	table_name, 
	col_names='*', 
	where=None,
	order_by=None,
	params=None,
	limit=None):
		with est_db_conn() as conn:
			cur = conn.cursor()
			sql =  f"SELECT {col_names} FROM {table_name}"
			if where:
				sql += f" WHERE {where}"
			if order_by:
				sql += f" ORDER BY {order_by}"
			if limit:
				sql += f" LIMIT {limit}"
			cur.execute(sql, params or [])
			result = cur.fetchall()
			return result
		
	#returns all rows as a list of tuples from the given table.
	def full_table_fetch(self, table_name):
		with est_db_conn() as conn:
			cur = conn.cursor()
			sql = f"SELECT * FROM {table_name}"
			cur.execute(sql)
			rows = cur.fetchall()
			return rows
			
	#takes a table name, and a dict of the column names as keys and data as values. It commits to db at each call. 
	def write_new_data(self, table_name, data):
		if not data:
			raise ValueError("Cannot insert empty data")
		col_names = list(data.keys())
		col_names_sql = ", ".join(col_names)
		placeholders = ", ".join(f':{k}' for k in col_names)
		with est_db_conn() as conn:
			cur = conn.cursor()
			cur.execute("PRAGMA foreign_keys = ON;")
			sql = f'''INSERT INTO {table_name}({col_names_sql}) VALUES({placeholders})'''
			cur.execute(sql, data)
			conn.commit()
			return cur.lastrowid
			
	def update_data(self, table_name, data, where=None, where_params=None):
		set_clause = ", ".join(f"{key} = ?" for key in data)
		params = list(data.values())
		with est_db_conn() as conn:
			cur = conn.cursor()
			cur.execute("PRAGMA foreign_keys = ON;")
			sql = f"UPDATE {table_name} SET {set_clause}"
			if where:
				sql += f" WHERE {where}"
				if where_params:
					params.extend(where_params)
			cur.execute(sql, params)
			conn.commit()
			
	def delete_data(self, 
	table_name,  
	where=None,
	params=None):
		with est_db_conn() as conn:
			cur = conn.cursor()
			cur.execute("PRAGMA foreign_keys = ON;")
			sql =  f"DELETE FROM {table_name}"
			if where:
				sql += f" WHERE {where}"
			cur.execute(sql, params or [])
			conn.commit()
			
	def nuke_tables(self):
		self.delete_data('set_metric_values')
		self.delete_data('sqlite_sequence', where='name = ?', params=['set_metric_values'])
		self.delete_data('exe_logs')
		self.delete_data('sqlite_sequence', where='name = ?', params=['exe_logs'])
		self.delete_data('sets')
		self.delete_data('sqlite_sequence', where='name = ?', params=['sets'])
		self.delete_data('sessions')
		self.delete_data('sqlite_sequence', where='name = ?', params=['sessions'])
		print("tables nuked")