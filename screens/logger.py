from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import StringProperty 
from widgets.exercise_logger import ExerciseLog, LogRow
from widgets.stop_watch import StopWatch

from utilities.session_manager import SessionManager
from utilities.dialogs import Dialogs

class Logger(Screen):
	session_manager = SessionManager()
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
						
	#this starts and finishes the workout session
	def workout_start_or_finish(self, *args):
		#what to do to start the session
		if not self.session_manager.session_started:
			#call the session manager to start the workout
			self.session_manager.start_session()
			#call the timer to start 
			self.ids.timer.start()
			#change the button text to finish workout
			self.ids.session_ctrl.values.pop()
			self.ids.session_ctrl.values.append("Finish Workout")			
		#what to do to finish a workout 
		elif self.session_manager.sets_submitted == self.session_manager.total_set_count:
			#stop stop watch 
			self.ids.timer.stop()
			#add session length to sessions data dict
			self.session_manager.sessions_table_data['length'] = self.ids.timer.elap_time
			#tell the session manager to finish the workout
			self.session_manager.finish_session()
			#reset the stopwatch
			self.ids.timer.reset()
			#clear out all exercises 
			self.ids.content_box.ids.container.clear_widgets()
			#go to the start workout screen
			App.get_running_app().root.current = 'start_workout'
			self.ids.session_ctrl.values.pop()
			self.ids.session_ctrl.values.append("Start Workout")
		elif self.session_manager.session_started and self.session_manager.sets_submitted < self.session_manager.total_set_count:
			Dialogs.error_popup("There are unsubmitted sets remaining.")
						
	def page_select(self, instance, value):
		if value == "history":
			App.get_running_app().root.current = 'history'
		elif value == "start workout":
			App.get_running_app().root.current = 'start_workout'
			
	def session_ctrl(self, instance, value):
		if value == "Start Workout" or value == "Finish Workout":
			self.workout_start_or_finish(instance)
		elif value =="Abandon":
			self.abandon_session()
		elif value == "Add Exercise":
			App.get_running_app().root.current = 'exercise_selector'
			
	def abandon_session(self):
		#stop stop watch 
			self.ids.timer.stop()
			#tell the session manager to abandon the workout
			self.session_manager.abandon_session()
			#reset the stopwatch
			self.ids.timer.reset()
			#clear out all exercises 
			self.ids.content_box.ids.container.clear_widgets()
			#go to the start workout screen
			App.get_running_app().root.current = 'start_workout'
			self.ids.session_ctrl.values.pop()
			self.ids.session_ctrl.values.append("Start Workout")