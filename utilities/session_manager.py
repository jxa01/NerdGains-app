from kivy.app import App
from datetime import datetime
#from tools import TableTools
from utilities.tools import TableTools
from utilities.NG_Config import NG_Config
from utilities.reference_manager import ReferenceManager
from widgets.exercise_logger import ExerciseLog, LogRow	
from debug import log, exc
		
class SessionManager:	
	def __init__(self):
		self.table_tools = TableTools()
		self.ng_config = NG_Config()
		self.selected_exercises=[]
		self.session_started = False
		self.recovery_mode = False
		self.session_id = 0
		self.sessions_table_data = {'start_dt': None, 'length': None, 'routine': None}
		self.total_set_count = 0
		self.sets_submitted = 0		
		
	#adds logs to logger screen
	def post_exercises(self):
		#session_id initializes at 0 so this checks if the session has been added to the sessions table yet. The session does not start until commanded in session control or by a log row submittion. 
		if self.session_id == 0:
			self.create_session_id()						
		for i in self.selected_exercises:
			exercise_info = self.table_tools.exercise_lookup(i)			
			exe_log_data = {'exe_id': exercise_info[0]['exe_id'], 'session_id': self.session_id}			
			exe_log_id = self.table_tools.new_row('exe_logs', exe_log_data)					
			exercise_info.append(exe_log_id)	
			exe_log = self.log_builder(exercise_info)
			ReferenceManager.get_logger().ids.content_box.ids.container.add_widget(exe_log)			
		self.selected_exercises.clear()
		
	#creates session_id and adds it to instance the variable and the sessions table data dict
	def create_session_id(self):
			self.session_id = self.table_tools.new_row('sessions', self.sessions_table_data)
			self.sessions_table_data['session_id'] = self.session_id
		
	#creates an exercise log widget				
	def log_builder(self, exercise_info):
		metric1, metric2, metric3 = (exercise_info[1] + ['','',''])[:3]	
		exe_log = ExerciseLog(metric1, metric2, metric3, exe_id=exercise_info[0]['exe_id'], exe_log_id=exercise_info[2], submit_row_callback=self.submit_row)	
		exe_log.exercise_name = exercise_info[0]['exe_name']
		print(f"adding submit_row_callback: {exe_log.submit_row_callback}")
		exe_log.delete_full_exercise_callback = self.delete_exercise
		return exe_log
	
	#creates a new row in the sets table
	def set_builder(self, exe_log_id, set_count):
		sets_data = {'set_type_id': 1, 'set_number': set_count, 'exe_log_id': exe_log_id}
		new_set_id = self.table_tools.new_row('sets', sets_data)
		return new_set_id
	
	#subittion callback function for the exercise log widget (needs more cleaning)
	def submit_row(self, set_id, sets_data, smvs_data):
		#update sets table  data in case set type was changed
		self.table_tools.update_data('sets', sets_data, where="set_id = ?", where_params=[set_id])
		#prep and submit smvs data		
		metric_ids = {self.table_tools.met_to_met_id(metric): value for metric, value in smvs_data.items()}
		
		#add the set id to each row being submitted and submit them.
		for i in metric_ids:
			row = {'set_id': set_id, 'metric_id': i, 'value': metric_ids[i]}
			self.table_tools.new_row(
			'set_metric_values', 
			row)
		self.sets_submitted += 1		
		
		#this function gets loaded to the on_delete obj-prop of the exercise log widget so it can delete its self from the ui and db. (needs cleaning)
	def delete_exercise(self, exercise_log, exe_log_id):
		self.table_tools.delete_table_row('exe_logs', where='exe_log_id = ?', params=[exe_log_id])
		App.get_running_app().root.get_screen('logger').ids.content_box.ids.container.remove_widget(exercise_log)
		
	def start_session(self):
		self.sessions_table_data['start_dt'] = datetime.now().strftime("%x, %I:%M%p")		
		self.table_tools.update_data('sessions', self.sessions_table_data, where='session_id = ?', where_params=[self.session_id])
		self.session_started = True
		self.ng_config.start_session(self.session_id)
			
	def unsubmit_row(self, set_id):
		self.table_tools.delete_table_row(
		'set_metric_values', 
		where='set_id = ?', 
		params=[set_id])
		self.sets_submitted -= 1
			
	def delete_row(self, set_id):
		self.table_tools.delete_table_row(
		'sets', 
		where='set_id = ?', 
		params=[set_id])
		self.total_set_count -= 1
		
	def finish_session(self):
		self.table_tools.update_data(
		'sessions', 
		self.sessions_table_data,
		where='session_id = ?',
		where_params=[self.session_id])
		self.wo_started = False
		self.ng_config.finish_session()
		
	def abandon_session(self, session_id):
		self.table_tools.delete_table_row(
		'sessions', 
		where='session_id = ?', 
		params=[session_id])
		self.wo_started = False		
		self.session_id = 0
		self.ng_config.abandon_session()
		
		
	def session_recovery(self, session_id):
		self.recovery_mode = True
		session_lookup =  self.table_tools.session_lookup(session_id)
		recovered_sessions_data = session_lookup[0]
		recovered_logs_data = session_lookup[1]
		#set up local session data
		self.recover_sessions_data(recovered_sessions_data, session_id)
		#set up logger screen
		self.recover_logger_screen(recovered_logs_data)
		#look up and add in logs
		
		self.recovery_mode = False				
		App.get_running_app().root.current = 'logger'
		
	def recover_session_data(self, sessions_data, session_id):
		self.session_id = session_id
		self.wo_started = True
		self.sessions_table_data = sessions_data

	#builds log widgets and adds them to logger from recovered data
	def recover_logger_screen(self, recovered_logs_data):
		for recovered_log in recovered_logs_data:
			exe_id = recovered_log['exe_id']
			exe_info = self.table_tools.exercise_lookup(exe_id)
			exe_info.append(exe_id)
			log_widget = self.log_builder(exe_info)
			#look up sets and smvs data for each log and populate data into ui.
			sets_data, smvs_data = self.table_tools.log_lookup(recovered_log['exe_log_id'])
			for set_info, set_metric_values in zip(sets_data, smvs_data):
				metric_values = [smv['value'] for smv in set_metric_values]	
				row_data = [set_info['set_id'], set_info['exe_log_id'], set_info['set_type_id']] + metric_values
				log_widget.row_recover(row_data)
			ReferenceManager.get_logger().ids.content_box.ids.container.add_widget(log_widget)