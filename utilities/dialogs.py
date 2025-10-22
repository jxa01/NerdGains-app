from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.metrics import dp

class Dialogs:
	
	@staticmethod
	def error_popup(message):
		app = App.get_running_app()
		layout = BoxLayout(
		orientation='vertical',
		padding=dp(10),
		spacing=dp(20))
		lbl = Label(text=message, color=app.Colors['primary_text'])
		layout.add_widget(lbl)
		
		popup = Popup(
		title="Error:",
		title_color=app.Colors['secondary'],
		separator_color=app.Colors['secondary'],
		background='',
		background_color=app.Colors['surface'],
		content=layout,
		size_hint=(0.75, 0.25),
		)
		popup.open()
		
	@staticmethod
	def session_recovery(session_id):
		app = App.get_running_app()
		layout = BoxLayout(
		padding=dp(10),
		spacing=dp(20))
		
		recover = Button(text="Recover Session")
		abandon = Button(text="Abandon Session")
		layout.add_widget(recover)
		layout.add_widget(abandon)
				
		popup = Popup(
		title="Session in Progress",
		title_color=app.Colors['secondary'],
		separator_color=app.Colors['secondary'],
		background='',
		background_color=app.Colors['surface'],
		content=layout,
		size_hint=(0.75, 0.25),
		auto_dismiss=False
		)
		logger = App.get_running_app().root.get_screen('logger')
		recover.bind(on_release=lambda x: (logger.session_manafer.session_recovery(session_id), popup.dismiss()))
		
		abandon.bind(on_release=lambda x: (logger.session_manager.abandon_session(session_id), popup.dismiss()))
		popup.open()