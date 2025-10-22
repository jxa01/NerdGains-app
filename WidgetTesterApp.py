from kivy.app import App
from kivy.metrics import sp, dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import Screen
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import StringProperty, ObjectProperty, ListProperty, NumericProperty
from utilities.tools import TableTools
from kivy.utils import get_color_from_hex as hex


#screen level logic
class ExerciseExplorer(Screen):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.tt = TableTools()
		self.exe_cat = self.tt.get_exercises()
		self.data = [{'text': dic['exe_name']} for dic in self.exe_cat]
		
		
#________testing code below______________
class WidgetTester(App):
	Sizes = {
	'title_line': dp(50),
	'title_font': sp(40),
	'normal_line': dp(40),
	'normal_font': sp(20)}
	Colors = {
	'background': hex('10002B'), 
'surface': hex('240046'),
'shadow': hex('120024'),
	'primary': hex('5A189A'),
	'primary_down': hex('#3f116c'),
'secondary': hex('3C096C'),
'primary_text': hex('5CFCFF'),
'secondary_text': hex('C77DFF'),
'disabled_text': hex('9D4EDD')}
	pass
	
WidgetTester().run()