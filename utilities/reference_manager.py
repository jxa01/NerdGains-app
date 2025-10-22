from kivy.app import App
from debug import log

class ReferenceManager:
	app = None
	logger = None
	session_manager = None

	@classmethod
	def init_refs(cls):
			cls.app = App.get_running_app()
			if cls.app:	
				cls.logger = cls.app.root.get_screen('logger')
			cls.session_manager = cls.logger.session_manager
			
	@classmethod
	def get_session_manager(cls):
		if not cls.session_manager:
			cls.init_refs()
		return cls.session_manager		
		
	@classmethod
	def get_logger(cls):
		if not cls.logger:
			cls.init_refs()
		return cls.logger					