from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from utilities.tools import TableTools

class HistoryScreen(Screen):
	data = ListProperty([])
	def on_pre_enter(self, *args):
		tt = TableTools()
		result = tt.get_session_ids()
		self.data = result
		
	def page_select(self, instance, value):
		if value == "Start Workout":
			App.get_running_app().root.current = 'start_workout'
		elif value == "Current Session":
			App.get_running_app().root.current = 'logger'
		