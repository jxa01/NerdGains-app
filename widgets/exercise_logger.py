from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from utilities.tools import TableTools
from utilities.reference_manager import ReferenceManager
from debug import log, exc

#ExerciseLog records data from a single exercise.
class ExerciseLog(BoxLayout):	
	#stores a call back to a function so it can delete itself. 	
	delete_full_exercise_callback = ObjectProperty(None)
	#titles
	exercise_name = StringProperty("")
	metric1 = StringProperty("")
	metric2 = StringProperty("")
	metric3 = StringProperty("")

	def __init__(self, metric1, metric2, metric3, exe_id, exe_log_id, submit_row_callback,**kwargs):
		self.submit_row_callback = submit_row_callback
		self.tt = TableTools()
		self.session_manager_ref = ReferenceManager.get_session_manager()
		self.exe_id = exe_id
		self.exe_log_id = exe_log_id
		self.set_count = 0
		self.metric1 = metric1
		self.metric2 = metric2
		self.metric3 = metric3
		super().__init__(**kwargs)
		lbl_width = App.get_running_app().Sizes['column']
		lbl1 = Label(text=self.metric1, size_hint_x=None, width=lbl_width)
		lbl2 = Label(text=self.metric2, size_hint_x=None, width=lbl_width)
		lbl3 = Label(text=self.metric3, size_hint_x=None, width=lbl_width)
		if self.metric3:
			self.ids.title_row.add_widget(lbl1)
			self.ids.title_row.add_widget(lbl2)
			self.ids.title_row.add_widget(lbl3)
		elif self.metric2:
			self.ids.title_row.add_widget(lbl1)
			self.ids.title_row.add_widget(lbl2)
		else:			
			self.ids.title_row.add_widget(lbl1)
		if not self.session_manager_ref.recovery_mode:
			self.add_row(exe_log_id=self.exe_log_id)
			
	#if minimum_height of rows widget changes update height to match.	
	def on_kv_post(self, instance):
		self.ids.rows.bind(minimum_height=self.ids.rows.setter('height'))
				 
	#adds another row for additional sets
	def add_row(self, exe_log_id):
		self.session_manager_ref.total_set_count += 1
		self.set_count += 1
		set_id = self.session_manager_ref.set_builder(exe_log_id, self.set_count)
		row = LogRow(self.metric1, self.metric2, self.metric3, set_id, exe_log_id)
		row.update_labels_callback= self.update_labels
		row.set_count = self.set_count
		row.submit_row_callback = self.submit_row_callback
		#add the widget to the layout		
		self.ids.rows.add_widget(row)
		
	#adds rows from a recovered session without readding them to the db and populates textinputs if metric values we're entered perviously
	def row_recover(self, row_data):
		set_id, exe_log_id, set_type = row_data[:3]
		self.session_manager_ref.total_set_count += 1
		self.set_count += 1
		#make the LogRow
		row = LogRow(self.metric1, self.metric2, self.metric3, set_id, exe_log_id)
		row.update_labels_callback= self.update_labels
		row.set_type_update("", self.tt.map_set_type(set_type))
		row.set_count = self.set_count
		row.submit_row_callback = self.submit_row_callback
		#add the widget to the layout		
		self.ids.rows.add_widget(row)
		#fill in the metric inputs with the recovered smvs if any we're given.
		metric_values = row_data[3:6]
		metric_value_inputs = list(reversed(row.ids.metric_inputs.children))
		if metric_values:
			for input_field, value in zip(metric_value_inputs, metric_values):
				input_field.text = str(value)
				input_field.disabled=True
			row.ids.set_type.disabled=True
			row.ids.submit_button.state = 'down'

	#deletes only the last added row. 
	def delete_row(self):
		if len(self.ids.rows.children) > 1:
			row = self.ids.rows.children[0]
			self.session_manager_ref.delete_row(row.set_id)
			self.ids.rows.remove_widget(self.ids.rows.children[0])
			self.set_count -=1

	#executes the callback to delete the entire exercise if such a callback was set at initialization.
	def request_delete(self):
			self.delete_full_exercise_callback(self, self.exe_log_id)
			
	def log_ctrl(self, instance, value):
		if value == "Delete Excercise":
			self.request_delete()

	def update_labels(self, instance, label):
		if label:
			self.ids.title_row.add_widget(label)
		else:
			self.ids.title_row.remove_widget(self.ids.title_row.children[0])

