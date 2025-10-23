#kivy stuff
from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.metrics import sp, dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder

#custom widgets
from widgets.my_widgets import DropButton, MyDropDown, NavBar
from widgets.workout_summary import WorkoutSummary
from widgets.routine_summary import Routines
from widgets.exercise_logger import ExerciseLog, LogRow
from widgets.stop_watch import StopWatch

#screens
from screens.history import HistoryScreen
from screens.start_workout import StartWorkoutScreen
from screens.logger import Logger
from screens.exercise_selector import ExerciseSelector

#utils
from utilities.NG_Config import NG_Config
from utilities.dialogs import Dialogs
 
#custom widget .kvs
Builder.load_file('widgets/my_widgets.kv')
Builder.load_file('widgets/workout_summary.kv')
Builder.load_file('widgets/routine_summary.kv')
Builder.load_file('widgets/exercise_logger.kv')

#screen .kvs
Builder.load_file('screens/history.kv')
Builder.load_file('screens/start_workout.kv')
Builder.load_file('screens/logger.kv')
Builder.load_file('screens/exercise_selector.kv')
#____________________________________
	
Window.softinput_mode = 'below_target'

class WorkoutTrackerApp(App):
	
	def on_start(self):
		self.ng_config = NG_Config()
		state = self.ng_config.get_app_state()
		if state['isactive']:
			Dialogs.session_recovery(state['session_id'])
		
	#theme colors
	Colors = {
	'background': hex('121212'), 
	'surface': hex('1E1E2E'),
	'primary': hex('303060'),
	'primary_down': hex('1E1E3B'),
	'secondary': hex('06B6D4'),
	'secondary_down': hex('04798D'),
	'primary_text': hex('FFFFFF'),
	'secondary_text': hex('E0E0E0'),
	'disabled_text': hex('C9A3AF'),
	'delete/error': hex('EF4444'),
	'delete/error_down': hex('BD1010')
	}
	#theme sizes
	Sizes = {
	'title_line': dp(45),
	'title_font': sp(25),
	'normal_line': dp(40),
	'normal_font': sp(20),
	'column': dp(200)}
	
	def build(self):
		sm = ScreenManager()	
		sm.add_widget(StartWorkoutScreen(name = 'start_workout'))		
		sm.add_widget(HistoryScreen(name = 'history'))
		sm.add_widget(Logger(name = 'logger'))
		sm.add_widget(ExerciseSelector(name = 'exercise_selector'))
		return sm
	
WorkoutTrackerApp().run()