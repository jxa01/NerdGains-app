from kivy.uix.screenmanager import Screen
from kivy.app import App

class StartWorkoutScreen(Screen):
	def page_select(self, instance, value):
		if value == "History":
			App.get_running_app().root.current = 'history'