from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import ObjectProperty, ListProperty, NumericProperty
from utilities.tools import TableTools
from utilities.reference_manager import ReferenceManager
from debug import log

class ExerciseSelector(Screen):
	all_data = ListProperty([])
	data = ListProperty([])
	selected_exercises = set()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.tt = TableTools()
		exe = self.tt.get_exercises()
		self.data = [{'exe_id': i['exe_id'], 'text': i['exe_name'], 'state': 'normal'} for i in exe]
		self.all_data = self.data
		
	#filters down the data set based on user input
	def search(self, text):
		text = text.lower()
		filtered = [i for i in self.all_data if text in i['text'].lower()]
		self.data = filtered
		self.ids.RV.refresh_from_data()
	
	#this adds the exercises widgets to to the logger screen.
	def post_exercises(self):		
		#tell session_manager to post the selected exercises
		ReferenceManager.get_session_manager().post_exercises()
		#clear selected exercises now that its been used.
		self.selected_exercises.clear()
		#reset all the buttons in the exercise selector screen
		for row in self.data:
			row['state'] = 'normal'
		self.ids.RV.refresh_from_data()
		#go to the logger screen
		App.get_running_app().root.current = 'logger'
		#end of post exercises function
		
	def page_select(self, instance, value):
		if value == "History":
			App.get_running_app().root.current = 'history'
		elif value == "Routines":
			App.get_running_app().root.current = 'start_workout'
		elif value == "Current Session":
			App.get_running_app().root.current = 'logger'
		
class MyToggleButton(RecycleDataViewBehavior, ToggleButton):
	index = NumericProperty(0)
	exe_id = NumericProperty(0)
	rv = ObjectProperty()
	
	def refresh_view_attrs(self, rv, index, data):
		self.index = index
		self.rv = rv
		self.exe_id = data['exe_id']
		super().refresh_view_attrs(rv, index, data)
	
	def on_state(self, instance, value):
		session_manager_reference = ReferenceManager.get_session_manager()
		#update the 'state' value in the data set
		self.rv.data[self.index]['state'] = value
		#if the state changed to down add it to the selected exercises list if it isnt there already
		if value == 'down' and self.exe_id not in session_manager_reference.selected_exercises:
			session_manager_reference.selected_exercises.append(self.exe_id)
		# if the state changed to normal remove it from the selected exercises list if it is there in the first place.
		elif value == 'normal' and self.exe_id in session_manager_reference.selected_exercises:
			session_manager_reference.selected_exercises.remove(self.exe_id)