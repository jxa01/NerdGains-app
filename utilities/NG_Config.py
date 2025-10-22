from datetime import datetime
from kivy.storage.jsonstore import JsonStore

class NG_Config:
	def __init__(self, path="NG_Config.json"):
		self.store = JsonStore(path)
		
	def start_session(self, session_id):
		self.store.put(
		'session',
		isactive=True,
		session_id=session_id,
		save_dt=datetime.now().isoformat())
		
	def finish_session(self):
		self.store.put(
		'session', 
		isactive=False,
		session_id=None,
		save_dt=datetime.now().isoformat())
	
	def update_save_dt(self):
		if self.store.exists('session'):
			session_data = self.store.get('session')
			session_data['save_dt'] = datetime.now().isoformat()
			self.store.put(
		'session',
		**session_data)
		
	def get_app_state(self):
		if not self.store.exists('session'):
			return {'isactive': False, 'session_id': None, 'save_dt': None}
		return self.store.get('session')
		
	def abandon_session(self):
		if self.store.exists('session'):
			self.store.delete('session')