#______a row to log an  individual set________
class LogRow(BoxLayout):
	set_count = NumericProperty(0)
	metric1_data = NumericProperty(0)
	metric2_data = NumericProperty(0)
	metric3_data = NumericProperty(0)
	submit_row_callback = ObjectProperty(None)
	update_labels_callback = ObjectProperty(None)
	
	def __init__(self, metric1, metric2, metric3, set_id, exe_log_id, **kwargs):
		self.session_manager_ref = ReferenceManager.get_session_manager()
		self.tt = TableTools()
		self.set_id = set_id
		self.exe_log_id = exe_log_id
		self.set_type = 1
		self.metric1 = metric1
		self.metric2 = metric2
		self.metric3 = metric3
		super().__init__(**kwargs)
		metric_input = Metric(metric=self.metric1, hint_text=self.metric1)
		metric_input.data_input = self.metric_data_input
		self.ids.metric_inputs.add_widget(metric_input)
		#if metric2 is set
		if self.metric2:
			#make a Metric class widget and set the hint text to the metric name
			metric_input = Metric(metric=self.metric2, hint_text=self.metric2)
			#fill the data_inout ObjectProperty of Metric object with the function found below
			metric_input.data_input = self.metric_data_input
			#add it to its container in the kv
			self.ids.metric_inputs.add_widget(metric_input)
		#see annotations for metric2	
		if self.metric3:
			self.ids.set_type.values = ("Normal", "drop set")
			metric_input = Metric(metric=self.metric3, hint_text=self.metric3)
			metric_input.data_input = self.metric_data_input			
			self.ids.metric_inputs.add_widget(metric_input)
								
	def set_type_update(self, instance, value):
		self.set_type = self.tt.map_set_type(value)
		self.ids.set_type.text = value
		#what to do for RIR
		if value != "RIR" and self.metric3 == "RIR":
			self.ids.metric_inputs.remove_widget(self.ids.metric_inputs.children[0])
			self.metric3 = ''
			self.update_labels_callback("", "")
			#self.parent.parent.ids.title_row.remove_widget(self.parent.parent.ids.title_row.children[0])
		if value == "RIR" and not self.metric3:
			#make the metric_input
			self.metric3 = "RIR"
			metric_input = Metric(metric=self.metric3, hint_text=self.metric3)
			metric_input.data_input = self.metric_data_input
			self.ids.metric_inputs.add_widget(metric_input)
			self.session_manager_ref.change_set_type(self.set_id, self.set_type)
			#make the label
			lbl_width = App.get_running_app().Sizes['column']
			lbl3 = Label(text="RIR", size_hint_x=None, width=lbl_width)
			self.update_labels_callback("", lbl3)
				
	def metric_data_input(self, metric, value):
		if value:
			if metric == self.metric1:
				self.metric1_data = value
			elif metric == self.metric2:
				self.metric2_data = value
			else:
				self.metric3_data = value
			self.validate_input()
				
	def validate_input(self, *args):
		if self.metric3:
			self.ids.submit_button.disabled = not (self.metric1_data and self.metric2_data and self.metric3_data)
		elif self.metric2:
			self.ids.submit_button.disabled = not (self.metric1_data and self.metric2_data)
		else:
			self.ids.submit_button.disabled = not (self.metric1_data)
			
	#checks if in recovery mode before submitting or unsubmitting rows
	def row_submit_btn(self, value):
		if self.session_manager_ref.recovery_mode:
			return
		if value == 'down':
			self.submit_row()
		else:
			self.unsubmit_row()

	#what to do when the submit button gets hit for a log row.
	def submit_row(self):
		#check if the session has been started and start it if needed.
		if not self.session_manager_ref.session_started:
			ReferenceManager.get_logger().workout_start_or_finish()			
		#if on_submit call back is set gather set data and smvs data and send it to the session manager object (session_manager).
		if self.submit_row_callback:
			sets_data = {'set_type_id': self.set_type, 'set_number': self.set_count, 'exe_log_id': self.exe_log_id}	
			if self.metric3:
				smvs_data = {self.metric1: self.metric1_data, self.metric2: self.metric2_data, self.metric3: self.metric3_data}			
			elif self.metric2:
				smvs_data = {self.metric1: self.metric1_data, self.metric2: self.metric2_data}
			else:
				smvs_data = {self.metric1: self.metric1_data}				
			self.submit_row_callback(self.set_id, sets_data, smvs_data)
			self.ids.set_type.disabled=True
			for child in self.ids.metric_inputs.children:
				child.disabled=True
							
	def unsubmit_row(self):
		self.session_manager_ref.unsubmit_row(self.set_id)
		self.ids.set_type.disabled=False
		for child in self.ids.metric_inputs.children:
			child.disabled=False
			
	def metric_recovery(self, metric1_data=0, metric2_data=0, metric3_data=0):
		self.ids.metric_inputs.children[0].on_data_entry(rec=metric1_data)
		
class Metric(TextInput):
	data_input = ObjectProperty(None)
	def __init__(self, metric, **kwargs):
		self.app = App.get_running_app()
		self.metric = metric
		super().__init__(**kwargs)
		self.size_hint = (None, None)
		self.width = self.app.Sizes['column']
		self.height = self.app.Sizes['normal_line']
		self.input_type = 'number'
		self.input_filter ='float'
		self.hint_text_color = self.app.Colors['disabled_text']
		self.foreground_color = self.app.Colors['primary_text']
		self.halign = 'center'
		self.valign = 'middle'
		self.multiline = False
		self.background_color = [0, 0, 0, 0]
		self.bind(text=self.on_data_entry)
			
	def on_data_entry(self, instance, value):
		if self.data_input:
			self.data_input(self.metric, value)