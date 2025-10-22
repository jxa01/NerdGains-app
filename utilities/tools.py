from datetime import datetime

#from sql import DbManager
from utilities.sql import DbManager

db = DbManager()
class TableTools():
	
	#returns a row from the sessions table with a given session_id
	def get_sessions(self, session_id):
		row = db.query('sessions', where='session_id = ?', params=(session_id,))
		return row
		
	#pulls all sets corrisponding to a given session_id
	def get_sets(self, session_id):
		sets = db.query('sets', where='session_id = ?', params=(session_id,))
		return sets
		
	#pulls all the smvs corrisponding to a given session_id. returns as a 
	def get_smvs(self, session_id):
		#pull the logs for a session and the sets that go to them.		
		logs = db.query('exe_logs', col_names='exe_log_id', where='session_id = ?', params=(session_id,))
		#pulls out all sets that go to the given session
		sets = list()
		for dic in logs:
			q = db.query('sets', col_names='set_id', where='exe_log_id = ?', params=(dic['exe_log_id'],))
			for d in q:
				sets.append(d['set_id'])	
		#generate placeholders for the sql query
		placeholders = ', '.join('?' for id in sets)
		#pull out all the smvs associated with the sets list
		smvs = db.query('set_metric_values', col_names='metric_id, value', where=f'set_id IN ({placeholders})', params=sets)
		return smvs
	
	#returns a list of all session_ids	
	def get_session_ids(self):
		result = db.query('sessions', col_names='session_id')
		session_ids = [dict['session_id'] for dict in result]
		return result
			
	#returns a list of all the exercise names that are in the catalog (the exe table).
	def get_exercises(self):
		result = db.query('exe', col_names='exe_id, exe_name')	
		return result
		
	def exercise_lookup(self, exe_id):
		exe = db.query('exe', col_names='exe_id, exe_name', where='exe_id = ?', params=[exe_id])	
		exe_mets_q = db.query('exercise_metrics', col_names='metric_id', where=f'exe_id = {exe_id}')
		exe_mets = [dic['metric_id'] for dic in exe_mets_q]
		met_map = db.query('metrics')
		mets = []
		for dic in met_map:
			if dic['metric_id'] in exe_mets:
				mets.append(dic['metric'])
		return [exe[0], mets]
		
	#looks up all data related to a given session_id
	def session_lookup(self, session_id):
		sessions_data = db.query('sessions', where='session_id = ?', params=[session_id])
		logs_data = db.query('exe_logs', col_names='exe_log_id, exe_id', where='session_id = ?', params=[session_id])		
		return [sessions_data, logs_data]
		
	def log_lookup(self, exe_log_id):
		sets_data = db.query('sets', where='exe_log_id = ?', params=[exe_log_id])
		smvs_data = list()		
		for set in sets_data:
			param = set['set_id']
			smvs_data.append(db.query('set_metric_values', where='set_id = ?', params=[param]))
		return sets_data, smvs_data
	
	#adds a new row to a table	
	def new_row(self, table_name, data):
		db.write_new_data(table_name, data)
	
	#updates the data within existing rows			
	def update_data(self, table_name, data, where, where_params):
		db.update_data(table_name, data, where, where_params)

	#retrieves the last entered id of a table
	def get_last_id(self, table_name, id_name):
			result = db.query(table_name, col_names=id_name, order_by=f'{id_name} DESC', limit=1)
			last_id = result[0][id_name]
			return last_id
			
	#takes an exe_id and tells you what metrics apply to that exercise		
	def get_exe_mets(self, exe_id):
		exe_mets_q = db.query('exercise_metrics', col_names='metric_id', where=f'exe_id = {exe_id}')
		exe_mets = [dic['metric_id'] for dic in exe_mets_q]
		met_map = db.query('metrics')
		mets = []
		for dic in met_map:
			if dic['metric_id'] in exe_mets:
				mets.append(dic['metric'])
		return mets
		
	#takes a name and gives the id its mapped to
	def met_to_met_id(self, met):
		met_map = db.query('metrics')
		for dic in met_map:
			if met == dic['metric']:
				return str(dic['metric_id'])
				
				
	#takes a set type and returns a set_type_id
	def map_set_type(self, type):
		types_map = db.query('set_types')
		for dic in types_map:
			if type == dic['set_type']:
				return dic['set_type_id']
			elif type == dic['set_type_id']:
				return dic['set_type']
				
	def delete_table_row(self, table_name, where, params):
		db.delete_data(table_name, where, params)
					
		
#db = DbManager()	
# tt = TableTools()

# log_lookup = tt.log_lookup(2)
# sets_data = log_lookup[0]
# smvs_data = log_lookup[1]
# print(smvs_data)
#info = tt.exercise_lookup(2)
#print(info[0]['exe_id'])
#print(info[0]['exe_name'])
#print(info[1][0])
#print(db.get_col_data('sessions'))
#data = {'start_dt': '10/17/25, 8:28am', 'length': '1:35', 'routine': "core day"}
#tt.log_data('sessions', data)('reps'))