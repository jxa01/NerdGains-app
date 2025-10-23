from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty, ListProperty
from utilities.tools import TableTools
from utilities.sql import DbManager
from debug import log, exc

tt = TableTools()
			
class WorkoutSummary(BoxLayout):
	workout_title = StringProperty("")
	duration = StringProperty("")
	session_id = NumericProperty(0)
	total_volume = StringProperty("")
	intensity = StringProperty("")
	
	def on_session_id(self, instance, value):
		#generate sessions derived data
		session_data = tt.get_sessions(value)		
		start_dt = session_data['start_dt']
		#generate workout duration
		if session_data['length']:
			duration_raw = session_data['length']
			min, sec = divmod(duration_raw, 60)
			self.duration = f"{int(min):02}:{int(sec):02}"
		else:
			self.duration = "No duration data"
		#generate workout title
		routine = session_data['routine']
		if routine:
			self.workout_title = f"{routine} on {start_dt}"
		else: 
			self.workout_title = f"Your {start_dt} workout"
				
		#generate set_metric_values specific data
		smvs_data = tt.get_smvs(value)
		if not smvs_data:
			self.total_volume = "None"
		else:
			#check if metrics are weight and reps and if True multiply them for set volume and add them for total volume.
			volume = 0
			rep_count = 0
			reps = 0
			weight = 0
			for smv in smvs_data:
				if smv['metric_id'] == 1:
					reps = smv['value']
					rep_count += reps
				if smv['metric_id'] == 2:
					weight = smv['value']
					set_v = reps * weight
					volume += set_v
			self.total_volume = str(volume)
			intense_calc = volume/rep_count if rep_count else 0
			self.intensity = f"{intense_calc:.2f}"