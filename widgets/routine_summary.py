from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty

class Routines(ScrollView):
	routine_count = 1
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		child_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=20)
		
		child_layout.bind(minimum_height=child_layout.setter('height'))
		
		
		self.add_widget(child_layout)
	
class RoutineSummary(Button):
	pass